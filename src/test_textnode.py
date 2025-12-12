import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()
