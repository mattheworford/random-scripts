"""
This script is used to scrape battle-related pages from Wikipedia. It prompts the user to enter the name of a Wikipedia list to scrape. It then goes through each link in the list, checks if the link is a battle page (not a list), and if it is, it scrapes the text from the page, removes certain words (like "References", "==", etc.), and appends the text to a file named "CompleteText.txt" in the "battleTexts" directory.

To run this script, you need to have Python installed on your system along with the required libraries: wikipediaapi, logging, os, and yaml.

You can install the required libraries using pip:
pip install wikipedia-api pyyaml

You also need to have a secrets.yml file in the same directory as this script. The secrets.yml file should contain your user-agent for the Wikipedia API in the following format:

wikipedia:
  user-agent: YOUR_USER_AGENT

Once you have Python and the required libraries installed, and the secrets.yml file set up, you can run the script from the command line as follows:

python singleDoc.py

When prompted, enter the name of the Wikipedia list you want to scrape. The script will then scrape the battle pages from that list and append them to the "CompleteText.txt" file in the "battleTexts" directory.
"""
import wikipediaapi
import logging
import os
import yaml

OUTPUT_DIR = "./battleTexts/"
OUTPUT_FILE = "CompleteText.txt"
EXCLUDE_WORDS = ["References", "==", "See also", "External links", "Notes"]

def get_user_agent(file_path):
    with open(file_path, "r") as stream:
        secrets = yaml.safe_load(stream)
        return secrets["wikipedia"]["user-agent"]

def get_battle_pages(wiki):
    listName = input("Enter the name of the Wikipedia list you want to scrape: ")
    page_list = wiki.page(listName)
    links = page_list.links
    for link in sorted(links):
        title = link.replace(" ", "_")
        if "battle" in title.lower() and "list" not in title.lower():
            yield title

def write_page_to_file(wiki, title):
    page = wiki.page(title)
    if page.exists():
        text = str(page.text)
        for word in EXCLUDE_WORDS:
            text = text.replace(word, "")
        with open(os.path.join(OUTPUT_DIR, OUTPUT_FILE), "a") as output:
            output.write("\n" + text)

def initialize_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        try:
            os.makedirs(OUTPUT_DIR)
        except Exception as e:
            logging.error(f"Failed to create output directory: {e}")

def main():
    logging.basicConfig(level=logging.INFO)
    user_agent = get_user_agent("secrets.yml")
    wiki = wikipediaapi.Wikipedia(user_agent=user_agent, language='en', extract_format=wikipediaapi.ExtractFormat.WIKI)
    initialize_output_dir()
    for title in get_battle_pages(wiki):
        try:
            write_page_to_file(wiki, title)
            logging.info(f"Written page {title} to file.")
        except Exception as e:
            logging.error(f"Failed to write page {title} to file: {e}")

if __name__ == "__main__":
    main()