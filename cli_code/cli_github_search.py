# About: Search & Scrape GitHub repositories
"""
Search on github for keyword(s) with optional parameters to refine your search and get all results in a CSV file.

Usage:

`cli_github_search amazon scraper`

or refine your search

`cli_github_search keyword1 keyword2 -c >2019-11-10 -p 2019-11-01..2019-11-10 -o results`

These are optional arguments:

`-c` or `--created` specify the period of repository creation
`-p` or `--pushed` specify the period of pushing to repo
`-o` or `--dir_out` specify the output folder for storing results (default value is `results`)
"""

import os
import argparse
import time
from datetime import datetime
import re

import requests
from bs4 import BeautifulSoup
import pandas as pd


def search_github(args, start_time):
    keywords = args.keyword
    created = args.created
    pushed = args.pushed
    folder_name = args.dir_out
    # print('Keyword to search GitHub: ' + keyword)
    # print('Created: ' + created)
    # print('Pushed: ' + pushed)

    df = pd.DataFrame()
    type = 'Repositories'

    # TODO: I beleive we can do better thean this
    if re.match(r'[<>]\d{4}-\d{2}-\d{2}', created) or \
            re.match(r'[<>]=\d{4}-\d{2}-\d{2}', created) or \
            re.match(r'\d{4}-\d{2}-\d{2}..\d{4}-\d{2}-\d{2}', created):
        if re.match(r'[<>]=\d{4}-\d{2}-\d{2}', pushed) or \
                re.match(r'[<>]=\d{4}-\d{2}-\d{2}', pushed) or \
                re.match(r'\d{4}-\d{2}-\d{2}..\d{4}-\d{2}-\d{2}', pushed):

            search_query = ''
            for word in keywords:
                search_query += word + '+'
            search_query += 'created%3A' + created + '+pushed%3A' + pushed

            #root_path = os.getcwd()
            root_url = 'https://github.com/search?'
            search_url = root_url + '&q=' + search_query + '&type=' + type
            print(search_url)
            header = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6)'
                ' AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/61.0.3163.100 Safari/537.36'}
            response = requests.get(search_url, headers=header)

            if response.status_code == 200:
                username = []
                repo_name, repo_url = [], []
                description = []
                update_info = []
                soup = BeautifulSoup(response.text, 'lxml')
                cont_pagination = soup.find(
                    'div', {'class': 'd-flex d-md-inline-block pagination'})
                if cont_pagination != None:
                    cont_links = cont_pagination.find_all('a')
                    pages_number = int(cont_links[-2].text)
                else:
                    pages_number = 1

                print('Number of pages: ' + str(pages_number))
                for page_number in range(pages_number):
                    # print(page_number + 1)
                    page_url = root_url + 'p=' + \
                        str(page_number+1) + '&q=' + \
                        search_query + '&type=' + type
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
                        cont_repos = soup1.find('ul', {'class': 'repo-list'})
                        if cont_repos != None:
                            repo_list = cont_repos.find_all('li')
                            # print(len(repo_list))
                            for repo in repo_list:
                                username.append(
                                    repo.find("div", attrs={"class": "f4"}).text.strip().split('/')[0])
                                repo_name.append(
                                    repo.find("div", attrs={"class": "f4"}).text.strip().split('/')[1])
                                repo_url.append(
                                    'github.com/' + repo.find("div", attrs={"class": "f4"}).text.strip())
                                description.append(
                                    repo.find("p", attrs={"class": "mb-1"}).text.strip())
                                update_info.append(
                                    repo.find('relative-time').text)
                        else:
                            print('No repos found for given keyword!')
                    else:
                        print('Page response: ' + str(response1.status_code))

                # Export on CSV
                filename = ""
                for word in keywords:
                    filename += word + '_'
                filename = filename[:-1] + "-" + \
                    datetime.now().strftime("%Y%m%d") + ".csv"

                try:
                    os.makedirs(folder_name)
                except OSError:
                    pass

                df['Username'] = username
                df['Repository'] = repo_name
                df['Description'] = description
                df['Link'] = repo_url
                df['Updated'] = update_info
                df.to_csv(folder_name + "/" + filename, index=False)
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
    return df


def get_arguments():
    # TODO: Improve default arguments
    p = argparse.ArgumentParser(
        description='Searches github for given keywords and specified parameters and store resutls in a directory.')
    p.add_argument(
        'keyword', nargs='*', help="Keyword to search in format: 'keyword1 keyword2 keyword3...'")
    p.add_argument(
        '--created', '-c', default='>2018-11-01', help="Created date in format: '<=YYYY-MM-DD' or '>=YYYY-MM-DD' or 'YYYY-MM-DD..YYYY-MM-DD'")
    p.add_argument(
        '--pushed', '-p', default='2018-11-01..2020-11-10', help="Pushed date in format: '<=YYYY-MM-DD' or '>=YYYY-MM-DD' or 'YYYY-MM-DD..YYYY-MM-DD'")
    p.add_argument('--dir_out', '-o', default='results',
                   help="Folder to store the results of your search")
    args = p.parse_args()

    return args


def main():
    start_time = time.time()
    args = get_arguments()
    search_github(args, start_time)


if __name__ == "__main__":
    main()
