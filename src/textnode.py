from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode


class TextType(Enum):
    plain = "plain"
    bold = "bold"
    italic = "italic"
    code = "code"
    links = "links"
    images = "images"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, textnode):
        if not isinstance(textnode, TextNode):
            return NotImplemented

        return (
            self.text == textnode.text
            and self.text_type == textnode.text_type
            and self.url == textnode.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    try:
        TextType(text_node.text_type)
    except ValueError:
        print("Value for the text type is not valid and not a supported type.")

    if text_node.text_type == TextType.plain:
        return LeafNode(value=text_node.text, tag=None)
    if text_node.text_type == TextType.bold:
        return LeafNode(value=text_node.text, tag="b")
    if text_node.text_type == TextType.italic:
        return LeafNode(value=text_node.text, tag="i")
    if text_node.text_type == TextType.code:
        return LeafNode(value=text_node.text, tag="code")
    if text_node.text_type == TextType.links:
        return LeafNode(value=text_node.text, tag="a", props={"href": text_node.url})
    if text_node.text_type == TextType.images:
        return LeafNode(
            value="", tag="img", props={"src": text_node.url, "alt": text_node.text}
        )
