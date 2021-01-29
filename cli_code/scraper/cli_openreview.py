import os

import fire
import requests
import tika
from dataclasses import dataclass
from tika import parser

tika.initVM()


@dataclass
class URLData:
    title: str
    url: str

    def title_normalized(self) -> str:
        return self.title.strip().replace("/", "\u2215")

    def pdf_title(self) -> str:
        return f"{self.title_normalized()}.pdf"

    def txt_title(self) -> str:
        return f"{self.title_normalized()}.txt"


class PageParser:
    def __init__(self):
        self.url_list = []
        self.page_count = 0

    def parse(self, url, page_limit):
        api_url = self.construct_api_url(url)
        print(f"API URL: {api_url}")
        initial_response = requests.get(api_url)

        if initial_response.status_code != 200:
            print(f"Cannot read URL {url}")
            initial_response.raise_for_status()

        self.url_list.extend(self.process_api_response(initial_response))

        self.page_count += 1
        current_url = api_url
        print(f"Scraping PDF URLs from page {self.page_count}...")

        while self.page_count < page_limit:
            current_url = self.generate_next_url(current_url)
            response = requests.get(current_url)
            self.url_list.extend(self.process_api_response(response))
            self.page_count += 1
            print(f"Scraping PDF URLs from page {self.page_count}...")

        return self.url_list

    def construct_api_url(self, url):
        needle = url.replace("https://openreview.net/group?id=", "")
        return f"""https://api.openreview.net/notes?invitation={needle}/-/Blind_Submission&details=replyCount%2Cinvitation%2Coriginal&includeCount=true&offset=0&limit=50"""

    def process_api_response(self, response):
        response_data = response.json()
        if not response_data.get("notes"):
            return
        result = []
        for note in response_data["notes"]:
            result.append(URLData(title=note["content"]["title"], url=self.construct_pdf_url(note)))
        return result

    def generate_next_url(self, current_url):
        new_url = current_url.split("offset")[0]
        new_url = f"{new_url}&offset={50 * self.page_count}&limit=50"
        return new_url

    @staticmethod
    def construct_pdf_url(note):
        return f"https://openreview.net/pdf?id={note['id']}"


class PDFExtractor:
    def __init__(self, pdf_path, txt_path):
        self.pdf_path = pdf_path
        self.txt_path = txt_path

    def extract(self, url_data: URLData):
        print(f'Scraping "{url_data.title_normalized()}" from URL {url_data.url}...')
        pdf_data = requests.get(url_data.url).content
        with open(os.path.join(self.pdf_path, url_data.pdf_title()), "wb") as pdf:
            pdf.write(pdf_data)
            text_data = parser.from_file(pdf.name)["content"]
        with open(os.path.join(self.txt_path, url_data.txt_title()), "w") as out_file:
            out_file.write(text_data)


class OpenreviewScraper:
    page_parser = PageParser()

    def __init__(self, url="", npage_max=1, path_pdf="", path_txt=""):
        self.url = url
        self.npage_max = npage_max
        self.path_pdf = path_pdf
        self.path_txt = path_txt

        self.pdf_extractor = PDFExtractor(pdf_path=path_pdf, txt_path=path_txt)

        print(f"PDF writing path: {self.path_pdf}\nTXT writing path: {self.path_txt}")
        print(f"Maximum number of pages to get: {self.npage_max}")
        print(f"Trying to read URL {url}...")

    def run(self):
        url_list = self.page_parser.parse(self.url, self.npage_max)
        url_list_len = len(url_list)
        for idx, url_data in enumerate(url_list, 1):
            print(f"Processing PDF {idx} of {url_list_len}")
            self.pdf_extractor.extract(url_data)


if __name__ == "__main__":
    fire.Fire(OpenreviewScraper)


