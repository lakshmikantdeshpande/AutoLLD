import sys

def chunk_files(file_list, chunk_size):
    print(f"[chunker.py] 🧩 Chunking {len(file_list)} files with chunk size {chunk_size}...", file=sys.stderr)
    chunks = [file_list[i:i + chunk_size] for i in range(0, len(file_list), chunk_size)]
    print(f"[chunker.py] 🧊 Created {len(chunks)} chunks!", file=sys.stderr)
    return chunks
