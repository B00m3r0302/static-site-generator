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


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.plain:
            new_nodes.append(node)
            continue

        if len(node.text) == 0:
            continue

        matches = extract_markdown_images(node.text)
        if not matches:
            new_nodes.append(node)
            continue

        text = node.text
        for alt_text, url in matches:
            pattern = f"![{alt_text}]({url})"
            parts = text.split(pattern, 1)
            if len(parts) == 2:
                if parts[0]:
                    new_nodes.append(TextNode(parts[0], TextType.plain))
                new_nodes.append(TextNode(alt_text, TextType.images, url))
                text = parts[1]

        if text:
            new_nodes.append(TextNode(text, TextType.plain))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.plain:
            new_nodes.append(node)
            continue

        if len(node.text) == 0:
            continue

        matches = extract_markdown_links(node.text)
        if not matches:
            new_nodes.append(node)
            continue

        text = node.text
        for link_text, url in matches:
            pattern = f"[{link_text}]({url})"
            parts = text.split(pattern, 1)
            if len(parts) == 2:
                if parts[0]:
                    new_nodes.append(TextNode(parts[0], TextType.plain))
                new_nodes.append(TextNode(link_text, TextType.links, url))
                text = parts[1]

        if text:
            new_nodes.append(TextNode(text, TextType.plain))

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.plain)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.bold)
    nodes = split_nodes_delimiter(nodes, "__", TextType.italic)
    nodes = split_nodes_delimiter(nodes, "_", TextType.italic)
    nodes = split_nodes_delimiter(nodes, "`", TextType.code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
