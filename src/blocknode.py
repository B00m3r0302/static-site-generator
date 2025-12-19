from enum import Enum
import re


class BlockType(Enum):
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"


def block_to_block_type(markdown_block):
    def is_ordered(text):
        lines = text.split('\n')
        pattern = re.compile(r"^(\d+)\.\s+")
        numbers = []
        for line in lines:
            match = pattern.match(line)
            if not match:
                return False
            numbers.append(int(match.group(1)))
        return numbers == list(range(1, len(numbers) + 1))

    if re.match(r"^\#{1,6} ", markdown_block):
        return BlockType.heading
    elif re.match(r"^\`\`\`.*\`\`\`$", markdown_block, re.DOTALL):
        return BlockType.code
    elif re.match(r"^\>.*(\n\>.*)*$", markdown_block):
        return BlockType.quote
    elif re.match(r"^\- .*(\n\- .*)*$", markdown_block):
        return BlockType.unordered_list
    elif is_ordered(markdown_block):
        return BlockType.ordered_list
    else:
        return BlockType.paragraph
