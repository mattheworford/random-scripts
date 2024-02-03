"""
To run this script, you need to have Python installed on your system along with the required libraries: instaloader, yaml, and logging.

You can install the required libraries using pip:
pip install instaloader pyyaml

You also need to have a secrets.yml file in the same directory as this script. The secrets.yml file should contain your Instagram credentials in the following format:

instagram:
  credentials:
    username: YOUR_USERNAME
    password: YOUR_PASSWORD

Once you have Python and the required libraries installed, and the secrets.yml file set up, you can run the script from the command line as follows:

python instascrape.py

When prompted, enter the username of the Instagram account you want to scrape. The script will then scrape the followers of that account and save them to a file named followers.txt in the same directory as the script.
"""

import instaloader
import yaml
import logging

def load_credentials(file_path):
    with open(file_path, "r") as stream:
        secrets = yaml.safe_load(stream)
        return secrets["instagram"]["credentials"]

def login_instagram(credentials):
    L = instaloader.Instaloader()
    L.login(credentials["username"], credentials["password"])
    return L

def scrape_followers(loader, username):
    profile = instaloader.Profile.from_username(loader.context, username)
    return [followee.username for followee in profile.get_followers()]

def save_followers(follow_list, file_path):
    with open(file_path, "a+") as file:
        for username in follow_list:
            file.write(username + "\n")
            logging.info(username)

def main():
    logging.basicConfig(level=logging.INFO)
    credentials = load_credentials("secrets.yml")
    loader = login_instagram(credentials)
    username = input("Enter the username of the account you want to scrape: ")
    follow_list = scrape_followers(loader, username)
    save_followers(follow_list, "followers.txt")

if __name__ == "__main__":
    main()