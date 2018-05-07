import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import style
import os
from os import path
import numpy as np

style.use('ggplot')


def plot_game(game, game_name, path, just_show):

    game = pd.read_csv(game, index_col='min', na_values='-')
    fig = plt.figure(figsize=(24, 13.5), dpi=80)
    
    ax3 = fig.add_subplot(321)
    ax2 = fig.add_subplot(322)

    ax1_1_hist = fig.add_subplot(334)
    ax1_2_hist = fig.add_subplot(335)
    ax1_x_hist = fig.add_subplot(336)
    
    ax1 = fig.add_subplot(313)
    
    
    
    ax1.plot(game[['odd_1']], color='r', label='odd_1')
    ax1.plot(game[['odd_x']], color='g', label='odd_x')
    ax1.plot(game[['odd_2']], color='b', label='odd_2')

    res_home = game['res_home'][game['res_home'].duplicated() == False]
    res_away = game['res_away'][game['res_away'].duplicated() == False]

    ax1.scatter(res_home.index, res_home, color='r', label='res_home', s=50)
    ax1.scatter(res_away.index, res_away, color='b', label='res_away', s=50)
    ax1.legend(loc="upper left")
    
    ax2.plot(game[['odd_hg_less']], color='orange', label='odd_hg_less')
    ax2.plot(game[['odd_hg_more']], color='r', label='odd_hg_more')
    ax2.plot(game[['odd_hg']], color='g', label='odd_hg')
    ax2.legend(loc="upper left")
    
    ax3.plot(game[['odd_ag_less']], color='orange', label='odd_ag_less')
    ax3.plot(game[['odd_ag_more']], color='b', label='odd_ag_more')
    ax3.plot(game[['odd_ag']], color='g', label='odd_ag')
    ax3.legend(loc="upper left")

    ax1_1_hist.hist(game[['odd_1']].T, color='r')
    ax1_2_hist.hist(game[['odd_2']].T, color='b')
    ax1_x_hist.hist(game[['odd_x']].T, color='g')
    
    plt.suptitle(game_name, fontsize=16)

    plt.ylim(0, 15)
    plt.xticks(game.index)
    plt.yticks(np.arange(0, 16, .5))
    if just_show:
        plt.show()
    else:
        fig.savefig(path + game_name.split('.')[0] + '.png', bbox_inches='tight')

    plt.close()
   


def plot_one_game():
    # print all available games for plot
    for i in range(0, len(logs)):
        print(str(i+1) + ": " + logs[i])
    game_no = int(input('Pick the game from a list')) - 1
    game_file = path_to_logs + logs[game_no]
    plot_game(game_file, logs[game_no], path_to_figures, True)


def draw_all(figures):
    for i in range(0, len(logs)):
        if logs[i].split('.')[0] not in figures:
            try:
                game_file = path_to_logs + logs[i]
                plot_game(game_file, logs[i], path_to_figures, just_show=False)
            except Exception as e:
                print(str(e) + ' - ', logs[i])


path_to_logs = path.abspath(path.curdir) + '\\logs\\'
path_to_figures = path_to_logs + '\\figures\\'
logs = []
existing_figures = []

# get all csv log files
for file in os.listdir(path_to_logs):
    if file.endswith(".csv"):
        logs.append(file)

#get all existing figures
for file in os.listdir(path_to_figures):
    if file.endswith(".png"):
        existing_figures.append(file.split('.')[0])

inp = int(input('Choose option:\n1. Plot all games\n2. Plot and show single game\n'))
if inp == 1:
    draw_all(existing_figures)
elif inp == 2:
    plot_one_game()


