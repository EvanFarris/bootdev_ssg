import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestTextNode(unittest.TestCase):
    def test_no_props(self):
        node = HTMLNode("p")
       
        self.assertEqual("", node.props_to_html())
   
    def test_one_props(self):
        node = HTMLNode("p", props={"href": "https://google.com"})
        
        self.assertEqual(" href=\"https://google.com\"", node.props_to_html())
        
    def test_two_props(self):
        node = HTMLNode("p", props={"href": "https://google.com", "target": "_blank"})
        
        self.assertEqual(" href=\"https://google.com\" target=\"_blank\"", node.props_to_html())
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_p(self):
        node = LeafNode("a", "Click me!", props={"href": "https://google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://google.com\">Click me!</a>")
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
if __name__ == "__main__":
    unittest.main()