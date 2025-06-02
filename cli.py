import argparse
import os
import shutil
import re
from repo_handler import clone_repo
from file_parser import parse_project_files
from chunker import chunk_files
from lld_generator import generate_llds
from merger import merge_llds, merged_llds_to_html, merge_llds_logically, merge_llds_parallel
from config_doc import document_properties
from prompts import LLD_GEN_PROMPT, LLD_MERGE_PROMPT
from config import CHUNK_SIZE
import sys

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def gen_lld_html(chunk, idx, level0_dir):
    out_path = os.path.join(level0_dir, f"lld_chunk_{idx}.html")
    print(f"[cli.py]   [LLDGEN] Generating LLD for chunk {idx}...", file=sys.stderr)
    input_text = "\n\n".join([open(f).read() for f in chunk if os.path.exists(f)])
    prompt = LLD_GEN_PROMPT + "Code to document:\n<pre><code>\n" + input_text + "\n</code></pre>\n"
    from llm_interface import ask_llm
    lld_html = ask_llm(prompt)
    html_text = getattr(lld_html, 'content', lld_html)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_text)
    print(f"[cli.py]   [LLDGEN] Done for chunk {idx}: {out_path}", file=sys.stderr)
    return out_path

def recursive_merge_llds(lld_files, debug_dir, chunk_size=CHUNK_SIZE):
    level = 1
    current_files = lld_files
    while len(current_files) > 1:
        print(f"[cli.py] 🧩 Merging LLDs for level{level}...\n", file=sys.stderr)
        level_dir = os.path.join(debug_dir, f"level{level}")
        ensure_dir(level_dir)
        chunks = chunk_files(current_files, chunk_size=chunk_size)
        def merge_lld_group(idx, chunk):
            print(f"[cli.py]   [MERGE] Merging LLD group {idx} (level{level})...", file=sys.stderr)
            out_path = os.path.join(level_dir, f"lld_level{level}_chunk_{idx}.html")
            merge_prompt = LLD_MERGE_PROMPT + "---\n\n".join([open(p, encoding="utf-8").read() for p in chunk])
            from llm_interface import ask_llm
            lld_merged = ask_llm(merge_prompt)
            merged_text = getattr(lld_merged, 'content', lld_merged)
            with open(out_path, "w", encoding="utf-8") as outfile:
                outfile.write(merged_text)
            print(f"[cli.py]   [MERGE] Done for group {idx}: {out_path}", file=sys.stderr)
            return out_path
        next_files = []
        from concurrent.futures import ThreadPoolExecutor, as_completed
        with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            futures = {executor.submit(merge_lld_group, i, chunk): i for i, chunk in enumerate(chunks)}
            for future in as_completed(futures):
                next_files.append(future.result())
        print(f"[cli.py] 📚 Level{level} LLDs: {next_files}\n", file=sys.stderr)
        current_files = next_files
        level += 1
    return current_files[0]

def main():
    print("[cli.py] 🚀 Starting LLDGen CLI!\n", file=sys.stderr)
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_url", help="Git repo URL to process")
    parser.add_argument("--output", default="./output", help="Output directory")
    args = parser.parse_args()

    output_dir = os.path.abspath(args.output)
    repo_dir = os.path.abspath("repository")  # Always clone at project root
    debug_dir = os.path.join(output_dir, "debug")
    ensure_dir(output_dir)
    ensure_dir(repo_dir)
    ensure_dir(debug_dir)

    print(f"[cli.py] 🧲 Cloning repo: {args.repo_url} into {repo_dir}\n", file=sys.stderr)
    local_path = clone_repo(args.repo_url, repo_dir)
    print(f"[cli.py] 📁 Repo cloned at: {local_path}\n", file=sys.stderr)

    print(f"[cli.py] 🔍 Parsing project files in {local_path}\n", file=sys.stderr)
    parsed_files = parse_project_files(local_path)
    print(f"[cli.py] 📄 Found {len(parsed_files)} files to process!\n", file=sys.stderr)

    # Level 0
    print(f"[cli.py] 🧩 Chunking files for LLD generation (level0)...\n", file=sys.stderr)
    level0_dir = os.path.join(debug_dir, "level0")
    ensure_dir(level0_dir)
    chunks = chunk_files(parsed_files, chunk_size=CHUNK_SIZE)
    print(f"[cli.py] 🧊 Total chunks created: {len(chunks)}\n", file=sys.stderr)
    print(f"[cli.py] 🤖 Generating LLDs for each chunk (level0)...\n", file=sys.stderr)
    lld_files_level0 = []
    from concurrent.futures import ThreadPoolExecutor, as_completed
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = {executor.submit(gen_lld_html, chunk, i, level0_dir): i for i, chunk in enumerate(chunks)}
        for future in as_completed(futures):
            lld_files_level0.append(future.result())
    print(f"[cli.py] 📚 LLDs generated: {lld_files_level0}\n", file=sys.stderr)

    # Recursive merging until one file remains
    print(f"[cli.py] 🧩 Recursively merging LLDs until one final LLD remains...\n", file=sys.stderr)
    final_html_path = recursive_merge_llds(lld_files_level0, debug_dir, chunk_size=CHUNK_SIZE)
    print(f"[cli.py] 🏆 Final merged LLD HTML at: {final_html_path}\n", file=sys.stderr)

    # Copy final LLD to output/component-lld.html
    output_component_path = os.path.join(output_dir, "component-lld.html")
    shutil.copyfile(final_html_path, output_component_path)
    print(f"[cli.py] 📄 Copied final LLD to: {output_component_path}\n", file=sys.stderr)

    print(f"[cli.py] 📝 Documenting config properties...\n", file=sys.stderr)
    document_properties(parsed_files, output_dir)
    print(f"[cli.py] ✅ LLD generation complete: {output_component_path} 🎉\n", file=sys.stderr)

if __name__ == "__main__":
    main()

