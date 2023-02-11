
"""
Please put the following line in the powershell if the prints do not displays correctly :

            reg add HKEY_CURRENT_USER\Console /v VirtualTerminalLevel /t REG_DWORD /d 1

"""

import numpy as np
import pandas as pd
import time
import re
import sys
from cool_terminal import *
from selenium import webdriver
from bs4 import BeautifulSoup
test_mode = False

# Link to the web page with the achievements as a function of the parameters 
# used by the main page to access it
achievements_url = lambda code_array : f"https://fs-world.org/p{code_array[0]}.php?u={code_array[1]}&c={code_array[2]}"


###################
##### PRINTS ######
###################
t0 = time.time()
sys.stdout.write(esc_code("hide cursor"))
print("\n ------ Begin Scrapping fs-world.org ------\n")


#########################
##### OPEN FIREFOX ######
#########################

if not test_mode :
    # set webdriver to use Firefox
    driver = webdriver.Firefox()

    # get a page, pass it to beautifulsoup and closing the web browser
    driver.get("https://fs-world.org/E/#")
    page = BeautifulSoup(driver.page_source, features="html.parser")

else :
    with open("WRL - Formula Student Electric.html", encoding="utf8") as file:
        page = BeautifulSoup(file, features="html.parser")


##################################################
##### FIND THE RIGHT TABLE AND EXTRACT ROWS ######
##################################################


#find all 4 WRL tables
all_WRL_tables = page.find_all('div', attrs={'class':'column wrl'})

# find the right table by finding the one with the right title
for table in all_WRL_tables:
    table_title = table.find('h2')
    if table_title != None :
        if table_title.string[1:7] == "WRL ID" :
            ranking_table = table.tbody
            break

# get all the rows of the table (including the header)
rows = ranking_table.find_all('tr')
nb_teams = len(rows)-1 # -1 because we don't wanna count the header


##################################
##### ITERATE THROUGH TEAMS ######
##################################

rank = []
world_points = []
uni_name = []
nb_compet = []
year_first_compet = []

for row in rows :
    # get every cells of this row
    cells = row.find_all('td')

    # First row is the header and does not have a 'td' field
    # The followin lines skips this row
    if cells == [] :
        continue

    # add all the data on this page
    rank.append(int( cells[0].contents[0] ))
    world_points.append( float(cells[1].contents[0].contents[0].replace(',','.')) )
    uni_name.append( cells[3].contents[0].contents[0] )
    codes = re.findall(r'\d+', cells[5].contents[0].attrs['onclick'])

    if not test_mode :
        # get achivement page
        driver.get(achievements_url(codes))
        achievements_page = BeautifulSoup(driver.page_source, features="html.parser")
        uni_name_achievements_page = achievements_page.find('strong').contents[0]
        #check if we are on the right achievement page
        if uni_name[-1] != uni_name_achievements_page :
            print(esc_code("clear line"),esc_code("left",1000),f" !!! WARNING : uni name '{uni_name[-1]}' (rank {str(rank[-1])}) does not correspond to the achievement page name ('{uni_name_achievements_page}')")
        # extract its data
        rows_achiev = achievements_page.find_all('tr')
        nb_compet.append( int(re.findall(r'\d+', rows_achiev[-1].td.contents[0])[0]) )
        year_first_compet.append( int(re.findall(r'\d+', rows_achiev[-2].td.contents[0])[0]) )
    
    else :
        nb_compet.append(0)
        year_first_compet.append(0)

    # updates the progess bar
    progess_bar(rank[-1], nb_teams,"Teams")


###################
##### PRINTS ######
###################

# reset the hidden cursor
sys.stdout.write(COLOR["HEADER"]+f"\nTime Taken : {int(time.time()-t0)} sec"+COLOR["ENDC"])
sys.stdout.write(esc_code("disp cursor"))

##########################
##### CLOSE FIREFOX ######
##########################
if not test_mode :
    driver.close()

##########################
##### PANDAS BEGINS ######
##########################

data_matrix = np.matrix([uni_name, world_points, nb_compet, year_first_compet]).T
np.save("./data_matrix", data_matrix)

data = pd.DataFrame(np.matrix([uni_name, world_points, nb_compet, year_first_compet]).T,
                     columns=["uni_name","points", "nb_compet","first year"],
                     index=rank)



print("\n\n", data)
print("------ Done ------")

