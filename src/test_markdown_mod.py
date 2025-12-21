import unittest

from markdown_mod import markdown_to_blocks, markdown_to_html_node
from blocknode import block_to_block_type, BlockType
from main import extract_title


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks_basic(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_single_block(self):
        md = "Just a single paragraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just a single paragraph"])

    def test_markdown_to_blocks_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [""])

    def test_markdown_to_blocks_multiple_newlines(self):
        md = "Block 1\n\nBlock 2\n\nBlock 3"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1", "Block 2", "Block 3"])

    def test_markdown_to_blocks_leading_trailing_newlines(self):
        md = "\n\n\nBlock 1\n\nBlock 2\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1", "Block 2"])

    def test_markdown_to_blocks_headings(self):
        md = "# Heading 1\n\n## Heading 2\n\nParagraph text"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["# Heading 1", "## Heading 2", "Paragraph text"])

    def test_markdown_to_blocks_code_block(self):
        md = "Paragraph\n\n```python\ncode here\n```\n\nAnother paragraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks, ["Paragraph", "```python\ncode here\n```", "Another paragraph"]
        )

    def test_markdown_to_blocks_mixed_content(self):
        md = """# Title

Paragraph with **bold** and _italic_.

- List item 1
- List item 2

> Quote block

1. Numbered item
2. Another item"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Title",
                "Paragraph with **bold** and _italic_.",
                "- List item 1\n- List item 2",
                "> Quote block",
                "1. Numbered item\n2. Another item",
            ],
        )

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_h1(self):
        md = "# Hello World"
        title = extract_title(md)
        self.assertEqual(title, "Hello World")

    def test_extract_title_with_text_after(self):
        md = "# My Title\n\nSome paragraph text"
        title = extract_title(md)
        self.assertEqual(title, "My Title")

    def test_extract_title_with_special_chars(self):
        md = "# Title with **bold** and _italic_"
        title = extract_title(md)
        self.assertEqual(title, "Title with **bold** and _italic_")

    def test_extract_title_no_header(self):
        md = "Just some text without a header"
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertEqual(
            str(context.exception), "Couldn't find a header for the markdown file"
        )

    def test_extract_title_h2_not_h1(self):
        md = "## This is h2, not h1"
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertEqual(
            str(context.exception), "Couldn't find a header for the markdown file"
        )

    def test_extract_title_empty_string(self):
        md = ""
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertEqual(
            str(context.exception), "Couldn't find a header for the markdown file"
        )

    def test_extract_title_whitespace_before(self):
        md = "   # Title with leading whitespace"
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertEqual(
            str(context.exception), "Couldn't find a header for the markdown file"
        )


if __name__ == "__main__":
    unittest.main()
