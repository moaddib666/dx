import os
import json

# Define the source and destination directories
source_dir = "./"  # Change this to your specific source directory
dist_dir = "./dist"

excluded = ["./test", "./dx-frontend", "./dx_backend", "./dx_mobile", "./infra"]
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
        if file_ext in [".txt", ".json"]:
            folder = os.path.basename(root)
            if folder not in folder_contents:
                folder_contents[folder] = []

            with open(file_path, "r") as f:
                content = f.read()
                if file_ext == ".json":
                    try:
                        loaded_content = json.loads(content)
                        content = json.dumps(loaded_content, indent=4)
                    except:
                        print("fail to get content from json", file_path)


            header = f"File: {file}\n{'=' * 20}\n"
            folder_contents[folder].append(header + content + "\n")

# Write the merged content to the output files in the dist directory
for folder, contents in folder_contents.items():
    output_file_path = os.path.join(dist_dir, f"{folder}_merged.txt")
    with open(output_file_path, "w") as output_file:
        output_file.writelines(contents)
    print(f"Merged content for folder '{folder}' has been saved to {output_file_path}")
