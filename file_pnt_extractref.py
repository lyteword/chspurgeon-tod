# The purpose of this script is to extract content from another file and paste it into the current one
# The idea is that whenever an important header within a commentary occurs, the original reference material can also be included

import sys
import os
import re

# Default directory path where reference files are stored
REFERENCE_DIR = "/home/architect/Projects/LyteWord/kjv/psalms"

def extract_exposition_section(lines):
    """Extract lines under ## Exposition until the next ## header."""
    in_exposition = False
    exposition_lines = []
    for line in lines:
        if line.startswith("## "):
            if in_exposition:
                break  # stop if we've reached the next section
            if line.strip() == "## Exposition":
                in_exposition = True
                continue
        if in_exposition:
            exposition_lines.append(line)
    return exposition_lines

def extract_reference_content(ref_filepath, reference_number):
    """Extract content from reference file that contains <sup>{d}</sup>."""
    try:
        with open(ref_filepath, "r", encoding="utf-8") as ref_file:
            for line in ref_file:
                if f"<sup>{reference_number}</sup>" in line:
                    # Remove the <sup>{d}</sup> tag and strip whitespace
                    return re.sub(rf"<sup>{reference_number}</sup>", "", line).strip()
    except FileNotFoundError:
        print(f"Reference file not found: {ref_filepath}")
    return None

def process_markdown(filename):
    """Main function to process markdown and insert blockquotes."""
    if not filename.endswith(".md"):
        print("Error: File must be a markdown file with .md extension.")
        return

    ref_filename = os.path.basename(filename)
    ref_filepath = os.path.join(REFERENCE_DIR, ref_filename)

    with open(filename, "r", encoding="utf-8") as main_file:
        lines = main_file.readlines()

    exposition_lines = extract_exposition_section(lines)
    updated_lines = []

    # The header you want to match will go here, it can be at any level
    # header_pattern = re.compile(r"^### Verse (\d+)")
    header_pattern = re.compile(r"^(?!.*-).*### Verse (\d+)")
    exposition_index = 0

    while exposition_index < len(exposition_lines):
        line = exposition_lines[exposition_index]
        match = header_pattern.match(line.strip())
        updated_lines.append(line)
        
        if match:
            reference_number = match.group(1)
            ref_content = extract_reference_content(ref_filepath, reference_number)
            if ref_content:
                updated_lines.append(f"\n> {ref_content}\n")
            else:
                updated_lines.append("\n> [Missing reference]\n")
        exposition_index += 1

    # Replace exposition section in original file
    output_lines = []
    in_exposition = False
    for line in lines:
        if line.strip() == "## Exposition":
            in_exposition = True
            output_lines.append(line)
            output_lines.extend(updated_lines)
            continue
        if in_exposition and line.startswith("## ") and line.strip() != "## Exposition":
            in_exposition = False
        if not in_exposition:
            output_lines.append(line)

    # Optional, you can create backups if needed
    # backup_filename = filename.replace(".md", "_backup.md")
    # os.rename(filename, backup_filename)
    with open(filename, "w", encoding="utf-8") as out_file:
        out_file.writelines(output_lines)

    # print(f"Processed and updated {filename}. Backup saved as {backup_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_directory_or_file>")
    else:
        input_path = sys.argv[1]
        
        if os.path.isdir(input_path):
            # If it's a directory, loop through all .md files
            for root, dirs, files in os.walk(input_path):
                for file in files:
                    if file.endswith(".md"):
                        file_path = os.path.join(root, file)
                        print(f"Processing {file_path}...")
                        process_markdown(file_path)
        elif os.path.isfile(input_path) and input_path.endswith(".md"):
            # If it's a single .md file, process it directly
            process_markdown(input_path)
        else:
            print("Error: Please provide a valid .md file or directory containing .md files.")
