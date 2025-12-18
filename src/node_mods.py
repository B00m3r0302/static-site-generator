from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode


def split_nodes_delimiter(old_nodes, delimiter):
    new_list = []

    for node in old_nodes:
        sp = node.text.split(delimiter)
        for item in range(0, len(sp)):
            tm = [sp[item]]
            new_list.append(tm)
    return new_list
