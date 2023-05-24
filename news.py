from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd

url = 'https://dados.gov.br/home'
datas = []

while True:
    search = str(input('O que deseja pesquisar no portal Gov.br? ')).strip().lower()
    if search:
        break

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

driver.get(url)
wait = WebDriverWait(driver, 10)                                       

input_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="search2"]')))
btn_element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/section/div/div/div[1]/div/div/div/div/button')))
input_element.send_keys(search)
btn_element.click()
sleep(4)

soup = BeautifulSoup(driver.page_source, 'html.parser')
not_found = soup.find('span', attrs={'class': 'col-12 text-center'}).find('h3')
values = soup.find_all('div', attrs={'class': 'd-flex flex-column justify-content-between dataset-card'})

if not not_found:
    for value in values:
        title = value.find('h4', attrs={'class': 'text-capitalize'})
        descrition = value.find('span', attrs={'class': 'line-clamp-3 overflow-scroll fw-light text-break'}).find('p')
        link = value.find('div', attrs={'class':'pt-3 px-3 dataset-card-text'}).find('a')
        
        if descrition:
            datas.append([title.text, descrition.text, 'https://dados.gov.br' + link.get('href')])
        else:
            datas.append([title.text, '', 'https://dados.gov.br' + link.get('href')])

    news = pd.DataFrame(datas, columns=['Titulo', 'Descrição', 'Link'])
    news.to_csv('dados_gov.csv', index=False)
else:
    print(not_found.text)


