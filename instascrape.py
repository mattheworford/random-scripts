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