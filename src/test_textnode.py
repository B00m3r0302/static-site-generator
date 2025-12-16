import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a textnode")
        node2 = TextNode("This is a textnode")
        self.assertEqual(node, node2)

    def test_not_eq_type(self):
        node = TextNode("**haha**")
        node2 = TextNode("__haha__")
        self.assertNotEqual(node, node2)

    def test_missing_url(self):
        node = TextNode("[haha](www.haha.com)")
        node2 = TextNode("[haha]www.haha.com)")
        self.assertNotEqual(node, node2)

    def test_image_link(self):
        node = TextNode("![haha](www.haha.com)")
        node2 = TextNode("[haha](www.haha.com)")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("**bold text**")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold text")

    def test_italic(self):
        node = TextNode("__italic text__")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "italic text")

    def test_code(self):
        node = TextNode("`code block`")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "code block")

    def test_link(self):
        node = TextNode("[click here](https://www.example.com)")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "click here")
        self.assertEqual(html_node.props["href"], "https://www.example.com")

    def test_image(self):
        node = TextNode("![alt text](https://www.example.com/image.png)")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "https://www.example.com/image.png")
        self.assertEqual(html_node.props["alt"], "alt text")


if __name__ == "__main__":
    unittest.main()
