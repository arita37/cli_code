
# About: Search & Scrape GitHub repositories
# Version: 1.0
# Date: November, 2019

import os
import argparse
import sys
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import pandas as pd
import re

start_time = time.time()

my_parser = argparse.ArgumentParser(description='===============USAGE HELP===============')
my_parser.add_argument('keyword', help="Keyword to search in format: 'keyword1 keyword2 keyword3...'")
my_parser.add_argument('created', help="Created date in format: '<=YYYY-MM-DD' or '>=YYYY-MM-DD' or 'YYYY-MM-DD..YYYY-MM-DD'")
my_parser.add_argument('pushed', help="Pushed date in format: '<=YYYY-MM-DD' or '>=YYYY-MM-DD' or 'YYYY-MM-DD..YYYY-MM-DD'")
# my_parser.add_argument('folder', help="Pushed date in format: '<=YYYY-MM-DD' or '>=YYYY-MM-DD' or 'YYYY-MM-DD..YYYY-MM-DD'")
args = my_parser.parse_args()
#
# print('Script name: ' + sys.argv[0])
keyword = sys.argv[1]
created = sys.argv[2]
pushed = sys.argv[3]
# print('Keyword to search GitHub: ' + keyword)
# print('Created: ' + created)
# print('Pushed: ' + pushed)

df = pd.DataFrame()
type = 'Repositories'
# keyword = 'vae'
# created = '>2019-11-10'
# pushed = '2019-11-01..2019-11-10'

if re.match('[<>]\d{4}-\d{2}-\d{2}', created) or \
        re.match('[<>]=\d{4}-\d{2}-\d{2}', created) or \
        re.match('\d{4}-\d{2}-\d{2}..\d{4}-\d{2}-\d{2}', created):
    if re.match('[<>]=\d{4}-\d{2}-\d{2}', pushed) or \
            re.match('[<>]=\d{4}-\d{2}-\d{2}', pushed) or \
            re.match('\d{4}-\d{2}-\d{2}..\d{4}-\d{2}-\d{2}', pushed):

        keyword = keyword.split()
        search_query = ''
        if len(keyword) > 1:
            for word in keyword[:-1]:
                search_query += word + '+'
        search_query += keyword[-1]
        search_query += '+created%3A' + created + '+pushed%3A' + pushed

        root_path = os.getcwd()
        root_url = 'https://github.com/search?'
        search_url = root_url + '&q=' + search_query + '&type=' + type
        print(search_url)
        response = requests.get(search_url,
                                            headers={
                                                    'User-Agent':   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6)'
                                                                    ' AppleWebKit/537.36 (KHTML, like Gecko) '
                                                                    'Chrome/61.0.3163.100 Safari/537.36'})
        if response.status_code == 200:
            username = []
            repo_name, repo_url = [], []
            description = []
            update_info = []
            soup = BeautifulSoup(response.text, 'lxml')
            cont_pagination = soup.find('div', {'class': 'd-flex d-md-inline-block pagination'})
            if cont_pagination != None:
                cont_links = cont_pagination.find_all('a')
                pages_number = int(cont_links[-2].text)
            else:
                pages_number = 1
            
            print('Number of pages: ' + str(pages_number))
            for page_number in range(pages_number):
                # print(page_number + 1)
                page_url = root_url + 'p=' + str(page_number+1) + '&q=' + search_query + '&type=' + type
                # print(page_url)
                time.sleep(10)
                response1 = requests.get(page_url,
                                         headers={
                                                 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6)'
                                                               ' AppleWebKit/537.36 (KHTML, like Gecko) '
                                                               'Chrome/61.0.3163.100 Safari/537.36'})
                if response1.status_code == 200:
                    # print(response1)
            
                    soup1 = BeautifulSoup(response1.text, 'lxml')
                    cont_repos = soup1.find('ul', {'class':'repo-list'})
                    if cont_repos != None:
                        repo_list = cont_repos.find_all('li')
                        # print(len(repo_list))
                        for repo in repo_list:
                            username.append(repo.div.h3.text.strip().split('/')[0])
                            repo_name.append(repo.div.h3.text.strip().split('/')[1])
                            repo_url.append('github.com/' + repo.div.h3.text.strip())
                            description.append(repo.div.p.text.strip())
                            update_info.append(repo.div.find('relative-time').text)
                    else:
                        print('No repos found for given keyword!')
                else:
                    print('Page response: ' + str(response1.status_code))


            ###### Export on CSV
            #folder_name = datetime.now().strftime("%Y-%m-%d")  + "_".join( keyword )
            filename = "_".join( keyword ) + "--" + datetime.now().strftime("%Y%m%d")   + ".csv"
            
            folder_name = "D:/_devs/Python01/gitdev/aapackage/zrepo/"
            try :
              os.makdirs(folder_name)
            except : pass

            df['Username'] = username
            df['Repository'] = repo_name
            df['Description'] = description
            df['Link'] = repo_url
            df['Updated'] = update_info
            df.to_csv(folder_name +  "/" + filename , index=False)
            print('written')
            df = df[0:0]

        else:
            print('Page response: ' + str(response.status_code))
    else:
        print('Pushed date wrong format.')
else:
    print('Created date wrong format.')

end_time = time.time()
print('Runtime: {0:.2f} seconds.'.format(end_time - start_time))