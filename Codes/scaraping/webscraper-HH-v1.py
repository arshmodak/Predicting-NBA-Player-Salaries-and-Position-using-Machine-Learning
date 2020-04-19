from selenium import webdriver
from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer
import pandas as pd
import time


def call_selenium_bs4(driver ,next = False, main_call = False, get_years = False):
    
    # if next == True:
    #     next_page = driver.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[3]/div/div/a[2]')
    #     next_page.click()
    html = driver.execute_script("return document.documentElement.outerHTML")
    time.sleep(.2)
    sauce = bs(html,'html.parser')
    if get_years == True:
        drop_down_list = sauce.findAll('li',{'class':'group'})
        current_year = sauce.find('a',{'class':'active-team'}, href = True)
        list_of_years = list()
        list_of_years.append(current_year['href'])
        for i in drop_down_list:
            for j in i.findAll('a',href = True):
                # j.getText()           # missing 1990-91 season data
                list_of_years.append((j['href']))
        return list_of_years
        
    # if main_call == True:
    #     div = sauce.find('div',{'class':'stats-table-pagination__info'})
    #     time.sleep(1)
    #     if div != None:
    #         number_of_pages = div.getText().strip()
    #         return int(number_of_pages[-1])
    #     else:
    #         return call_selenium_bs4(driver,next = False, main_call = True)
    else:
        table = sauce.find('table',{'class':'hh-salaries-ranking-table hh-salaries-table-sortable responsive'})
    return table

def create_team_stats_table(driver):
    # driver = webdriver.Chrome(chromeDriver)
    lst = call_selenium_bs4(driver,get_years=True)
    data_col = list()
    data_row = [data_col]
    outer_count = 0
    for year in lst:
        outer_count += 1
        driver.get(year)
        time.sleep(2)
        player_data_frame = pd.DataFrame()
        headers = list()
        game_links = list() 
        table =  call_selenium_bs4(driver)
        
        for i in table.find('tbody').findAll('tr'):
            inner_counter = 0
            for j in i.findAll('td')[:4]:
                inner_counter += 1
                if inner_counter == 4:
                    temp = j.getText()
                temp = j.getText()
                if '\n' in temp:
                    temp = temp.replace('\n',' ')
                    data_col.append(temp.strip())
                else:
                    data_col.append(temp)
            
            if outer_count == 1:
                year_link = "2019"
            else: 
                year_link = (str(year[39:42])).replace('/','')
            print(year_link)
                
            data_col.append(year_link)
            data_row.append(data_col)
            # print(year_link)
            data_col = []
        
    
    print(headers, len(headers))
    print(len(data_row))
    headers = ['Rank','Player Name','Salary','InflatedSalary','Year']
    all_player_stats = pd.DataFrame(data_row, columns= headers)
    print(all_player_stats)
   
    # # # team_stats = team_stats.drop(team_stats.index[:1])
    all_player_stats.to_csv("D:\\Northeastern courses\\DS 5110\\Project\\Data-Management-and-Processing-Project\\datasets\\player_salary.csv",index=None, header=True)
    # # # player_data_frame.to_csv(r'D:\vs_code_workspace\DS 5010\player_stats_v2.csv',index=None, header=True)
    return

if __name__ == "__main__":
    
    chromeDriver = "D:\\Northeastern courses\\DS 5110\Project\\Data-Management-and-Processing-Project\\scaraping\\chromedriver.exe"
    driver = webdriver.Chrome(chromeDriver)
    driver.get("https://hoopshype.com/salaries/players/")
    create_team_stats_table(driver)
    driver.quit()
    
