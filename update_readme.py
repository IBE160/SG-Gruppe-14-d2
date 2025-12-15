import re
import os
import datetime

def update_readme(file_path="README.md"):
    """
    Updates the README.md file with the current date and time,
    and checks for new files in the 'docs' directory to list them.
    """
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Read the existing README.md content
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return

    # Update the "Last Updated" section
    content = re.sub(
        r"(<!-- LAST_UPDATED_START -->)(.*?)(<!-- LAST_UPDATED_END -->)",
        f"<!-- LAST_UPDATED_START -->\nLast Updated: {current_date}\n<!-- LAST_UPDATED_END -->",
        content,
        flags=re.DOTALL
    )

    # Check for new files in the 'docs' directory
    docs_path = "docs"
    new_files_list = []
    if os.path.exists(docs_path) and os.path.isdir(docs_path):
        for root, _, files in os.walk(docs_path):
            for file in files:
                # Add a simple check to exclude common non-document files or hidden files
                if not file.startswith('.') and not file.endswith(('.DS_Store', '.gitkeep')):
                    relative_path = os.path.relpath(os.path.join(root, file), docs_path)
                    # Replace backslashes with forward slashes for Markdown compatibility
                    markdown_path = relative_path.replace("\\", "/")
                    new_files_list.append(f"- [{markdown_path}](docs/{markdown_path})")
    
    # Update the "New Files Added" section
    if new_files_list:
        new_files_content = "\n".join(sorted(new_files_list))
        content = re.sub(
            r"(<!-- NEW_FILES_START -->)(.*?)(<!-- NEW_FILES_END -->)",
            f"<!-- NEW_FILES_START -->\n{new_files_content}\n<!-- NEW_FILES_END -->",
            content,
            flags=re.DOTALL
        )
    else:
        # If no new files, ensure the section is still present but empty or with a message
        content = re.sub(
            r"(<!-- NEW_FILES_START -->)(.*?)(<!-- NEW_FILES_END -->)",
            f"<!-- NEW_FILES_START -->\nNo new files added recently.\n<!-- NEW_FILES_END -->",
            content,
            flags=re.DOTALL
        )

    # Write the updated content back to README.md
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"{file_path} updated successfully.")
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")

if __name__ == "__main__":
    update_readme()
