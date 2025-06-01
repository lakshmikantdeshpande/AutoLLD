import os
import yaml
import configparser

def document_properties(files, output_dir):
    out = []
    for file in files:
        if file.endswith(".properties"):
            with open(file) as f:
                lines = [line.strip() for line in f.readlines() if "=" in line and not line.strip().startswith("#")]
                out.extend([f"{file}: {line}" for line in lines])
        elif file.endswith(".yml") or file.endswith(".yaml"):
            try:
                with open(file) as f:
                    data = yaml.safe_load(f)
                    out.append(f"{file}:\n{yaml.dump(data, indent=2)}")
            except Exception:
                continue
    with open(f"{output_dir}/config_doc.md", "w") as f:
        f.write("\n\n".join(out))

