from concurrent.futures import ThreadPoolExecutor
from llm_interface import ask_llm
import os
import re

def merge_llds(lld_paths, output_dir):
    merged_path = os.path.join(output_dir, "final_lld.html")
    return merge_llds_logically(lld_paths, merged_path)

def merge_llds_logically(lld_paths, output_path):
    """
    Logically merges multiple LLD HTML files into a single HTML file using LLM.
    The LLM will be prompted to merge the content, deduplicate, and combine diagrams and explanations.
    """
    merged_content = []
    for path in lld_paths:
        with open(path, encoding="utf-8") as infile:
            content = infile.read()
            merged_content.append(content)
    prompt = (
        "You are a software architect. Merge the following Low-Level Design (LLD) HTML documents into a single, logically consistent HTML LLD. "
        "Deduplicate sections, merge diagrams (especially mermaid diagrams), and ensure the resulting document is well-structured, readable, and not repetitive. "
        "Preserve all important details, but combine related information and diagrams where possible. Output in HTML.\n\n"
        "---\n\n".join(merged_content)
    )
    lld_merged = ask_llm(prompt)
    merged_text = getattr(lld_merged, 'content', lld_merged)
    with open(output_path, "w", encoding="utf-8") as outfile:
        outfile.write(merged_text)
    return output_path

def merge_llds_parallel(chunk_groups, output_dir, level_prefix):
    """
    Merge each chunk group in parallel using LLM-based HTML merging.
    Returns a list of output HTML file paths.
    """
    results = []
    def merge_group(idx, chunk):
        out_path = os.path.join(output_dir, f"{level_prefix}_chunk_{idx}.html")
        merge_llds_logically(chunk, out_path)
        return out_path
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(merge_group, i, chunk) for i, chunk in enumerate(chunk_groups)]
        for f in futures:
            results.append(f.result())
    return results

def merged_llds_to_html(lld_paths, output_dir):
    # Deprecated: now handled by LLM merging directly to HTML, so just return the last file
    # This function is kept for compatibility, but just copies the last file to output_dir/final_lld.html
    import shutil
    if not lld_paths:
        return None
    final_html_path = os.path.join(output_dir, "final_lld.html")
    shutil.copyfile(lld_paths[-1], final_html_path)
    return final_html_path

