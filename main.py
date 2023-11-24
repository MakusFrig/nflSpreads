import requests

from bs4 import BeautifulSoup as soup

from bs4 import Comment

import pandas as pd

import csv

#data

#just a test for github

class Game:

    def __init__(self, spread, ou, score):

        self.spread = spread
        self.ou = ou
        self.score = score

    def __str__(self):

        print()

def get_team_link(team_name):

    initLink = "https://www.pro-football-reference.com/teams/"

    #https://www.pro-football-reference.com/

    team_names = requests.get(initLink)

    print(team_names.ok)

    team_names = soup(team_names.content, 'html.parser')

    total = 0

    smt = team_names.findAll("th")

    for i in smt:

        if "data-stat" in i.attrs.keys():

            aTag = i.find("a")

            if aTag != None:

                total += 1

                print(aTag.attrs['href'].split('/')[2])

    print(total)

    return type(smt), len(smt)


#this function returns an array of links to the boxscore of games
def get_season_games(year):

    #the link should look like this 

    #https://www.pro-football-reference.com/years/2023/games.htm

    link = "https://www.pro-football-reference.com/years/" + year + "/games.htm"

    r = requests.get(link)

    html = soup(r.content, 'html.parser')


    #this array will store the links to the box scores
    boxscores = []

    boxscores_tags = html.find_all("a")

    for aTag in boxscores_tags:

        if aTag.text == "boxscore":

            boxscores.append("https://www.pro-football-reference.com" + aTag.attrs['href'])


    return boxscores

#this function will webscrape data from the website to get the spread
#the over under and more information and return it in a list
def get_betting_info(link):

    r = requests.get(link)



    

    html = soup(r.content, 'html.parser')

    score_table = html.find_all( attrs = {"class":"linescore nohover stats_table no_freeze"})

    score_table = score_table[0]

    teams = score_table.find_all("a")

    trList = []

    tdList, thList = [], []

    boxScoreTable = {}

    for i in score_table.find_all('tr'):

        trList.append(i)
    


    for i in trList[0]:

        if i.text != '\n': #we need to include this because of the way the html is written, weird???

            if i.text == '\xa0':
                thList.append('Teams')
            else:
                thList.append(i.text)

    for i in trList[1:]:

        temp = []

        for e in i.find_all('td'):

            temp.append(e.text)

        tdList.append(temp)



    for i in range(len(thList)):

        boxScoreTable[thList[i]] = [tdList[0][i], tdList[1][i]]



    homeTeam = boxScoreTable['Teams'][0]

    awayTeam = boxScoreTable['Teams'][1]

    homeTeamScore = boxScoreTable['Final'][0]

    awayTeamScore = boxScoreTable['Final'][1]


    #from here we want to get the information of the spread and the over under

    commentList = []

    for comments in html.findAll(text=lambda text:isinstance(text, Comment)):
        commentList.append(comments.extract())

    #in the comments of the html we want the index 28 of this to ge the game info

    commentList = ' '.join(commentList)

    

    game_info_html = soup(commentList, 'html.parser')

    table = game_info_html.find('table', id='game_info')

    thList, tdList = [], []

    game_info = {}

    for i in table.find_all('th'):

        thList.append(i.text)

    for i in table.find_all('td'):

        tdList.append(i.text)

    #this is to get ride of the 'game info' text at the top of the html table

    tdList.pop(0)

    for i in range(len(thList)):

        game_info[thList[i]] = tdList[i]


    

    

    #this is what we need to return 
    spread = game_info['Vegas Line']

    temp = spread.split(' ')



    spread = [' '.join(temp[0:len(temp)-1]), temp[len(temp)-1]]

    mov = int(boxScoreTable['Final'][0])-int(boxScoreTable['Final'][1])

    ou = game_info['Over/Under'].split(' ')[0]

    #from here we want to convert everything to a data frame

    temp_game = [homeTeam, awayTeam, homeTeamScore, awayTeamScore] +[spread[0], spread[1], ou, mov]
    
    return temp_game

    



boxscores = get_season_games('2022')



for i in range(10):

    print(get_betting_info(boxscores[i]))

#format of the csv file should be 

# HT, AT, HTFinalScore, AWFinalScore, Spread Fav, Spread, OU, MOV Favorite