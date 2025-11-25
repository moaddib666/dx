import json
import os

# Define the source and destination directories
source_dir = "./"  # Change this to your specific source directory
dist_dir = "./dist"

excluded = [
    "./test",
    "./dx-frontend",
    "./dx_backend",
    "./dx_mobile",
    "./infra",
    "./dx_mcp",
    "./map",
    "./.claude",
    "./.idea",
]

# Supported file extensions for merging
supported_extensions = [".txt", ".json", ".md"]

# Create the dist directory if it doesn't exist
if not os.path.exists(dist_dir):
    os.makedirs(dist_dir)

# Initialize a dictionary to hold file contents by subfolder
folder_contents = {}

# Iterate over files in the source directory
for root, dirs, files in os.walk(source_dir):
    # Skip the dist directory
    if dist_dir in root:
        continue
    if any(i in root for i in excluded):
        continue

    for file in files:
        file_path = os.path.join(root, file)
        file_ext = os.path.splitext(file)[1].lower()

        if file_ext in supported_extensions:
            # Get relative path from source_dir and use it as folder key
            rel_path = os.path.relpath(root, source_dir)

            # Use the relative path as folder name, replacing / with _
            # This preserves directory structure in output file names
            if rel_path == ".":
                folder = "root"
            else:
                folder = rel_path.replace("/", "_").replace("\\", "_")

            if folder not in folder_contents:
                folder_contents[folder] = []

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                    # Pretty-print JSON files
                    if file_ext == ".json":
                        try:
                            loaded_content = json.loads(content)
                            content = json.dumps(loaded_content, indent=4)
                        except Exception as e:
                            print(f"Failed to parse JSON from {file_path}: {e}")

                # Create header with full relative path for context
                header = f"File: {os.path.join(rel_path, file)}\n{'=' * 60}\n"
                folder_contents[folder].append(header + content + "\n\n")

            except Exception as e:
                print(f"Failed to read {file_path}: {e}")

# Write the merged content to the output files in the dist directory
for folder, contents in folder_contents.items():
    output_file_path = os.path.join(dist_dir, f"{folder}_merged.txt")
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.writelines(contents)
    print(f"Merged content for folder '{folder}' has been saved to {output_file_path}")

print(f"\nTotal folders processed: {len(folder_contents)}")
print(f"Supported file extensions: {', '.join(supported_extensions)}")
