import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

def read_file(file_path):
    """Reads and returns the content of a file."""
    try:
        with open(file_path, "r") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return ""

def process_template(template_path, output_path):
    """Processes the template file and writes the result to the output path."""
    output_content = []
    base_dir = Path(template_path).parent

    # Read the template file
    with open(template_path, "r") as template_file:
        lines = template_file.readlines()

    for line in lines:
        line = line.strip()
        if line.startswith("include "):
            # Include a single file
            include_path = line.split(" ", 1)[1].strip()
            full_path = base_dir / include_path
            output_content.append(read_file(full_path))

        elif line.startswith("include_dir "):
            # Include all files in a directory (sorted by creation date descending)
            include_dir = line.split(" ", 1)[1].strip()
            full_dir_path = base_dir / include_dir

            if full_dir_path.is_dir():
                files = sorted(
                    full_dir_path.iterdir(),
                    key=lambda x: x.stat().st_ctime,
                    reverse=True
                )
                for file in files:
                    if file.is_file():
                        output_content.append(read_file(file))
            else:
                print(f"Directory not found: {full_dir_path}")

        else:
            # Add the line as-is
            output_content.append(line)

    # Write to the output file
    with open(output_path, "w") as output_file:
        output_file.write("\n".join(output_content))
    print(f"Generated output written to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate markdown file from template")
    parser.add_argument("--template", required=True, help="Path to the template file")
    parser.add_argument("--output", required=True, help="Path to the output file")
    args = parser.parse_args()

    template_path = Path(args.template).resolve()
    output_path = Path(args.output).resolve()

    if not template_path.exists():
        print(f"Template file does not exist: {template_path}")
        sys.exit(1)

    # Ensure the output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Process the template and generate the output
    process_template(template_path, output_path)
