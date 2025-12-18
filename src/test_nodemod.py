import unittest

from node_mods import extract_markdown_images, extract_markdown_links, split_nodes_delimiter
from textnode import TextNode


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
        node = TextNode("This is text with a `code block` word")
        new_nodes = split_nodes_delimiter([node], "`")
        expected = [["This is text with a "], ["code block"], [" word"]]
        self.assertEqual(expected, new_nodes)

    def test_split_multiple_delimiters(self):
        node = TextNode("Text with **bold** and **more bold**")
        new_nodes = split_nodes_delimiter([node], "**")
        expected = [["Text with "], ["bold"], [" and "], ["more bold"], [""]]
        self.assertEqual(expected, new_nodes)

    def test_split_no_delimiter(self):
        node = TextNode("Plain text without delimiters")
        new_nodes = split_nodes_delimiter([node], "`")
        expected = [["Plain text without delimiters"]]
        self.assertEqual(expected, new_nodes)

    def test_split_delimiter_at_start(self):
        node = TextNode("**bold** text after")
        new_nodes = split_nodes_delimiter([node], "**")
        expected = [[""], ["bold"], [" text after"]]
        self.assertEqual(expected, new_nodes)

    def test_split_delimiter_at_end(self):
        node = TextNode("text before **bold**")
        new_nodes = split_nodes_delimiter([node], "**")
        expected = [["text before "], ["bold"], [""]]
        self.assertEqual(expected, new_nodes)

    def test_split_multiple_nodes(self):
        node1 = TextNode("First `code` text")
        node2 = TextNode("Second `code` text")
        new_nodes = split_nodes_delimiter([node1, node2], "`")
        expected = [["First "], ["code"], [" text"], ["Second "], ["code"], [" text"]]
        self.assertEqual(expected, new_nodes)

    def test_split_empty_between_delimiters(self):
        node = TextNode("text****text")
        new_nodes = split_nodes_delimiter([node], "**")
        expected = [["text"], [""], ["text"]]
        self.assertEqual(expected, new_nodes)


if __name__ == "__main__":
    unittest.main()
