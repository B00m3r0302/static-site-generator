import unittest

from markdown_mod import markdown_to_blocks


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


if __name__ == "__main__":
    unittest.main()
