from textnode import TextNode, TextType
from file_generation import copy_static, generate_page, generate_pages_recursive
import sys

def main():
    basepath = ""
    if len(sys.argv) == 1:
        basepath = "/"
    else:
        basepath = sys.argv[1].strip() + "/"

    testNode = TextNode("This is some anchor text", TextType["LINK"], "https://www.boot.dev")
    copy_static()
    generate_pages_recursive("content/", "template.html", "docs/", basepath)

if __name__ == "__main__":
    main()
    
