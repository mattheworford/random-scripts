## This script will pull the average weight of each NFL team and write it to a CSV file

import csv
import json
import requests
import yaml

with open("secrets.yml", "r") as stream:
    secrets = yaml.safe_load(stream)
    teams_url = 'https://api.sportsdata.io/v3/nfl/scores/json/Teams'
    headers = {'Ocp-Apim-Subscription-Key': secrets["ocp-apim"]["subscription-key"]}
    teams_response = requests.get(teams_url, headers=headers)
    teams = json.loads(teams_response.text)

    weight_dict = {}
    lightest_weight = {}

    header = ['Team', 'Total Weight', '# of Players', 'Average Weight']

    with open('nfl_weights.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for team in teams:
            team_key = team['Key']
            players_url = f'https://api.sportsdata.io/v3/nfl/scores/json/Players/{team_key}'
            players_response = requests.get(players_url, headers=headers)
            players = json.loads(players_response.text)
            total_weight = 0
            num_players = 0
            for player in players:
                if player['Status'] == 'Active':
                    total_weight += player['Weight']
                    num_players += 1

            avg_weight = total_weight / num_players
            weight_dict[team_key] = avg_weight
            print(f"Team: {team_key}\n\t"
                f"Total Weight: {total_weight}\n\t"
                f"# of Players: {num_players}\n\t"
                f"Average Weight: {avg_weight}\n")
            data = [team_key, total_weight, num_players, avg_weight]
            writer.writerow(data)
        sorted_weight_dict = dict(sorted(weight_dict.items(), key=lambda item: item[1]))
        print(sorted_weight_dict)
