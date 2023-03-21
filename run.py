import os
import re
from lxml import html
from urllib.parse import unquote

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def extract_headline(html_content):
    tree = html.fromstring(html_content)
    headline_div = tree.find_class('doc-title editable')
    if headline_div:
        return headline_div[0].text_content().strip()
    return None

def rename_html_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r") as file:
                content = file.read()
                headline = extract_headline(content)
                if headline:
                    new_filename = sanitize_filename(headline) + ".html"
                    new_filepath = os.path.join(directory, new_filename)
                    os.rename(filepath, new_filepath)
                    print(f"Renamed '{filename}' to '{new_filename}'")
                else:
                    print(f"Warning: No headline found in '{filename}'")

if __name__ == "__main__":
    directory = os.path.dirname(os.path.abspath(__file__))
    rename_html_files(directory)
