import os
import shutil
import re


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


def main():
    copy_to("static", "public")


if __name__ == "__main__":
    main()
