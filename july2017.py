## imports

selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert 
import calendar
import datetime
import time

from json2xml import json2xml
from json2xml.utils import readfromjson

## functions

def author_block(soup):
            try:
                author = soup.find('div',attrs={'class':'_3Mkg- byline'}).text.split("|")[0].strip()
                if 'IST' in author:
                    author = 'NA'
            except:
                try:
                    author = soup.find('a',attrs={'class':'auth_detail'}).text
                except:
                    author = 'NA'
            return author


def date_block(soup):
            try:
                date = soup.find('div',attrs={'class':'_3Mkg- byline'}).text.split("|")[-1].strip()
            except:
                date = 'NA'
            return date


def des_block(soup):
    try:
        des = soup.find('div',attrs={'class':'ga-headlines'}).text
    except:
        try:
            des = soup.find('div',attrs={'class':'section1'}).text
        except:
            des = 'NA'
    return des


def headline_block(soup):
    try:
        head = soup.find('h1',attrs={'class':'_23498'}).text
    except:
        try:
            head = soup.find('h1',attrs={'class':'heading1'}).text
        except:
            head = 'NA'
    return head


def vertical_block(soup):
    try:
        vertical = soup.find_all('span',attrs={'itemprop':'name'})[1].text
    except:
        vertical = 'NA'
    return vertical


# main code

req_month = 'july'.title()
req_year = 2017

req_month_no = list(calendar.month_name).index(req_month)



opts = Options()

opts.add_argument("--headless")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-notifications")
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36")


driver = webdriver.Chrome(r"C:\Users\Admin\.wdm\drivers\chromedriver\win32\87.0.4280.88\chromedriver.exe",options=opts)  # set driver and options

url = f'https://timesofindia.indiatimes.com/archive/year-{req_year},month-{req_month_no}.cms'                                             # url 

driver.get(url)   
    
    
date_l,headline_l,des_l,author_l,vertical_l = [],[],[],[],[]
    

links = driver.find_elements_by_xpath("//td[@align='center']//a")

for link in links[9:]:    
    if link.get_attribute('text') != '':
        
        
        ########    set date block -> start    ########
        window_before = driver.window_handles[0]                                                            # get root tab

        ActionChains(driver).key_down(Keys.CONTROL).click(link).key_up(Keys.CONTROL).perform()        # open the link in new tab

        window_after = driver.window_handles[-1]                                                       

        driver.switch_to.window(window_after)
        
        
        #%%%%%%%%%%  iterate thorugh links of the selected date -> start  %%%%%%%%%%%%%%  
        
        for i in range(len(driver.find_elements_by_xpath("//tr/td/span/a"))):
            
            ActionChains(driver).move_to_element(driver.find_elements_by_xpath("//tr/td/span/a")[i]).click().perform()
            
            #driver.find_elements_by_xpath("//tr/td/span/a")[i].click()
            
            #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& get data block -> start &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
            
            time.sleep(3)

            sauce = driver.page_source                                           

            soup = BeautifulSoup(sauce)
            
            date_current = date_block(soup)
            date_l.append(date_current)
            
            author_current = author_block(soup)
            author_l.append(author_current)
            
            vertical_current = vertical_block(soup)
            vertical_l.append(vertical_current)
            
            headline_current = headline_block(soup)
            headline_l.append(headline_current)
            print(headline_current)
            
            des_current = des_block(soup)
            des_l.append(des_current)
                       
           
            #df = pd.DataFrame(list(zip(date_l,vertical_l,headline_l,author_l,des_l)),columns=['date','vertical','headline','author','description'])       
            #df.to_csv('patial_july_2k17_v1.csv')
            
            #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& get data block -> end   &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
                    

            driver.back()
            time.sleep(2)
            
            print(driver.title)
            
            
        df = pd.DataFrame(list(zip(date_l,vertical_l,headline_l,author_l,des_l)),columns=['date','vertical','headline','author','description'])       
        df.to_csv('july_2k17_v1.csv')
            
        #%%%%%%%%%%  iterate thorugh links of the selected date -> end    %%%%%%%%%%%%%%            
        
        driver.close()                                   # close the current driver ( the one with the opened link )
        
        driver.switch_to.window(window_before)
        
        ########    set date block -> end      ########
        

        
    else:
        pass

