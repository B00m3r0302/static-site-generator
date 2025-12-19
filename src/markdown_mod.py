def markdown_to_blocks(markdown):
    blocks = markdown.strip("\n")
    blocks = blocks.split("\n\n")
    return blocks
