import unittest

from node_mods import extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
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


class test_split_nodes_image(unittest.TestCase):
    def test_split_single_image(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.plain)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextType.plain),
            TextNode("image", TextType.images, "https://i.imgur.com/zjjcJKZ.png")
        ]
        self.assertEqual(expected, new_nodes)

    def test_split_multiple_images(self):
        node = TextNode("Start ![img1](url1) middle ![img2](url2) end", TextType.plain)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Start ", TextType.plain),
            TextNode("img1", TextType.images, "url1"),
            TextNode(" middle ", TextType.plain),
            TextNode("img2", TextType.images, "url2"),
            TextNode(" end", TextType.plain)
        ]
        self.assertEqual(expected, new_nodes)

    def test_split_image_at_start(self):
        node = TextNode("![image](url) text after", TextType.plain)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("image", TextType.images, "url"),
            TextNode(" text after", TextType.plain)
        ]
        self.assertEqual(expected, new_nodes)

    def test_split_image_at_end(self):
        node = TextNode("text before ![image](url)", TextType.plain)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("text before ", TextType.plain),
            TextNode("image", TextType.images, "url")
        ]
        self.assertEqual(expected, new_nodes)


class test_split_nodes_link(unittest.TestCase):
    def test_split_single_link(self):
        node = TextNode("This is text with a [link](https://example.com)", TextType.plain)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a ", TextType.plain),
            TextNode("link", TextType.links, "https://example.com")
        ]
        self.assertEqual(expected, new_nodes)

    def test_split_multiple_links(self):
        node = TextNode("Start [link1](url1) middle [link2](url2) end", TextType.plain)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Start ", TextType.plain),
            TextNode("link1", TextType.links, "url1"),
            TextNode(" middle ", TextType.plain),
            TextNode("link2", TextType.links, "url2"),
            TextNode(" end", TextType.plain)
        ]
        self.assertEqual(expected, new_nodes)

    def test_split_link_at_start(self):
        node = TextNode("[link](url) text after", TextType.plain)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("link", TextType.links, "url"),
            TextNode(" text after", TextType.plain)
        ]
        self.assertEqual(expected, new_nodes)

    def test_split_link_at_end(self):
        node = TextNode("text before [link](url)", TextType.plain)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("text before ", TextType.plain),
            TextNode("link", TextType.links, "url")
        ]
        self.assertEqual(expected, new_nodes)


class test_text_to_textnodes(unittest.TestCase):
    def test_text_with_all_formatting(self):
        text = "This is **bold** and __italic__ and `code` text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.plain),
            TextNode("bold", TextType.bold),
            TextNode(" and ", TextType.plain),
            TextNode("italic", TextType.italic),
            TextNode(" and ", TextType.plain),
            TextNode("code", TextType.code),
            TextNode(" text", TextType.plain)
        ]
        self.assertEqual(expected, nodes)

    def test_text_with_bold_and_italic(self):
        text = "**bold text** and __italic text__"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("bold text", TextType.bold),
            TextNode(" and ", TextType.plain),
            TextNode("italic text", TextType.italic)
        ]
        self.assertEqual(expected, nodes)

    def test_text_with_link_and_image(self):
        text = "Check [this link](https://example.com) and ![this image](https://example.com/img.png)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Check ", TextType.plain),
            TextNode("this link", TextType.links, "https://example.com"),
            TextNode(" and ", TextType.plain),
            TextNode("this image", TextType.images, "https://example.com/img.png")
        ]
        self.assertEqual(expected, nodes)

    def test_text_with_all_types(self):
        text = "**Bold** __italic__ `code` [link](url) ![image](img.png)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Bold", TextType.bold),
            TextNode(" ", TextType.plain),
            TextNode("italic", TextType.italic),
            TextNode(" ", TextType.plain),
            TextNode("code", TextType.code),
            TextNode(" ", TextType.plain),
            TextNode("link", TextType.links, "url"),
            TextNode(" ", TextType.plain),
            TextNode("image", TextType.images, "img.png")
        ]
        self.assertEqual(expected, nodes)

    def test_plain_text_only(self):
        text = "Just plain text with no formatting"
        nodes = text_to_textnodes(text)
        expected = [TextNode("Just plain text with no formatting", TextType.plain)]
        self.assertEqual(expected, nodes)

    def test_nested_formatting_bold_first(self):
        text = "This is **bold with __nested italic__ inside**"
        nodes = text_to_textnodes(text)
        # Bold is processed first, so __ inside bold stays as literal text (no nesting support)
        expected = [
            TextNode("This is ", TextType.plain),
            TextNode("bold with __nested italic__ inside", TextType.bold)
        ]
        self.assertEqual(expected, nodes)

    def test_multiple_bold_and_italic(self):
        text = "**bold1** normal **bold2** __italic1__ normal __italic2__"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("bold1", TextType.bold),
            TextNode(" normal ", TextType.plain),
            TextNode("bold2", TextType.bold),
            TextNode(" ", TextType.plain),
            TextNode("italic1", TextType.italic),
            TextNode(" normal ", TextType.plain),
            TextNode("italic2", TextType.italic)
        ]
        self.assertEqual(expected, nodes)


if __name__ == "__main__":
    unittest.main()
