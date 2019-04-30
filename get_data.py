from bs4 import BeautifulSoup
from selenium import webdriver
from time import gmtime, strftime
import time
import json
import os.path as path
import re
import pandas as pd

# time to check for updates in seconds
refresh_period = 30

# Path to dir of logs
path_dir = path.abspath(path.curdir) + '\\logs\\'

# configuration file
config_file = path.abspath(path.curdir) + '\\config.json'


def write_to_json(match, log_path):
    with open(log_path
              + strftime("%Y_%m_%d", gmtime())
              + '_' + match['home']
              + '_' + match['away'] + '.json', encoding='utf-8', mode='w') as outfile:
        json.dump(match, outfile, sort_keys=False, indent=4)


def write_to_csv(match, log_path):
    output = pd.DataFrame(match['history'])
    output = output.T
    output.to_csv(log_path
                  + match['start_time']
                  + '_' + match['home']
                  + '_' + match['away'] + '.csv', index_label='min')


def read_config(file_path):
    with open(file_path, encoding="utf-8") as infile:
        config_dict = json.load(infile)
        return config_dict


def translate_odds(mapping_dict, gathered_odds):
    translated_odd = {}
    for i in mapping_dict.keys():
        try:
            translated_odd[i] = gathered_odds[mapping_dict[i]['game_type']][mapping_dict[i]['odd_name']]
        except:
            translated_odd[i] = 1
    return translated_odd

class logger():

    log_path = path.abspath(path.curdir) + '//logs//' + strftime("%Y-%m-%d", gmtime()) + '_log.txt'

    def __init__(self):
        self.file = open(self.log_path, encoding='utf-8', mode='a+')
        self.file.write(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ": Logger started.\n")
        self.file.flush()

    def append(self, message):
        print('logger: ', message)
        self.file.write(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ': ' + message + '\n')
        self.file.flush()

    def close(self):
        self.file.close()


class GamesPool:
    pool = {}

    def start(self):
        log = logger()
        config = read_config(config_file)
        mapping = config['odds']

        url = config['url']
        browser = webdriver.Chrome('C:/chromeDr/chromedriver')
        browser.get(url)

        # wait for js to load
        print('Waiting for JS to load: ')
        for i in range(10, 1, -1):
            time.sleep(1)
            print(i)

        already_started = []
        games_pool = self.pool

        while True:
            html = browser.page_source
            soup = BeautifulSoup(html, 'lxml')


            if browser.current_url != url:
                log.append('Site redirected to different URL. Checking football mathces...')
                #proveri da li postoji neki fudbal pa ako da refreshuj i vrati na pocetni url
                if 'Fudbal' in [i.text for i in soup.find_all('h2')]:
                    log.append('There are football matches. Heading to specified URL.')
                    browser.get(url)
                    time.sleep(7)
                else:
                    log.append('Currently there are no matches. Passing 30s...')
                    time.sleep(60)
            else:
                # get current games
                live_matches = soup.find_all('div', class_ =re.compile('match live'))
                live_matches_ids = [x.find(class_='code').string for x in live_matches]
                print(str(len(live_matches_ids)) + ' matches currently.')

                # check to dump the finished games
                if games_pool:
                    delete = []

                    #check if there are matches
                    if len(live_matches_ids) != 0:
                        for i in games_pool.keys():
                            if i not in live_matches_ids:
                                print('Game ' + i
                                      + ':' + games_pool[i]['home']
                                      + ' - ' + games_pool[i]['away']
                                      + ' has just finished.')
                                log.append('Game ' + i
                                      + ':' + games_pool[i]['home']
                                      + ' - ' + games_pool[i]['away']
                                      + ' has just finished.')
                                log.append('live matches: ' + str(live_matches_ids))
                                log.append('games pool: ' + str(games_pool.keys()))
                                try:
                                    write_to_csv(games_pool[i], path_dir)
                                except Exception as ex:
                                    print('Error writing to file: ' + i + ": " + str(ex))
                                delete.append(i)
                        if delete:
                            for i in delete:
                                del games_pool[i]
                    else:
                        print('Something wrong. Refreshing the page...')
                        log.append('Something wrong. Refreshing the page...')
                        browser.refresh()

                # get the matches data
                for i in live_matches:
                    try:
                        game_time = i.find_all(class_='time')[0].string.strip()
                        game_time = int(str.replace(game_time, "'", ""))
                    except:
                        game_time = None
                    if game_time:
                        code = i.find_all(class_='code')[0].string.strip()
                        league = i.find_all(class_='league')[0].string#.strip()

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

                        available_bets = i.find_all('div', class_='game')
                        odds_dict = {}
                        if available_bets:
                            for game in available_bets:
                                game_type_div = game.div
                                if game_type_div.string:
                                    game_type = game_type_div.string.strip()
                                    new_dict = {}
                                    for desc in game.find_all('div', class_='selection-name'):
                                        try:
                                            odd_name = desc.text
                                            odd = desc.next_sibling.text.strip()
                                            new_dict[odd_name] = odd
                                        except:
                                            pass
                                    odds_dict[game_type] = new_dict

                        translated_odds = translate_odds(mapping, odds_dict)
                        moment = game_time
                        data = {'res_home': home_result,
                                'res_away': away_result
                                }
                        data.update(translated_odds)

                        if code not in games_pool.keys():
                            game_data = {'start_time': strftime("%Y_%m_%d_%H_%M", gmtime()),
                                        'code': code,
                                         'league': league,
                                         'home': home,
                                         'away': away,
                                         'history': {moment: data}
                                         }
                            games_pool[code] = game_data
                        else:
                            games_pool[code]['history'][moment] = data
                time.sleep(refresh_period)
