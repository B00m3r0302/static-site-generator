class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        print(f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})")

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        try:
            if self.props is None or len(self.props) == 0:
                return ""
            else:
                result = ""
                for item in self.props:
                    result += f' {item}="{self.props[item]}"'
                return result
        except Exception as e:
            print(f"Error: {e}")
        return ""


class LeafNode(HTMLNode):
    def __init__(self, value, tag, props=None):
        super().__init__(tag, value, props)

    def to_html(self):
        try:
            if self.value is None:
                raise ValueError("All leaf nodes MUST have a value")
            if self.tag is None:
                return str(self.value)
            else:
                if self.props is not None:
                    return f"<{self.tag} {self.props_to_html(self.props)}>{self.value}</{self.tag}>"
                else:
                    return f"<{self.tag}>{self.value}</{self.tag}>"
        except Exception as e:
            print(f"Error: {e}")
