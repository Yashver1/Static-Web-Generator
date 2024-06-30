import unittest
from textnode import TextNode
from htmlnode import *
from helper_functions import *

class Test_Helper_Func(unittest.TestCase):

    def test_split_function(self):
        node = TextNode("this is a **bold** text","text")
        test_node1 = TextNode("this is a ","text")
        test_node2 = TextNode("bold","bold")
        test_node3 = TextNode(" text","text")
        self.assertEqual([test_node1,test_node2,test_node3],split_nodes_delimiter([node],'**',"bold"))


    def test_no_close_delimiter(self):
        node = TextNode("this is a *bold text","text")
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node],'*',"bold")
    def test_repeated_split(self):
        node = TextNode("this is a **bold** text and this is a *italic* text","text")
        test_node1 = TextNode("this is a ","text")
        test_node2 = TextNode("bold","bold")
        test_node3 = TextNode(" text and this is a ","text")
        test_node4 = TextNode("italic","italic")
        test_node5 = TextNode(" text","text")
        self.assertEqual([test_node1,test_node2,test_node3,test_node4,test_node5],split_nodes_delimiter(split_nodes_delimiter([node],"**","bold"),"*","italic"))

    def test_invalid_delimiter(self):
        node = TextNode("this is a &unknown& text","text")
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node],'&',"unkown")

    def test_match_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        self.assertEqual(extract_markdown_image(text),[("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")])

    def test_match_link(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        self.assertEqual(extract_markdown_link(text),[("link", "https://www.example.com"), ("another", "https://www.example.com/another")])

    def test_split_node_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        node = TextNode(text,"text")
        test_node1 = TextNode("This is text with an ","text")
        test_node2 = TextNode("image","image","https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png")
        test_node3 = TextNode(" and ","text")
        test_node4 = TextNode("another","image","https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")
        self.assertEqual(split_nodes_image([node]),[test_node1,test_node2,test_node3,test_node4])

    def test_missing_closing_image(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"
        node = TextNode(text,"text")
        with self.assertRaises(ValueError):
            split_nodes_image([node])

    def test_split_node_links(self):
        text = "This is text with an [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and [another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        node = TextNode(text,"text")
        test_node1 = TextNode("This is text with an ","text")
        test_node2 = TextNode("link","link","https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png")
        test_node3 = TextNode(" and ","text")
        test_node4 = TextNode("another","link","https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")
        self.assertEqual(split_nodes_link([node]),[test_node1,test_node2,test_node3,test_node4])

    def test_missing_closing_link(self):
        text = "This is a text with a [link](fake url"
        node = TextNode(text,"text")
        with self.assertRaises(ValueError):
            split_nodes_link([node])

    def test_complete_markdown(self):
        text = "This is *text* with an **bold** word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        self.assertEqual(text_to_textnodes(text), [
            TextNode("This is ", "text"),
            TextNode("text", "italic"),
            TextNode(" with an ", "text"),
            TextNode("bold", "bold"),
            TextNode(" word and a ", "text"),
            TextNode("code block", "code"),
            TextNode(" and an ", "text"),
            TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", "text"),
            TextNode("link", "link", "https://boot.dev"),
        ])



    def test_split_blocks(self):
        text = '''This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items'''

        expected = ['This is **bolded** paragraph','This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line','* This is a list\n* with items']

        self.assertEqual(markdown_to_blocks(text),expected)


    def test_block_to_block_type(self):
        expected_list = ["quote","heading","ordered_list","unordered_list","code","paragraph"]
        input_list = [">line1\n>line2","## line1\nline2","1. line1\n2. line","- line1\n- line2","```line1\nline2```","line1\nline2"]
        for i in range(len(expected_list)):
            self.assertEqual(expected_list[i],block_to_block_type(input_list[i]))


    
    def test_block_to_nodes(self):
        text = '''* this is a test **heading** element.
* this is the *second* line.'''
        expected = ParentNode("ul",[ParentNode("li",[LeafNode(None,"this is a test ",None), LeafNode("b","heading",None), LeafNode(None," element.",None)],None), ParentNode("li",[LeafNode(None,"this is the ",None), LeafNode("i","second",None), LeafNode(None," line.",None)],None)],None)
        self.assertEqual(expected,block_to_nodes(text))

    def test_markdown_to_htmlnodes(self):

        text = '''##### this is a test **heading** block.
this is the *second* line.

>this is a **quote** block.
>this is the *second* line.

```print("this is a code block.)"
print('test')```

* this is one line.
* this is another line.

1. this is the first line.
2. this is the second line.

this is a normal para.
test test.'''
        
        test = markdown_to_htmlnodes(text)
        print(test.to_html())
        
