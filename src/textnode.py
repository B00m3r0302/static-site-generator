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
    def __init__(self, text: str):
        self.text = text
        self.text_type = self._get_type()
        self.url = None

        # Normalize the text and get URLs
        self._normalize_text()

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

    def _get_type(self):
        try:
            if self.text.startswith("**") and self.text.endswith("**"):
                return TextType.bold
            elif self.text.startswith("__") and self.text.endswith("__"):
                return TextType.italic
            elif self.text.startswith("`") and self.text.endswith("`"):
                return TextType.code
            elif self.text.startswith("[") and self.text.endswith(")"):
                return TextType.links
            elif self.text.startswith("!") and self.text.endswith(")"):
                return TextType.images
            else:
                return TextType.plain
        except Exception as e:
            print(f"Error: {e}")

    def _normalize_text(self):
        try:
            if self.text_type == TextType.plain:
                self.text = self.text
            if self.text_type == TextType.bold:
                self.text = self._strip_bold(self.text)
            if self.text_type == TextType.italic:
                self.text = self._strip_italic(self.text)
            if self.text_type == TextType.code:
                self.text = self._strip_code(self.text)
            if self.text_type == TextType.links:
                self.text = self._strip_anchor(self.text)
            if self.text_type == TextType.images:
                self.text = self._strip_alt(self.text)

            return self.text, self.text_type, self.url

        except Exception as e:
            print(f"Error: {e}")

    def _strip_bold(self, text):
        try:
            return text[2:-2]
        except Exception as e:
            print(f"Error: {e}")

    def _strip_italic(self, text):
        try:
            return text[2:-2]
        except Exception as e:
            print(f"Error: {e}")

    def _strip_code(self, text):
        try:
            return text[1:-1]
        except Exception as e:
            print(f"Error: {e}")

    def _strip_anchor(self, text):
        try:
            parts = text[1:-1].split("](")
            self.url = parts[1]
            return parts[0]
        except IndexError:
            self.url = None
            return text
        return text

    def _strip_alt(self, text):
        try:
            parts = text[2:-1].split("](")
            self.url = parts[1]
            return parts[0]
        except IndexError:
            self.url = None
            return text
        return text


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
