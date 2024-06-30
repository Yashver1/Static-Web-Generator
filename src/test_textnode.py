import unittest
from textnode import TextNode
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("this is a text node","bold")
        node2 = TextNode("this is a text node","bold")
        self.assertEqual(node,node2)
    def test_url(self):
        node = TextNode("this is a text node","bold")
        self.assertEqual(None,node.url)
        node2 = TextNode("this is a text node","bold", "http://www.boot.dev")
        self.assertEqual("http://www.boot.dev",node2.url)
    def test_uneq_text_type(self):
        node = TextNode("this is a text node","Italic")
        node2 = TextNode("this is a text node","bold")
        self.assertNotEqual(node,node2)
    def test_repr(self):
        node = TextNode("this is a text node","bold")
        self.assertEqual("TextNode(this is a text node,bold,None)",repr(node))
    def test_text_to_html(self):
        node=TextNode("this is a text node","Italic")
        leafnode=LeafNode('i',"this is a text node")
        self.assertEqual(node.text_node_to_html_node(),leafnode)
    def test_text_to_html_2(self):
        node=TextNode("alt-text","Image","http://www.dummy-image.com")
        leafnode=LeafNode("img","",{"src":"http://www.dummy-image.com","alt":"alt-text"})
        self.assertEqual(node.text_node_to_html_node(),leafnode)


if __name__  == "__main__":
    unittest.main()
