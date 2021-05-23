
!pip install selenium
!apt-get update # to update ubuntu to correctly run apt install
!apt install chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /usr/bin
import sys
import time
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')

from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
wd = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
login_url='https://dashboard.ngrok.com/login'
wd.get(login_url)
wd.find_element_by_id('email').send_keys(username)
wd.find_element_by_id('password').send_keys(password)
wd.find_element_by_xpath("//button[@type='submit']").click()
time.sleep(5)
tags=wd.find_elements_by_tag_name('code')

for i in tags:
    if 'authtoken' in str(i.text):
        result=str(i.text).split()[-1]
        print(result)
        file = open('token.txt','w')
        file.write(result)
        file.close()
        token= result
        print(token)

!/ngrok authtoken token
