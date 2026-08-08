
from textnode import TextNode, TextType, text_node_to_html_node
from extract_markdown import extract_markdown_images, extract_markdown_links
from enum import Enum
from htmlnode import LeafNode, ParentNode
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    split_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            split_nodes.append(node)
            continue
        
        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise ValueError(node.text, " has invalid MarkDown syntax.")
        for i in range(len(split_text)):
            if len(split_text[i]) == 0:
                continue
            if i % 2 == 0:
                tt = TextType.TEXT
            else:
                tt = text_type
            split_nodes.append(TextNode(split_text[i], tt))
    return split_nodes
    
def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    result_nodes = []
    
    if len(old_nodes) == 0:
        return result_nodes
    
    for node in old_nodes:
        if len(node.text) == 0:
            continue
        if node.text_type != TextType.TEXT:
            result_nodes.append(node)
            continue
        
        
        images = extract_markdown_images(node.text)
        #If there are no images in this node, just add the node
        if len(images) == 0:
            result_nodes.append(node)
            continue
        
        #There are images to extract in this text (possible duplicates)
        remainingText = node.text
        for tup in images:
            curDelim = "![" + tup[0] + "](" + tup[1] + ")"
            daSplit = remainingText.split(curDelim, 1)
            
            if daSplit[0] != "":
                result_nodes.append(TextNode(daSplit[0], TextType.TEXT))
            result_nodes.append(TextNode(tup[0], TextType.IMAGE, tup[1]))
            remainingText = daSplit[1]
        
        if remainingText != "":
            result_nodes.append(TextNode(remainingText, TextType.TEXT))

    return result_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    result_nodes = []
    
    if len(old_nodes) == 0:
        return result_nodes
    
    for node in old_nodes:
        if len(node.text) == 0:
            continue
        if node.text_type != TextType.TEXT:
            result_nodes.append(node)
            continue
        
        
        links = extract_markdown_links(node.text)
        #If there are no images in this node, just add the node
        if len(links) == 0:
            result_nodes.append(node)
            continue
        
        #There are images to extract in this text (possible duplicates)
        remainingText = node.text
        for tup in links:
            curDelim = "[" + tup[0] + "](" + tup[1] + ")"
            daSplit = remainingText.split(curDelim, 1)
            
            if daSplit[0] != "":
                result_nodes.append(TextNode(daSplit[0], TextType.TEXT))
            result_nodes.append(TextNode(tup[0], TextType.LINK, tup[1]))
            remainingText = daSplit[1]
        
        if remainingText != "":
            result_nodes.append(TextNode(remainingText, TextType.TEXT))
        
    return result_nodes
    
def text_to_textnodes(text):
    tn = TextNode(text, TextType.TEXT)
    tnlist = split_nodes_delimiter([tn], "**", TextType.BOLD)
    tnlist = split_nodes_delimiter(tnlist, "_", TextType.ITALIC)
    tnlist = split_nodes_delimiter(tnlist, "`", TextType.CODE)
    tnlist = split_nodes_image(tnlist)
    tnlist = split_nodes_link(tnlist)
    return tnlist

def markdown_to_blocks(text):
    lst = text.split("\n\n")
    blocks = []
    for i in range(len(lst)):
        lst[i] = lst[i].strip()
        if len(lst[i]) > 0:
            blocks.append(lst[i])
    return blocks

def block_to_block_type(block):
    if re.match("^#{1,6} .+", block) is not None:
        return BlockType.HEADING
    if re.match(re.compile("^```\n.*```$",re.DOTALL), block) is not None:
        return BlockType.CODE
    lines = block.split("\n")
    cond = True
    for line in lines:
        if re.match(r"^>", line) is None:
            cond = False
            break
    if cond == True and len(lines) > 0:
        
        return BlockType.QUOTE
    
    cond = True
    for line in lines:
        if re.match(r"^- ", line) is None:
            cond = False
            break
    
    if cond == True:
        return BlockType.UNORDERED_LIST
    
    cond = True
    
    n = 1
    for line in lines:
        if re.match(r"^\d+\. ", line) is None or int(line.split(".")[0]) != n:
            cond = False
            break
        else:
            n += 1
    if cond == True:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    children = []
    for block in blocks:
        btype = block_to_block_type(block)
        node = block_to_node(block, btype)
        children.append(node)
    return ParentNode("div", children)

def block_to_node(block, block_type):
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_node(block)
        case BlockType.HEADING:
            return heading_to_node(block)
        case BlockType.CODE:
            return code_to_node(block)
        case BlockType.QUOTE:
            return quote_to_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_node(block)

def text_nodes_to_html_nodes(nodes):
    for ind in range(len(nodes)):
        nodes[ind] = text_node_to_html_node(nodes[ind])
    return nodes

def paragraph_to_node(block):
    lines = block.split("\n")
    for ind in range(len(lines)):
        lines[ind] = lines[ind].strip()
    block = " ".join(lines)

    nodes = text_nodes_to_html_nodes(text_to_textnodes(block))
    return ParentNode("p", nodes)
    
def heading_to_node(block):
    i = 0
    while block[i] == "#":
        i += 1
    block = block[i+1:]
    tn = text_to_textnodes(block)
    nodes = text_nodes_to_html_nodes(tn)
    return ParentNode("h" + str(i), nodes)
    
def code_to_node(block):
    block = block[4:-3]
    code_node = LeafNode("code", block)
    return ParentNode("pre", [code_node])

def quote_to_node(block):
    items = block.split("\n")
    for ind in range(len(items)):
        items[ind] = items[ind][1:].lstrip()
    
    children = text_nodes_to_html_nodes(text_to_textnodes(" ".join(items)))
    return ParentNode("blockquote", children)

def unordered_list_to_node(block):
    items = block.split("\n")
    for ind in range(len(items)):
        items[ind] = items[ind][2:]
    
    children = []
    for item in items:
        children.append(ParentNode("li", text_nodes_to_html_nodes(text_to_textnodes(item))))
        
    return ParentNode("ul", children)

def ordered_list_to_node(block):
    items = block.split("\n")
    for ind in range(len(items)):
        items[ind] = items[ind].split(". ", 1)[1]
    
    children = []
    for item in items:
        children.append(ParentNode("li", text_nodes_to_html_nodes(text_to_textnodes(item))))
        
    return ParentNode("ol", children)