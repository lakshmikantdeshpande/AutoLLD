import os
import sys
from llm_interface import ask_llm
from prompts import LLD_GEN_PROMPT

def generate_llds(file_chunks, output_dir):
    print(f"[lld_generator.py] 🤖 Generating LLDs for {len(file_chunks)} chunks...", file=sys.stderr)
    llds = []
    for i, chunk in enumerate(file_chunks):
        print(f"[lld_generator.py] 🧩 Processing chunk {i+1}/{len(file_chunks)}: {chunk}", file=sys.stderr)
        input_text = "\n\n".join([open(f).read() for f in chunk if os.path.exists(f)])
        prompt = LLD_GEN_PROMPT + "Code to document:\n<pre><code>\n" + input_text + "\n</code></pre>\n"
        print(f"[lld_generator.py] 📝 Sending prompt to LLM (chunk {i})...", file=sys.stderr)
        lld = ask_llm(prompt)
        out_path = os.path.join(output_dir, f"lld_chunk_{i}.md")
        with open(out_path, "w") as f:
            f.write(lld.content)
        print(f"[lld_generator.py] 📄 LLD for chunk {i} written to {out_path}", file=sys.stderr)
        llds.append(out_path)
    print(f"[lld_generator.py] ✅ All LLDs generated!", file=sys.stderr)
    return llds
