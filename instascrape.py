## This script is used to scrape the followers of a given Instagram account and save them to a text file.

import instaloader
import yaml

L = instaloader.Instaloader()

with open("secrets.yml", "r") as stream:
    secrets = yaml.safe_load(stream)
    credentials = secrets["instagram"]["credentials"]

    L.login(credentials["username"], credentials["password"])

    username = input("Enter the username of the account you want to scrape: ")
    profile = instaloader.Profile.from_username(L.context, username)

    follow_list = [followee.username for followee in profile.get_followers()]

    file = open("followers.txt","a+")
    for username in follow_list:
        file.write(username + "\n")
        print(username)
    file.close()