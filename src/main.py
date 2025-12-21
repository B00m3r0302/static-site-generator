import os
import shutil
import re
import sys
from markdown_mod import markdown_to_html_node
from htmlnode import ParentNode


def copy_to(source, destination):
    if not os.path.exists(source):
        raise Exception("Can't find the source directory....not much to do here....")

    if os.path.exists(destination):
        shutil.rmtree(destination)

    os.makedirs(destination)

    # copy contents recursively
    for item in os.listdir(source):
        src_path = os.path.join(source, item)
        dst_path = os.path.join(destination, item)

        if os.path.isdir(src_path):
            copy_to(src_path, dst_path)
        else:
            shutil.copy2(src_path, dst_path)


def extract_title(markdown):
    header = re.match(r"^\# (.*?)$", markdown, re.MULTILINE)
    if not header:
        raise Exception("Couldn't find a header for the markdown file")
    else:
        return header.group(1).strip()


def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f_file:
        from_content = f_file.read()

    with open(template_path, "r") as t_file:
        template_content = t_file.read()

    # convert markdown to html
    html_string = markdown_to_html_node(from_content).to_html()
    title = extract_title(from_content)
    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html_string)

    # replace paths with basepath
    template_content = template_content.replace('href="/', f'href="{basepath}')
    template_content = template_content.replace('src="/', f'src="{basepath}')

    # create parent directories if they don't exist
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as dest_file:
        dest_file.write(template_content)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    for item in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, item)

        if os.path.isdir(src_path):
            # recursively process subdirectories
            dest_subdir = os.path.join(dest_dir_path, item)
            generate_pages_recursive(src_path, template_path, dest_subdir, basepath)
        elif item.endswith('.md'):
            # convert .md extension to .html for destination
            html_filename = item[:-3] + '.html'
            dest_path = os.path.join(dest_dir_path, html_filename)
            generate_page(src_path, template_path, dest_path, basepath)


def main():
    # get basepath from CLI argument, default to /
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    copy_to("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

if __name__ == "__main__":
    main()
