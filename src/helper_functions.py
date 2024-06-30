from textnode import TextNode
from htmlnode import ParentNode
import re
import os
from pathlib import Path

valid_delimiters = ['*','**','`']

# Inline Markdown
def split_nodes_delimiter(old_nodes,delimiter,text_type):
    split_nodes = []

    if delimiter not in valid_delimiters:
        raise ValueError("Invalid delimiter")

    for node in old_nodes:
        node_list = []
        old_text = node.text
        old_type = node.text_type
        text_list = old_text.split(delimiter)

        if len(text_list)%2==0:
            raise ValueError("Missing end delimiter")
        
        for i in range(len(text_list)):
            if text_list[i] == "":
                continue
            elif i%2==1:
                node_list.append(TextNode(text_list[i],text_type))
            else:
                node_list.append(TextNode(text_list[i],old_type))
        
        split_nodes.extend(node_list)

     
    return split_nodes

def extract_markdown_image(text):
    #test_match = re.findall(r"!\[(?![^\]]*\])",text)
    #test_match2 = re.findall(r"\((?![^)]*\))",text)
    #if test_match or test_match2:
    #        raise ValueError("Missing closing link bracket")

    match = re.findall(r"!\[(.*?)\]\((.*?)\)",text)
    return match

def extract_markdown_link(text):
   # test_match = re.findall(r"\[(?![^\]]*\])",text)
   # test_match2 = re.findall(r"\((?![^)]*\))",text)
   # if test_match or test_match2:
   #         raise ValueError("Missing closing link bracket")
    match = re.findall(r"\[(.*?)\]\((.*?)\)",text)
    return match

def split_nodes_image(old_nodes):
    nodes_list = []
    for node in old_nodes:
        old_text = node.text
        old_type = node.text_type
        text_list = extract_markdown_image(old_text)
        if not text_list:
            nodes_list.append(node)
        else:
            for link in text_list:
                sections = old_text.split(f"![{link[0]}]({link[1]})",1)
                if sections[0] != "":
                    nodes_list.append(TextNode(sections[0],old_type))
                nodes_list.append(TextNode(link[0],"image",link[1]))
                old_text = sections[1]
            if old_text != "":
                nodes_list.append(TextNode(old_text,old_type))
    return nodes_list

def split_nodes_link(old_nodes):
    nodes_list = []
    for node in old_nodes:
        old_text = node.text
        old_type = node.text_type
        text_list = extract_markdown_link(old_text)
        if not text_list:
            nodes_list.append(node)
        else:
            for link in text_list:
                sections = old_text.split(f"[{link[0]}]({link[1]})",1)
                if sections[0] != "":
                    nodes_list.append(TextNode(sections[0],old_type))
                nodes_list.append(TextNode(link[0],"link",link[1]))
                old_text = sections[1]
            if old_text != "":
                nodes_list.append(TextNode(old_text,old_type))
    return nodes_list


def text_to_textnodes(text):
    split_nodes = []
    node = TextNode(text,"text")
    split_nodes.extend(split_nodes_link(split_nodes_image(split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter([node],'`',"code"),'**',"bold"),'*',"italic"))))

    return split_nodes

def text_to_htmlnodes(text):
    split_nodes = text_to_textnodes(text)
    leaf_nodes = []
    for node in split_nodes:
        leaf_nodes.append(node.text_node_to_html_node())
    return leaf_nodes






# Block Markdown

def markdown_to_blocks(markdown):
    result = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        if block == "":
            continue
        result.append(block.strip())
    return result




def block_to_block_type(block):
    lines = block.split('\n')
    if block.startswith("# ") or block.startswith("## ") or block.startswith("### ") or block.startswith("#### ") or block.startswith("##### ") or block.startswith("###### "):
        return "heading"
    
    elif block.startswith("```") and block.endswith("```"):
        return "code"

    elif block.startswith(">"):
        for line in lines:
            if  not line.startswith(">"):
                return "paragraph"
        return "quote"

    elif block.startswith('* '):
        for line in lines:
            if not line.startswith('* '):
                return "paragraph"
        return "unordered_list"
    
    elif block.startswith('- '):
        for line in lines:
            if not line.startswith('- '):
                return "paragraph"
        return "unordered_list"
    elif block.startswith('1. '):
        next = 1
        for line in lines:
            if not line.startswith(f"{next}. "):
                return "paragraph"
            next+=1
        return "ordered_list"
    else:
        return "paragraph"

    


def heading_to_node(block,block_type):
    if block_type != "heading":
        raise ValueError("Invalid block type")
    tag_number = 0
    for char in block:
        if char == "#":
            tag_number +=1
            continue
        break
    block = block.replace('\n','<br>')
    children_nodes = text_to_htmlnodes(block[tag_number+1:])
    return ParentNode(f"h{tag_number}",children_nodes)

def code_to_node(block,block_type):
    if block_type != "code":
        raise ValueError("Invalid block type")
    block = block.replace('\n','<br>')
    block_text = block.strip("```")
    children_nodes = text_to_htmlnodes(block_text)
    code_node = ParentNode("code",children_nodes)
    return ParentNode("pre",[code_node])

def quote_to_node(block,block_type):
    if block_type != "quote":
        raise ValueError("Invalid block type")
    block = block.replace('>','')
    block = block.replace('\n','<br>') # must be after > or br tag will be removed
    children_nodes = text_to_htmlnodes(block) 
    return ParentNode("blockquote",children_nodes)

def ul_to_node(block,block_type):
    if block_type != "unordered_list":
        raise ValueError("Invalid block type")
    lines = block.split('\n')
    list_nodes = []
    for line in lines:
        children_nodes = text_to_htmlnodes(line[2:]) # remove '* '
        list_nodes.append(ParentNode("li",children_nodes))

    return ParentNode("ul",list_nodes)

def ol_to_node(block,block_type):
    if block_type != "ordered_list":
        raise ValueError("Invalid block type")
    lines = block.split('\n')
    list_nodes = []
    for line in lines:
        children_nodes = text_to_htmlnodes(line[3:]) # remove '1. '
        list_nodes.append(ParentNode("li",children_nodes))

    return ParentNode("ol",list_nodes)

def para_to_node(block,block_type):
    if block_type != "paragraph":
        raise ValueError("Invalid block type")
    block = block.replace('\n','<br>')
    children_nodes = text_to_htmlnodes(block)
    return ParentNode("p",children_nodes)

def block_to_nodes(block):
    block_type = block_to_block_type(block)

    match block_type:
        case "heading":
            return heading_to_node(block,"heading")
        case "code":
            return code_to_node(block,"code")
        case "quote":
            return quote_to_node(block,"quote")
        case "unordered_list":
            return ul_to_node(block,"unordered_list")
        case "ordered_list":
            return ol_to_node(block,"ordered_list")
        case "paragraph":
            return para_to_node(block,"paragraph")

def markdown_to_htmlnodes(text):
    blocks = markdown_to_blocks(text)
    block_nodes = []
    for block in blocks:
        parent_node = block_to_nodes(block)
        block_nodes.append(parent_node)
    return ParentNode("div",block_nodes)

    
def extract_title(markdown):
    lines = markdown.split("\n\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("No title found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path,'r') as file:
        content = file.read()
    title = extract_title(content)

    with open(template_path,'r') as file:
        template = file.read()
    template =  template.replace("{{ Title }}",title)
    htmlnodes = markdown_to_htmlnodes(content)
    content_html = htmlnodes.to_html()
    template = template.replace("{{ Content }}",content_html)

    dest_dir = os.path.dirname(dest_path)
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)
    with open(dest_path,'w') as file:
        file.write(template)


def generate_pages_recursive(dir_path_content,template_path,dest_dir_path):
    src_list = os.listdir(dir_path_content)

    for src in src_list:
        
        abs_src_dir = os.path.join(dir_path_content,src)
        if os.path.isfile(abs_src_dir):
            path = Path(src)
            new_src = path.with_suffix(".html")
            abs_dest_dir = os.path.join(dest_dir_path,new_src)
            generate_page(abs_src_dir,template_path,abs_dest_dir)
        elif os.path.isdir(abs_src_dir):
            abs_dest_dir = os.path.join(dest_dir_path,src)
            generate_pages_recursive(abs_src_dir,template_path,abs_dest_dir)









    


    
   










