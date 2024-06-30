import unittest
from htmlnode import HTMLNode,LeafNode,ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_prop(self):
        htmlnode = HTMLNode('a','test','span',{"href":"https://www.google.com", "target":"_blank"})
        self.assertEqual(" href=\"https://www.google.com\" target=\"_blank\"",htmlnode.props_to_html())
    def test_repr(self):
        htmlnode = HTMLNode('a',"test","span",{"href":"https://www.google.com","target":"_blank"})
        self.assertEqual("HTMLNode(a,test,span,{'href': 'https://www.google.com', 'target': '_blank'})",repr(htmlnode))

    def test_leaf(self):
        leafnode = LeafNode('a',"click link here.",{"href":"https://www.boot.dev"})
        self.assertEqual(leafnode.to_html(),"<a href=\"https://www.boot.dev\">click link here.</a>")

    def test_leaf_notag(self):
        leafnode = LeafNode(None,"just raw text")
        self.assertEqual(leafnode.to_html(),"just raw text")

    def test_leaf_repr(self):
        leafnode = LeafNode('a',"click link here.",{"href":"https://www.boot.dev"})
        self.assertEqual(repr(leafnode),"LeafNode(a,click link here.,{'href': 'https://www.boot.dev'})")

    def test_parent(self):

        parentnode1 = node = ParentNode("p",
        [  
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],)

        parentnode2 = ParentNode("div",[parentnode1,LeafNode('p',"paragraph text")])

        expected = "<div><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><p>paragraph text</p></div>"
        result = parentnode2.to_html()

        self.assertEqual(expected,result)

    
                                 


