from selenium import webdriver
from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer
import pandas as pd
import time

def call_selenium_bs4(next = False):
    
    if next == True:
        next_page = driver.find_element_by_xpath('/html/body/main/div[2]/div/div/div[3]/div/div/div/nba-stat-table/div[3]/div/div/a[2]')
        next_page.click()
    html = driver.execute_script("return document.documentElement.outerHTML")
    sauce = bs(html,'html.parser')
    div = sauce.findAll('div',{'class':'nba-stat-table'})[0]
    table = div.find('table')
    return table


def create_team_stats_table():
    
    player_data_frame = pd.DataFrame()
    headers = list()
    game_links = list() 
    for h in call_selenium_bs4().findAll("th"):   #method returns bs4 object - table
        headers.append(h.getText())

    data_col = list()
    data_row = [data_col]
    
    count = 0
    # next_page = call_selenium_bs4('driver').find_element_by_xpath('/html/body/main/div[2]/div/div/div[3]/div/div/div/nba-stat-table/div[3]/div/div/a[2]')
    while count < total_table_pages:
        if count >= 1:
            search_table = call_selenium_bs4(True)
        else:
            search_table = call_selenium_bs4()
        for i in search_table.findAll('tr')[1:]:
            for j in i.findAll('td'):
                temp = j.getText()
                if '\n' in temp:
                    temp = temp.replace('\n',' ')
                    data_col.append(temp.strip())
                else:
                    data_col.append(temp)
            data_row.append(data_col)
            data_col = []
            
        for col1 in search_table.findAll('td',{'class':'lineup'}):
            for link in col1.findAll('a',href=True):
                player_table = create_player_stats_table([link['href'],link.getText()])
                player_data_frame = player_data_frame.append(player_table)
            
        count += 1
     
    
    team_stats = pd.DataFrame(data_row, columns = headers)
    team_stats = team_stats.drop(team_stats.index[:1])
    team_stats.to_csv(r'D:\vs_code_workspace\DS 5010\team_stats_v2.csv',index=None, header=True)
    player_data_frame.to_csv(r'D:\vs_code_workspace\DS 5010\player_stats_v2.csv',index=None, header=True)
    return

def create_player_stats_table(game_link_and_name):
    
    i = game_link_and_name
    match_against = i[1] 
    chromeDriver = "D:\\software setups\\coding\\chromedriver.exe"
    new_driver = webdriver.Chrome(chromeDriver)
    new_driver.get("https://stats.nba.com"+str(i[0]))
    time.sleep(5)
    html = new_driver.execute_script("return document.documentElement.outerHTML")
    sauce2 = bs(html,'html.parser')
    # home vs away , table location are placed differnetly
    
    time.sleep(2)
    if '@' in i[1]:
        div = sauce2.find('div',{'class':'nba-stat-table'})
    else:
        div = sauce2.findAll('div',{'class':'nba-stat-table'})[1]
    
    
    # bs4 objects for table head and table body
    player_head = div.find('thead')
    player_body = div.find('tbody')
    
    player_data_col = list()
    player_data_row = [player_data_col]
    headers = list()
        
    for h in player_head.findAll("th"):
        headers.append(h.getText())
    headers.append("MATCHUP")
    
    for tr in player_body.findAll('tr'):
        for td in tr.findAll('td'):
            temp = td.getText()
            if '\n' in temp:
                temp = temp.replace('\n',' ')
                player_data_col.append(temp.strip())
            else:
                player_data_col.append(temp)
        player_data_col.append(match_against)
        player_data_row.append(player_data_col)
        player_data_col = []

    player_stats = pd.DataFrame(player_data_row,columns=headers)
    # player_data_frame = player_data_frame.append(player_stats)
    
    new_driver.close()
    return player_stats
    
        
    

if __name__ == "__main__":
    
    
    total_table_pages = 2
    chromeDriver = "D:\\software setups\\coding\\chromedriver.exe"
    driver = webdriver.Chrome(chromeDriver)
    # driver.get("https://stats.nba.com/team/1610612738/boxscores/?sort=MATCHUP&dir=-1")
    driver.get("https://stats.nba.com/team/1610612738/boxscores/?Season=2018-19&SeasonType=Regular%20Season")
    time.sleep(2)
    create_team_stats_table()