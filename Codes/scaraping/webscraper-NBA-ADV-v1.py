from selenium import webdriver
from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer
import threading
import pandas as pd
import time

def call_selenium_bs4(driver ,next = False, main_call = False, get_years = False):
    
    if next == True:
        next_page = driver.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[3]/div/div/a[2]')
        next_page.click()
    html = driver.execute_script("return document.documentElement.outerHTML")
    time.sleep(.2)
    sauce = bs(html,'html.parser')
    if get_years == True:
        drop_down_list = sauce.find('select',{'name':'Season'})
        label = drop_down_list.findAll('option')
        lst = list()
        for i in label:
            lst.append(i.getText().strip())
        return lst
    if main_call == True:
        div = sauce.find('div',{'class':'stats-table-pagination__info'})
        time.sleep(1)
        if div != None:
            number_of_pages = div.getText().strip()
            return int(number_of_pages[-1])
        else:
            return call_selenium_bs4(driver,next = False, main_call = True)
    else:
        div = sauce.findAll('div',{'class':'nba-stat-table'})[0]
    table = div.find('table')
    return table

def create_team_stats_table(position,driver):
    lst = call_selenium_bs4(driver,False,False,True)
    data_col = list()
    data_row = [data_col]
    for year in lst:
        driver.get("https://stats.nba.com/players/advanced/?sort=PTS&dir=-1&Season="+year+"&SeasonType=Regular%20Season&PlayerPosition="+position)
        time.sleep(2)
        total_number_of_pages = call_selenium_bs4(driver,next = False, main_call = True)
        player_data_frame = pd.DataFrame()
        headers = list()
        game_links = list() 
        for h in call_selenium_bs4(driver).findAll("th")[1:]:
            if '\n' in h:
                        h = h.replace('\n',' ')
                        headers.append(h.strip())   #method returns bs4 object - table
            headers.append(h.getText().strip())
        headers = headers[:22]
        headers.append('YEAR')

        count = 0
        # next_page = call_selenium_bs4('driver').find_element_by_xpath('/html/body/main/div[2]/div/div/div[3]/div/div/div/nba-stat-table/div[3]/div/div/a[2]')
        while count < total_number_of_pages:
            if count >= 1:
                search_table = call_selenium_bs4(driver,next = True)
            else:
                search_table = call_selenium_bs4(driver)
            for i in search_table.findAll('tr')[1:]:
                for j in i.findAll('td')[1:]:
                    temp = j.getText()
                    if '\n' in temp:
                        temp = temp.replace('\n',' ')
                        data_col.append(temp.strip())
                    else:
                        data_col.append(temp)
                data_col.append(year[0:4])
                data_row.append(data_col)
                data_col = []
            count += 1
     
    # print(headers, len(headers))
    # print(len(data_row))
    all_player_stats = pd.DataFrame(data_row, columns = headers)
    # print(all_player_stats)
    
    # # team_stats = team_stats.drop(team_stats.index[:1])
    all_player_stats.to_csv("D:\\Northeastern courses\\DS 5110\\Project\\Data-Management-and-Processing-Project\\datasets\\player_stats_adv_"+position+".csv",index=None, header=True)
    # # player_data_frame.to_csv(r'D:\vs_code_workspace\DS 5010\player_stats_v2.csv',index=None, header=True)
    return

def initialize_main_threads(position, driver):
    #print(driver)
    driver.get("https://stats.nba.com/players/advanced/?sort=PTS&dir=-1&Season=2019-20&SeasonType=Regular%20Season&PlayerPosition="+ position)
    time.sleep(.2)
    create_team_stats_table(position,driver)
    driver.quit()

if __name__ == "__main__":
    
    chromeDriver = "D:\\Northeastern courses\\DS 5110\Project\\Data-Management-and-Processing-Project\\scaraping\\chromedriver.exe"
    # driver = webdriver.Chrome(chromeDriver)
    # positions = ['F','C','G']
    driver1 = webdriver.Chrome(chromeDriver)
    driver2 = webdriver.Chrome(chromeDriver)
    driver3 = webdriver.Chrome(chromeDriver)
    t1 = threading.Thread(target = initialize_main_threads, args= ('F',driver1))
    t2 = threading.Thread(target = initialize_main_threads, args= ('C',driver2))
    t3 = threading.Thread(target = initialize_main_threads, args= ('G',driver3)) 
    t1.start()
    t2.start()
    t3.start()
    
    # for i in positions:
    #     driver.get("https://stats.nba.com/players/traditional/?sort=PTS&dir=-1&Season=2019-20&SeasonType=Regular%20Season&PlayerPosition="+i)
    #     time.sleep(2)
    #     create_team_stats_table(i)
    # driver.quit()
        
    # driver.get("https://stats.nba.com/players/traditional/?sort=PTS&dir=-1&Season=2019-20&SeasonType=Regular%20Season&PlayerPosition=C")
    # html = driver.execute_script("return document.documentElement.outerHTML")
    # sauce = bs(html,'html.parser')
    
    

    
        
    
    