"""

python cli_arxiv  --main (url="", path_pdf="data/scraper/v1/pdf/", path_txt="data/scraper/v1/txt/", npage_max=1, tag="v1")



"""
import os
import time

import bs4
import fire
import requests
import tika
from tika import parser

tika.initVM()

page_count = 0
page_num = 1

print(os.getcwd() )

def main(url="", path_pdf="data/scraper/v1/pdf/", path_txt="data/scraper/v1/txt/", npage_max=1, tag="v1"):
    global page_num
    page_num = npage_max

    path_pdf= f"data/scraper/{tag}/pdf/" 
    path_txt= f"data/scraper/{tag}/txt/" 
    
    os.makedirs(path_pdf, exist_ok=True)
    os.makedirs(path_txt, exist_ok=True)

    print(f"PDF writing path: {path_pdf}\nTXT writing path: {path_txt}")
    print(f"Maximum number of pages to get: {npage_max}.")

    url_list = parse_main_page(url)
    list_len = len(url_list)
    print(f"URLs scraped. Total: {list_len}")

    for idx, url_data in enumerate(url_list, 1):
        process_url(url_data, idx, list_len, path_pdf=path_pdf, path_txt=path_txt)


def parse_main_page(url):
    print(f"Trying to read URL {url}...")
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Cannot read URL {url}.")
        response.raise_for_status()

    response_soup = bs4.BeautifulSoup(response.content, "html.parser")
    url_list = []

    for url_data in process_and_paginate_soup(response_soup):
        url_list.append(url_data)

    return url_list


def process_and_paginate_soup(response_soup):
    global page_count
    page_count += 1

    def _extract_url():
        for element in response_soup.find_all("li", {"class": "arxiv-result"}):
            try:
                pdf_link_element = element.div.p.span.a
                if pdf_link_element.text.strip() != "pdf":
                    continue
                pdf_link = pdf_link_element["href"]
            except (TypeError, AttributeError):
                continue
            title = element.find("p", {"class": "title"}).text.strip()

            yield pdf_link, title

    for url_data in _extract_url():
        yield url_data

    print(f"Scraping PDF URLs from page {page_count}...")
    if page_count == page_num:
        return

    next_page = response_soup.find("a", {"class": "pagination-next"})
    if next_page:
        time.sleep(0.25)

        next_content = requests.get(f'https://arxiv.org{next_page["href"]}').content
        next_soup = bs4.BeautifulSoup(next_content, "html.parser")

        for url_data in process_and_paginate_soup(next_soup):
            yield url_data


def process_url(url_data, idx, list_len, path_pdf="", path_txt=""):
    page_url, page_title = url_data
    page_title = page_title.replace("/", "\u2215")

    print(f"Processing PDF {idx} of {list_len}.")
    print(f'Scraping "{page_title}" from URL {page_url}...')
    try:
        pdf_data = requests.get(f"{page_url}.pdf").content
        with open(os.path.join(path_pdf, f"{page_title}.pdf"), "wb") as pdf:
            pdf.write(pdf_data)
            file_data = parser.from_file(pdf.name)
            text = file_data["content"]
        with open(os.path.join(path_txt, f"{page_title}.txt"), "w") as out_file:
            out_file.write(text)
    except:
        print(f"Bad or unavailable PDF file from URL {page_url}. Skipping...")


if __name__ == "__main__":
    fire.Fire(main)
