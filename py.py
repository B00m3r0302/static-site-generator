md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
li = md.strip("\n")
li = li.split("\n\n")
print(li)
