import unittest

from node_mods import extract_markdown_images, extract_markdown_links, split_nodes_delimiter
from textnode import TextNode, TextType


class test_extract_markdown_images(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_fail_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertNotEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_other_text_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is some hahahahaha ![haha](https://yousuck.yourmom.com/suck-it-nerd)"
        )
        self.assertListEqual(
            [("haha", "https://yousuck.yourmom.com/suck-it-nerd")], matches
        )


class test_extract_markdown_links(unittest.TestCase):
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_fail_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a malformed [link]https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertNotEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_other_text_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is some hahahahahahah [haha](https://yousuck.yourmom.com/suck-it-nerd)"
        )
        self.assertListEqual(
            [("haha", "https://yousuck.yourmom.com/suck-it-nerd")], matches
        )


class test_split_nodes_delimiter(unittest.TestCase):
    def test_split_single_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.plain)
        new_nodes = split_nodes_delimiter([node], "`", TextType.code)
        expected = [
            TextNode("This is text with a ", TextType.plain),
            TextNode("code block", TextType.code),
            TextNode(" word", TextType.plain)
        ]
        self.assertEqual(expected, new_nodes)

    def test_split_multiple_delimiters(self):
        node = TextNode("Text with **bold** and **more bold**", TextType.plain)
        new_nodes = split_nodes_delimiter([node], "**", TextType.bold)
        expected = [
            TextNode("Text with ", TextType.plain),
            TextNode("bold", TextType.bold),
            TextNode(" and ", TextType.plain),
            TextNode("more bold", TextType.bold)
        ]
        self.assertEqual(expected, new_nodes)

    def test_split_no_delimiter(self):
        node = TextNode("Plain text without delimiters", TextType.plain)
        new_nodes = split_nodes_delimiter([node], "`", TextType.code)
        expected = [TextNode("Plain text without delimiters", TextType.plain)]
        self.assertEqual(expected, new_nodes)

    def test_split_delimiter_at_start(self):
        node = TextNode("**bold** text after", TextType.plain)
        new_nodes = split_nodes_delimiter([node], "**", TextType.bold)
        expected = [
            TextNode("bold", TextType.bold),
            TextNode(" text after", TextType.plain)
        ]
        self.assertEqual(expected, new_nodes)

    def test_split_delimiter_at_end(self):
        node = TextNode("text before **bold**", TextType.plain)
        new_nodes = split_nodes_delimiter([node], "**", TextType.bold)
        expected = [
            TextNode("text before ", TextType.plain),
            TextNode("bold", TextType.bold)
        ]
        self.assertEqual(expected, new_nodes)

    def test_split_multiple_nodes(self):
        node1 = TextNode("First `code` text", TextType.plain)
        node2 = TextNode("Second `code` text", TextType.plain)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.code)
        expected = [
            TextNode("First ", TextType.plain),
            TextNode("code", TextType.code),
            TextNode(" text", TextType.plain),
            TextNode("Second ", TextType.plain),
            TextNode("code", TextType.code),
            TextNode(" text", TextType.plain)
        ]
        self.assertEqual(expected, new_nodes)

    def test_split_empty_between_delimiters(self):
        node = TextNode("text****text", TextType.plain)
        new_nodes = split_nodes_delimiter([node], "**", TextType.bold)
        expected = [
            TextNode("text", TextType.plain),
            TextNode("text", TextType.plain)
        ]
        self.assertEqual(expected, new_nodes)


if __name__ == "__main__":
    unittest.main()
