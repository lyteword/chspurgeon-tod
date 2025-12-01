import os
import re

def clean_markdown_files(root_dir):
    # Regex to collapse multiple spaces into a single space
    multi_space_re = re.compile(r' {2,}')

    for folder, subfolders, files in os.walk(root_dir):
        for filename in files:
            if filename.lower().endswith(".md"):
                file_path = os.path.join(folder, filename)

                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Step 1: Replace &nbsp; with a real space
                content = content.replace("&nbsp;", " ")

                # Step 2: Replace multiple spaces with a single space
                content = multi_space_re.sub(" ", content)

                # Write cleaned content back to file
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)

                print(f"Cleaned: {file_path}")

if __name__ == "__main__":
    directory = input("Enter directory path: ").strip()
    clean_markdown_files(directory)

