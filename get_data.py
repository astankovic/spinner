from bs4 import BeautifulSoup
from selenium import webdriver
import time
from time import gmtime, strftime
import json
import csv
import os.path as path

# from tabulate import tabulate

# config

# time to check for updates in seconds
refresh_period = 30

# Path to dir of logs
path_dir = path.abspath(path.curdir) + '\\logs\\'


class GameSummary:
    # storing result and odds during the game

    def __init__(self, ID, home, away):
        self.ID = ID
        self.home = home
        self.away = away
        self.history = {}

    def collect_data(self, period, data):
        if period not in self.history.keys():
            self.history[period] = data
            return 1
        else:
            return 0

    def write_to_csv(self, location):
        with open(location
                  + strftime("%Y_%m_%d", gmtime())
                  + '_' + self.home
                  + '_' + self.away + '.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Spam'] * 5 + ['Baked Beans'])
            writer.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

    def write_json(self, location):
        with open(location
                  + strftime("%Y_%m_%d", gmtime())
                  + '_' + self.home
                  + '_' + self.away + '.json', 'wb') as outfile:
            json.dump(self.__dict__, outfile)

    def to_json(self, location):
        with open(location
                  + strftime("%Y_%m_%d", gmtime())
                  + '_' + self.home
                  + '_' + self.away + '.json', 'wb') as outfile:
            json.dump(self, outfile, default=lambda o: o.__dict__,
                            sort_keys=True, indent=4)

    # todo - should be deserialized
    def read_json(self, location):
        pass
        with open(location) as infile:
            self = json.load(infile)


def write_to_json(match, log_path):
    with open(log_path
              + strftime("%Y_%m_%d", gmtime())
              + '_' + match['home']
              + '_' + match['away'] + '.json', 'w') as outfile:
        json.dump(match, outfile, sort_keys=True, indent=4)


url = 'https://meridianbet.rs/sr/kladjenje/uzivo/fudbal'
browser = webdriver.Chrome('C:/chromeDr/chromedriver')
browser.get(url)

# todo
# browser.quit()

# wait for js to load
print('Waiting for JS to load: ')
for i in range(6, 1, -1):
    time.sleep(1)
    print(i)

games_pool = {}

while True:
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')

    # get current games
    live_matches = soup.find_all('div', {'class': 'match live'})
    live_matches_ids = [x.find(class_='code').string for x in live_matches]
    print(str(len(live_matches_ids)) + ' matches currently.')

    # check to dump the finished games
    if games_pool:
        delete = []
        for i in games_pool.keys():
            if i not in live_matches_ids:
                write_to_json(games_pool[i], path_dir)
                print('Game ' + i
                      + ':' + games_pool[i]['home']
                      + ' - ' + games_pool[i]['away']
                      + ' has just finished.')
                delete.append(i)
        if delete:
            for i in delete:
                del games_pool[i]

    # get the matches data
    for i in live_matches:

        code = i.find_all(class_='code')[0].string.strip()
        league = i.find_all(class_='league')[0].string.strip()
        try:
            game_time = i.find_all(class_='time')[0].string.strip()
        except:
            game_time = None
        home = i.find_all(class_='home')[0].string.strip()
        away = i.find_all(class_='away')[0].string.strip()

        try:
            home_result = i.find_all(class_='home')[1].string.strip()
        except:
            home_result = None
        try:
            away_result = i.find_all(class_='away')[1].string.strip()
        except:
            away_result = None

        odds = []
        selection_odds = i.find_all('div', class_='selection-odd')
        for odd in selection_odds:
            odds.append(odd.string.strip())

        # game.append(code)
        # game.append(game_time)
        # game.append(home)
        # game.append(away)
        # game.append(home_result + '-' + away_result)
        # game.extend(odds)
        # games.append(game)

        # todo
        available_bets = i.find_all('div', class_='game')
        odds = {}
        for game in available_bets:
            for desc in game.descendants:
                if desc['class'] == "selection-name":
                    odd_name = desc.string
                    odd = desc.next_sibling.string
                    odds[odd_name] = odd

        moment = game_time
        data = {'res_home': home_result,
                'res_away': away_result,
                'odd_1': odds[0],
                'odd_x': odds[1],
                'odd_2': odds[2],

                'odd_tg_less': odds[5],
                'odd_tg_more': odds[6],
                'odd_tg': odds[7],

                'odd_hg_less': odds[8],
                'odd_hg_more': odds[9],
                'odd_hg': odds[9],

                'odd_ag_less': odds[10],
                'odd_ag_more': odds[11],
                'odd_ag': odds[12]}


        if code not in games_pool.keys():

            game_data = {'code': code,
                         'league': league,
                         'home': home,
                         'away': away,
                         'history': {moment: data}
                         }
            games_pool[code] = game_data
            # game_data = GameSummary(code, home, away)
            # game_data.collect_data(moment, data)
            # games_pool[game_data.ID] = game_data
        else:
            games_pool[code]['history'][moment] = data
            # games_pool[game_data.ID].collect_data(moment, data)

        # print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        # print(tabulate(games,
        #                headers=["Code", "Time", "Home", "Away", "Result", "1", "x", "2", "", "", "UG<", "UG>", "UG",
        #                         "D<", "D>", "DG", "G<", "G>", "GG", "", "", ""]))

    # if input('stop?') != '':
    #     break
    for i in range(refresh_period):
        time.sleep(1)
        # print(i * 'x' + (refresh_period - i) * '_')
