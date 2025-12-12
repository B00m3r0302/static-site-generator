from enum import Enum


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
            self.text == textnode.text,
            self.text_type == textnode.text_type,
            self.url == textnode.url,
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    def _get_type(self):
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

    def _normalize_text(self):
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

    def _strip_bold(self, text):
        return text[2:-2]

    def _strip_italic(self, text):
        return text[2:-2]

    def _strip_code(self, text):
        return text[1:-1]

    def _strip_anchor(self, text):
        parts = text[1:-1].split("](")
        self.url = parts[1]
        return parts[0]

    def _strip_alt(self, text):
        parts = text[2:-1].split("](")
        self.url = parts[1]
        return parts[0]
