from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode 
import re

def split_nodes_delimiter(old_nodes, delimiter):
    new_list = []
    tmp = []
    st = ""
    patterns = [ (TextType.bold, "*"), 
                (TextType.italic, "_"),
                (TextType.code, "`"),
            ]
    what_type = TextType.plain

    for node in old_nodes:
        tmp = tmp.extend(node)
        for character in range(0, len(tmp)):
            while character is not delimiter:
                st += tmp[character]
                if character is delimiter:

        




