from textnode import TextNode, TextType
from file_generation import copy_static, generate_page, generate_pages_recursive


def main():
    testNode = TextNode("This is some anchor text", TextType["LINK"], "https://www.boot.dev")
    copy_static()
    generate_pages_recursive("content/", "template.html", "public/")
    #generate_page("content/index.md", "template.html", "public/index.html")
    #generate_page("content/blog/glorfindel/index.md", "template.html", "public/blog/glorfindel/index.html")
    #generate_page("content/blog/tom/index.md", "template.html", "public/blog/tom/index.html")
    #generate_page("content/blog/majesty/index.md", "template.html", "public/blog/majesty/index.html")
    #generate_page("content/contact/index.md", "template.html", "public/contact/index.html")
if __name__ == "__main__":
    main()
    
