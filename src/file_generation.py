import os
import shutil
import re
from split_nodes import markdown_to_html_node

def copy_static():
    print(os.getcwd())
    if os.path.exists("./public"):
        shutil.rmtree("./public")
        shutil.copytree("./static","./public")

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        m = re.search("^# ", markdown)
        if m is not None:
            return line[2:].strip()
    raise ValueError("No h1 found")

def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r") as f:
        from_content = f.read()
    with open(template_path, "r") as f:
        template_content = f.read()
    
    
    htmlstr = markdown_to_html_node(from_content).to_html()

    title = extract_title(from_content)
    test1 = f"href=\"{basepath}"
    test2 = f"src=\"{basepath}"
    print(test1)
    print(test2)
    result = template_content.replace("{{ Title }}", title)
    result = result.replace("{{ Content }}", htmlstr)
    #result = result.replace("href=\"/", test1)
    #result = result.replace("src=\"/", test2)
    pathonly = dest_path.split("/")
    pathonly = pathonly[:-1]
    pathonly = "/".join(pathonly)
    
    os.makedirs(pathonly, exist_ok=True)
    
    with open(dest_path, "w") as f:
        f.write(result)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath = "/"):
    for obj in os.listdir(dir_path_content):
        obj_dir_path = os.path.join(dir_path_content, obj)
        
        if os.path.isfile(obj_dir_path):
            obj_dest_path = os.path.join(dest_dir_path, obj[:-2] + "html")
            generate_page(obj_dir_path, template_path, obj_dest_path, basepath)
        else:
            obj_dest_path = os.path.join(dest_dir_path, obj)
            generate_pages_recursive(obj_dir_path, template_path, obj_dest_path, basepath)