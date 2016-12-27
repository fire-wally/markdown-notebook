#!/usr/local/bin/python3
import sys
import os
import shutil
import markdown

class Page(object):
    def __init__(self, filename, mtime):
        self.file_name = filename
        self.modified_at = mtime

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
    files_written=[]
    print("Creating .html Files in Output Directory")
    for root, dirs, files in os.walk(source):
        for name in files:
            print(os.path.join(dest,name))
            ##Transform Markdown files to HTML. Copy all other files as-is
            if (name.endswith(".md")):
                file_path = os.path.join(root, name)
                new_file_name = generate_markdown(file_path, dest)
                new_file = Page(new_file_name, os.path.getmtime(file_path))
                files_written.append(new_file)
            else:
                shutil.copy(os.path.join(root, name), dest)
        for name in dirs:
            os.mkdir(os.path.join(dest, name))
    #Now generate the index file
    generate_index(files_written, dest)

def generate_index(files, dest_dir):
    html = generate_index_html(files)
    index_path = os.path.join(dest_dir, "index.html")
    with open(index_path, "w+") as opened_file:
        opened_file.write(html)


def generate_markdown(source_file, dest_dir):
    '''generates a new html file in the dest directory, returns the name of the 
    newly-created file'''

    md = ""
    with open(source_file, 'r') as opened_file:
        md = opened_file.read()
    html = content_to_html(md)
    new_name = os.path.split(source_file)[1].replace("md", "html")
    new_path = os.path.join(dest_dir, new_name)
    with open(new_path, "w+") as opened_file:
        opened_file.write(html)
    return new_name

def generate_index_html(pages):
    with open("index-template.html") as template_file:
        html_template = template_file.read()
    alpha_page_list = "<ul>"
    for page in pages:
        alpha_page_list += "\n<li><a href='http://localhost/notes/{0}'>{0}</a></li>".format(page.file_name)
    alpha_page_list += '\n</ul>'

    recent_page_list = "<ul>"
    for page in sorted(pages, key=lambda p: p.modified_at, reverse=True):
        recent_page_list += "\n<li><a href='http://localhost/notes/{0}'>{0}</a></li>".format(page.file_name)
    recent_page_list += "</ul>"
    html_page = html_template.replace("{{PAGE_LIST_RECENT}}", recent_page_list) \
                             .replace("{{PAGE_LIST_ALPHA}}", alpha_page_list)


    return html_page


def content_to_html(source_string):
    with open("page-template.html") as template_file: #Assume in same directory as code
        html_template = template_file.read()
    page_fragment = markdown.markdown(source_string)
    html_page = html_template.replace("{{PAGE_GOES_HERE}}", page_fragment)
    return html_page


if __name__ == "__main__":
    main(sys.argv)