import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a textnode", TextType.plain)
        node2 = TextNode("This is a textnode", TextType.plain)
        self.assertEqual(node, node2)

    def test_not_eq_type(self):
        node = TextNode("haha", TextType.bold)
        node2 = TextNode("haha", TextType.italic)
        self.assertNotEqual(node, node2)

    def test_missing_url(self):
        node = TextNode("haha", TextType.links, "www.haha.com")
        node2 = TextNode("haha", TextType.plain)
        self.assertNotEqual(node, node2)

    def test_image_link(self):
        node = TextNode("haha", TextType.images, "www.haha.com")
        node2 = TextNode("haha", TextType.links, "www.haha.com")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.plain)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("bold text", TextType.bold)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold text")

    def test_italic(self):
        node = TextNode("italic text", TextType.italic)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "italic text")

    def test_code(self):
        node = TextNode("code block", TextType.code)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "code block")

    def test_link(self):
        node = TextNode("click here", TextType.links, "https://www.example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "click here")
        self.assertEqual(html_node.props["href"], "https://www.example.com")

    def test_image(self):
        node = TextNode("alt text", TextType.images, "https://www.example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "https://www.example.com/image.png")
        self.assertEqual(html_node.props["alt"], "alt text")


if __name__ == "__main__":
    unittest.main()
