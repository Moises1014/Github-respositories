import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

#Gets the User Id 
gitID = input('Please enter a github ID to get the user repositories: ')

driver = webdriver.Chrome(options=chrome_options)
#url needed to get to the users github
url = "https://github.com/"+gitID+"?tab=repositories"
#start the google chrome
driver.get(url)
#gets number of elements in page(repositories)
numberofrep = driver.find_elements_by_class_name('wb-break-all')
#number of repositories
repos = len(numberofrep)
#list to save all information initialized
repo_list = []

#gets all repositories in first page
for i in range(1, repos + 1):
  #must be string to put to xpath
  repnumb = str(i)
  #get Name of repository
  name = driver.find_element_by_xpath('//*[@id="user-repositories-list"]/ul/li['+repnumb+']/div[1]/div[1]/h3/a').text
  #get language for repository, but only if there is one
  try:
    Code_lang = driver.find_element_by_xpath('//*[@id="user-repositories-list"]/ul/li['+repnumb+']/div[1]/div[3]/span/span[2]').text
    code_lang = Code_lang 
  except NoSuchElementException:
    code_lang= "None"
  
  #get Description for repository, but only if there is one
  try:
    Desc = driver.find_element_by_xpath('//*[@id="user-repositories-list"]/ul/li['+repnumb+']/div[1]/div[2]/p').text
    desc = Desc 
  except NoSuchElementException:
    desc= "None"
  #get link for repository
  repolink = driver.find_element_by_xpath('//*[@id="user-repositories-list"]/ul/li['+repnumb+']/div[1]/div[1]/h3/a').get_attribute('href')
  #makes new row
  repo_items={
    'Name:' : name,
    'Language:' : code_lang,
    'Description:': desc,
    'Link:' : repolink
  }
  #add the row to the list
  repo_list.append(repo_items)
#put list in rigth data Frame
df = pd.DataFrame(repo_list)
#put info in csv file
df.to_csv('Repositories.csv', sep="|")
#close drive
driver.close()

