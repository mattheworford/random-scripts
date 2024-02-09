"""
This script is used to scrape the text from every page on a given Wikipedia 
list. It prompts the user to enter the name of a Wikipedia list to scrape. 
It then goes through each link in the list, checks if the link is a page (vs. 
another list), and if it is, it scrapes the text from the page, removes 
certain words (like "References", "==", etc.), and writes the text to a 
separate file for each page in the given directory.

To run this script, you need to have Python installed on your system along
with the required libraries: wikipediaapi, logging, os, and yaml.

You can install the required libraries using pip:
pip install wikipedia-api pyyaml

You also need to have a secrets.yml file in the same directory as this script.
The secrets.yml file should contain your user-agent for the Wikipedia API in 
the following format:

wikipedia:
  user-agent: YOUR_USER_AGENT

Once you have Python and the required libraries installed, and the secrets.yml 
file set up, you can run the script from the command line as follows:

python multiDoc.py

When prompted, enter the name of the Wikipedia list you want to scrape and the 
name of the desired output directory. The script will then scrape the pages 
from said list and write them to separate files in the given directory.
"""

import wikipediaapi
import logging
import os
import yaml

EXCLUDE_WORDS = ["References", "==", "See also", "External links", "Notes"]


def get_user_agent(file_path):
    with open(file_path, "r") as stream:
        secrets = yaml.safe_load(stream)
        return secrets["wikipedia"]["user-agent"]


def get_pages(wiki):
    listName = input("Enter the name of the Wikipedia list you want to scrape: ")
    page_list = wiki.page(listName)
    links = page_list.links
    for link in sorted(links):
        title = link.replace(" ", "_")
        if "list" not in title.lower():
            yield title


def write_page_to_file(wiki, title, output_dir):
    page = wiki.page(title)
    if page.exists():
        text = str(page.text)
        for word in EXCLUDE_WORDS:
            text = text.replace(word, "")
        with open(os.path.join(output_dir, title + ".txt"), "w") as output:
            output.write(text)


def initialize_output_dir():
    output_dir = input("Enter the name of the output directory: ")

    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
        except Exception as e:
            logging.error(f"Failed to create output directory: {e}")
    return output_dir


def main():
    logging.basicConfig(level=logging.INFO)
    user_agent = get_user_agent("secrets.yml")
    wiki = wikipediaapi.Wikipedia(
        user_agent=user_agent,
        language="en",
        extract_format=wikipediaapi.ExtractFormat.WIKI,
    )
    output_dir = initialize_output_dir()
    for title in get_pages(wiki):
        try:
            write_page_to_file(wiki, title, output_dir)
            logging.info(f"Written page {title} to file.")
        except Exception as e:
            logging.error(f"Failed to write page {title} to file: {e}")


if __name__ == "__main__":
    main()
