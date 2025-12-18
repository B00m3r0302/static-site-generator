from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []

    for node in old_nodes:
        if node.text_type != TextType.plain:
            new_list.append(node)
            continue

        sp = node.text.split(delimiter)
        for i in range(len(sp)):
            if sp[i] == "":
                continue
            if i % 2 == 0:
                new_list.append(TextNode(sp[i], TextType.plain))
            else:
                new_list.append(TextNode(sp[i], text_type))
    return new_list


def extract_markdown_images(text):
    image_pattern = re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
    return image_pattern


def extract_markdown_links(text):
    link_pattern = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return link_pattern
