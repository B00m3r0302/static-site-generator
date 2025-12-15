import unittest

from htmlnode import HTMLNode, LeafNode


class test_prop_to_html(unittest.TestCase):
    def test_empty(self):
        HTMLNode(props={}).props_to_html()
        self.assertEqual(HTMLNode(props={}).props_to_html(), "")

    def test_2(self):
        categories = {
            "youre": "a loser",
            "not": "today satan",
        }
        self.assertEqual(
            HTMLNode(props=categories).props_to_html(),
            ' youre="a loser" not="today satan"',
        )

    def test_5(self):
        categories = {
            "hudson": "smart",
            "work": "dumb",
            "life": "good",
            "dog1": "lilo",
            "dog2": "zoey",
        }
        self.assertEqual(
            HTMLNode(props=categories).props_to_html(),
            ' hudson="smart" work="dumb" life="good" dog1="lilo" dog2="zoey"',
        )


class test_leafnode_to_html(unittest.TestCase):
    def test_basic_no_props(self):
        self.assertEqual(
            LeafNode(tag="p", value="try harder my man").to_html(),
            "<p>try harder my man</p>",
        )

    def test_link(self):
        da_props = {"href": "haha.com/image.png"}
        self.assertNotEqual(
            LeafNode(tag="a", value="try haha", props=da_props),
            '<a href="haha.com/image.png">try haha</a>',
        )


if __name__ == "__main__":
    unittest.main()
