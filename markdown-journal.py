#!/usr/local/bin/python3
import sys
import os
import shutil
import markdown

def main(argv):
    if len(argv) != 3:
        print("USAGE: markdown-journal.py source-dir output-dir")
        return
    source = argv[1]
    dest = argv[2]
    if not (os.path.isdir(source)):
        print(source+ " is not a directory!")
        return
    if not (os.path.isdir(dest)):
        print(dest + " is not a directory!")
        return
    print("Source directory is " + argv[1])
    print("Output directory is " + argv[2])
    clean_output(dest)
    generate_output(source, dest)

def clean_output(dest):
    print("Cleaning Output Directory")
    for root, dirs, files in os.walk(dest, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))



def generate_output(source, dest):
    print("Creating .html Files in Output Directory")
    for root, dirs, files in os.walk(source):
        for name in files:
            ##Transform Markdown files to HTML. Copy all other files as-is
            if (name.endswith(".md")):
                generate_markdown(os.path.join(root, name), dest)
            else:
                shutil.copy(os.path.join(root, name), dest)
        for name in dirs:
            os.mkdir(os.path.join(dest, name))

def generate_markdown(source_file, dest_dir):
    md = ""
    with open(source_file, 'r') as opened_file:
        md = opened_file.read()
    html = content_to_html(md)
    new_path = os.path.join(dest_dir, os.path.split(source_file)[1].replace("md", "html"))
    with open(new_path, "w+") as opened_file:
        opened_file.write(html)

def content_to_html(source_string):
    with open("template.html") as template_file: #Assume in same directory as code
        html_template = template_file.read()
    page_fragment = markdown.markdown(source_string)
    html_page = html_template.replace("{{PAGE_GOES_HERE}}", page_fragment)
    return html_page


if __name__ == "__main__":
    main(sys.argv)