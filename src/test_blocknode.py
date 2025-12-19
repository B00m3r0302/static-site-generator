import unittest

from blocknode import block_to_block_type, BlockType


class TestBlockToBlockType(unittest.TestCase):
    def test_heading_h1(self):
        block = "# Heading 1"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.heading)

    def test_heading_h6(self):
        block = "###### Heading 6"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.heading)

    def test_heading_with_space_required(self):
        block = "#Heading without space"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.paragraph)

    def test_heading_too_many_hashes(self):
        block = "####### Not a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.paragraph)

    def test_code_block(self):
        block = "```python\nprint('hello')\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.code)

    def test_code_block_empty(self):
        block = "```\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.code)

    def test_code_block_multiline(self):
        block = "```\nline1\nline2\nline3\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.code)

    def test_quote_single_line(self):
        block = ">This is a quote"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.quote)

    def test_quote_multiline(self):
        block = ">First line\n>Second line\n>Third line"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.quote)

    def test_quote_all_lines_must_start_with_gt(self):
        block = ">First line\nSecond line without >\n>Third line"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.paragraph)

    def test_unordered_list_single_item(self):
        block = "- Item 1"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.unordered_list)

    def test_unordered_list_multiple_items(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.unordered_list)

    def test_unordered_list_all_lines_must_start_with_dash(self):
        block = "- Item 1\nItem 2 without dash\n- Item 3"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.paragraph)

    def test_unordered_list_requires_space_after_dash(self):
        block = "-Item without space"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.paragraph)

    def test_ordered_list_single_item(self):
        block = "1. Item 1"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ordered_list)

    def test_ordered_list_multiple_items(self):
        block = "1. Item 1\n2. Item 2\n3. Item 3"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ordered_list)

    def test_ordered_list_must_start_at_1(self):
        block = "2. Item 2\n3. Item 3"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.paragraph)

    def test_ordered_list_must_be_sequential(self):
        block = "1. Item 1\n3. Item 3"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.paragraph)

    def test_ordered_list_all_lines_must_be_numbered(self):
        block = "1. Item 1\nItem 2 without number\n3. Item 3"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.paragraph)

    def test_paragraph_plain_text(self):
        block = "This is just a paragraph"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.paragraph)

    def test_paragraph_multiline(self):
        block = "This is a paragraph\nwith multiple lines\nbut no special formatting"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.paragraph)

    def test_paragraph_with_bold_italic(self):
        block = "This has **bold** and _italic_ text"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.paragraph)


if __name__ == "__main__":
    unittest.main()
