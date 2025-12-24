from dotenv import load_dotenv
from mal import client
import os
import numpy as np
filepath = os.path.dirname(os.path.abspath(__file__))

np.set_printoptions(legacy='1.25')

class CompareFriendsLists:

    def __init__(self, cli_in, users_in):
        self.cli = cli_in
        self.users = users_in

    def read_manga_list(self, limit=1000, status_list=["completed", "watching"]):
        manga_info = {}

        for user in self.users:
            data = self.cli.get_manga_list(user, limit=limit, fields=[
                "title",
                "mean",
            ])

            if data == None:
                raise LookupError(f"User {user} does not have any manga saved.")
            
            for entry in data:
                title = entry.entry.title
                series = entry.entry
                status = entry.list_status.status.value
                score = entry.score
                if status in status_list:
                    if user not in manga_info:
                        manga_info[user] = {title: {"series" : series, "status" : status, "score": score}}

                    else:
                        manga_info[user][title] = {"series" : series, "status" : status, "score": score}
            
            if user not in manga_info:
                raise LookupError(f"User {user} does not have any manga that fullfil the conditions")

        return manga_info

    def read_anime_list(self, limit=1000, status_list=["completed", "watching"]):
        anime_info = {}

        for user in self.users:
            data = self.cli.get_anime_list(user, limit=limit, fields=[
                "title",
                "mean",
            ])

            if data == None:
                raise LookupError(f"User {user} does not have any anime saved.")
            
            for entry in data:
                title = entry.entry.title
                series = entry.entry
                status = entry.list_status.status.value
                score = entry.score
                if status in status_list:
                    if user not in anime_info:
                        anime_info[user] = {title: {"series" : series, "status" : status, "score": score}}

                    else:
                        anime_info[user][title] = {"series" : series, "status" : status, "score": score}
                
            if user not in anime_info:
                raise LookupError(f"User {user} does not have any anime that fullfil the conditions")
        
        return anime_info

    def separate_to_combined_and_seperate(self, info):
        combined = {}
        seperate = {}

        for anime in {a for user in self.users for a in info[user]}:
            people = [u for u in self.users if anime in info[u]]

            scores = [
                info[u][anime]["score"]
                for u in people
                if info[u][anime]["score"] != 0
            ]

            if len(people) == 1:
                user = people[0]
                seperate[anime] = {
                    "score": info[user][anime]["score"],
                    "user": user
                }
            else:
                mean_value = np.mean(scores) if scores else 0
                combined[anime] = {
                    "mean_value": mean_value,
                    "people": people
                }

        return combined, seperate
    
    @staticmethod
    def sort_combined(combined, 
                      key=lambda item: (len(item[1]["people"]), item[1]["mean_value"]), 
                      reverse=True):
        
        return dict(sorted(combined.items(), key=key, reverse=reverse))

    @staticmethod
    def save_combined(combined, filename, filepath=filepath):
        data_path = os.path.join(filepath, filename)
        with open(data_path, "w") as outfile:
            outfile.write("Title; Mean Score; People\n")
            for item in combined.items():
                s = f"{item[0]}; {item[1]['mean_value']:.2f}; " + ", ".join(item[1]["people"]) + "\n"

                outfile.write(s)

# Check main
if __name__ == '__main__':
    # This code won't run if this file is imported.
    load_dotenv()

    MAL_TOKEN = os.environ["MAL_TOKEN"]
    cli = client.Client(MAL_TOKEN)

    users = ["Stark700", "Joabter", "ktulu007", "dezdance", "Sxlemm_"]
    
    cfl = CompareFriendsLists(cli, users)

    info = cfl.read_anime_list()

    combined, seperate = cfl.separate_to_combined_and_seperate(info)

    sorted_combined = cfl.sort_combined(combined)

    cfl.save_combined(sorted_combined, "sorted_combined_test.csv")
