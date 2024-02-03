import csv
import json
import requests
import yaml
import logging
from collections import namedtuple

TEAMS_URL = 'https://api.sportsdata.io/v3/nfl/scores/json/Teams'
PLAYERS_URL = 'https://api.sportsdata.io/v3/nfl/scores/json/Players/{}'

WeightStats = namedtuple('WeightStats', ['total_weight', 'num_players', 'avg_weight'])

def load_secrets(file_path):
    with open(file_path, "r") as stream:
        secrets = yaml.safe_load(stream)
        return secrets["ocp-apim"]["subscription-key"]

def get_teams(subscription_key):
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    response = requests.get(TEAMS_URL, headers=headers)
    response.raise_for_status()
    return json.loads(response.text)

def get_players(subscription_key, team_key):
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    response = requests.get(PLAYERS_URL.format(team_key), headers=headers)
    response.raise_for_status()
    return json.loads(response.text)

def calculate_weights(subscription_key, teams):
    weight_dict = {}
    for team in teams:
        team_key = team['Key']
        players = get_players(subscription_key, team_key)
        total_weight = sum(player['Weight'] for player in players if player['Status'] == 'Active')
        num_players = sum(1 for player in players if player['Status'] == 'Active')
        avg_weight = total_weight / num_players if num_players else 0
        weight_dict[team_key] = WeightStats(total_weight, num_players, avg_weight)
        logging.info(f"Team: {team_key}, Total Weight: {total_weight}, # of Players: {num_players}, Average Weight: {avg_weight}")
    return weight_dict

def write_to_csv(weight_dict, file_path):
    with open(file_path, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Team', 'Total Weight', '# of Players', 'Average Weight'])
        for team_key, weight_stats in weight_dict.items():
            writer.writerow([team_key, weight_stats.total_weight, weight_stats.num_players, weight_stats.avg_weight])

def main():
    logging.basicConfig(level=logging.INFO)
    subscription_key = load_secrets("secrets.yml")
    teams = get_teams(subscription_key)
    weight_dict = calculate_weights(subscription_key, teams)
    sorted_weight_dict = dict(sorted(weight_dict.items(), key=lambda item: item[1]))
    write_to_csv(sorted_weight_dict, 'nfl_weights.csv')

if __name__ == "__main__":
    main()