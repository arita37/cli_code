import os
import time
import urllib.parse

import bs4
import fire
import requests
import requests.utils
from dataclasses import dataclass


@dataclass
class URLData:
    title: str
    url: str
    post_id: str

    def fixed_post_id(self):
        return f"t3_{self.post_id}"

    def completed_url(self):
        return f"http://old.reddit.com{self.url}"

    def new_url(self):
        return f"http://www.reddit.com{self.url}"

    def sanitized_title(self):
        return self.title.replace("/", "\u2215")


class RedditPageScraper:
    def __init__(self, path_txt):
        self.url_list = []
        self.path_txt = path_txt

    def parse(self, url, nposts):
        page_count = 0
        while nposts > 0:
            url = self.replace_url(url, page_count)
            response = self.request(url)

            if response.status_code != 200:
                print(f"Cannot read URL {url}")
                response.raise_for_status()

            response_soup = bs4.BeautifulSoup(response.content, "html.parser")
            for link in response_soup.find_all("a", {"class": "title"}):
                if not link["href"].startswith("/"):
                    continue
                self.url_list.append(URLData(title=link.text.strip(), url=link["href"], post_id=link['href'].split('comments/')[1].split("/")[0]))
                nposts -= 1
                if nposts <= 0:
                    break

            page_count += 1

        return self.url_list

    def extract(self, url_data: URLData):
        print(f'Scraping "{url_data.sanitized_title()}" from {url_data.new_url()}')
        page_content = self.request(url_data.completed_url()).content
        page_soup = bs4.BeautifulSoup(page_content, "html.parser")
        text_data = page_soup.find("div", {"class": "usertext-body"}).text.strip()
        with open(os.path.join(self.path_txt, url_data.sanitized_title()), 'w') as out_file:
            out_file.write(text_data)

    def request(self, url):
        print(f'REQUESTING URL {url}')
        time.sleep(2)
        headers = requests.utils.default_headers()
        headers.update(
            {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0",}
        )
        return requests.get(url, headers=headers)

    def replace_url(self, url, page_count):
        url = url.replace("www", "old")
        if page_count > 0:
            last_post_id = self.url_list[-1].fixed_post_id()
            return urllib.parse.urljoin(url, f"?count={page_count * 25}&after={last_post_id}")
        return url


class RedditScraper:
    def __init__(self, url="", nposts=20, path_txt=""):
        self.url = url
        self.nposts = nposts
        self.path_txt = path_txt

        self.page_parser = RedditPageScraper(self.path_txt)

        print(f"TXT writing path: {self.path_txt}")
        print(f"Number of posts to get: {self.nposts}")
        print(f"Trying to read URL {url}...")

    def run(self):
        post_url_list = self.page_parser.parse(self.url, self.nposts)
        post_url_list_len = len(post_url_list)
        for idx, url_data in enumerate(post_url_list, 1):
            print(f"Processing post {idx} of {post_url_list_len}")
            self.page_parser.extract(url_data)


if __name__ == "__main__":
    fire.Fire(RedditScraper)
