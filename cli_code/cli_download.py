"""
This script automates downloading of bulk files from github, google drive and dr0pbox. 
You can either provide a single url or a file containg multiple urls,
 one per line and an optional directory to store download results.

Usage:

`cli_download -u a_valid_url`

`cli_download -f /path/to/a_valid_urls_file -o my_download_dir`

`-u` or `--url` specify a valid url for the file to download
`-f` or `--file` specify path to a file containing a list of valid urls, one per line
`-o` or `--dir_out` specify the output directory (default is `downloaded`)

What is a valid url?

- Github - Url of a _file_ in a github repo e.g., `https://github.com/Chhekur/amazon-scraper/blob/master/README.md`
- Google Drive -    Share link of a file on google drive (share setting must be set 
                    to `anyone with the link`) e.g., `https://drive.google.com/file/d/1FPn4Q4PClobHgEU4DglyF2Xbs5Boe1r_/view?usp=sharing`
- Dropbox - TO BE TESTED, DON't OWN A DROPBOX ACCOUNT
"""
import cgi
import os
import re
import uuid
import argparse

import requests


class Downloader:

    GITHUB_NETLOC = 'github.com'
    GITHUB_RAW_NETLOC = 'raw.githubusercontent.com'

    GDRIVE_NETLOC = 'drive.google.com'
    GDRIVE_LINK_TEMPLATE = 'https://drive.google.com/u/0/uc?id={fileid}&export=download'

    DROPBOX_NETLOC = 'dropbox.com'

    DEFAULT_FILENAME = uuid.uuid4().hex  # To provide unique filename in batch jobs

    def __init__(self, url):
        """Make path adjustments and parse url"""
        self.url = url
        self.parsed = requests.utils.urlparse(url)

        self.clean_netloc()

        if not self.parsed.netloc:
            raise ValueError('Wrong URL (Make sure "http(s)://" included)')

        self.adjust_url()

    def clean_netloc(self):
        clean_netloc = re.sub(r'^www\.', '', self.parsed.netloc)
        self.parsed = self.parsed._replace(netloc=clean_netloc)

    def adjust_url(self):
        if self.parsed.netloc == self.GITHUB_NETLOC:
            self._transform_github_url()
        elif self.parsed.netloc == self.GDRIVE_NETLOC:
            self._transform_gdrive_url()
        elif self.parsed.netloc == self.DROPBOX_NETLOC:
            self._transform_dropbox_url()

    def _transform_github_url(self):
        """Github specific changes to get link to raw file"""
        self.url = (
            self.url
            .replace('/blob/', '/')
            .replace(self.GITHUB_NETLOC, self.GITHUB_RAW_NETLOC)
        )

    def _transform_gdrive_url(self):
        """GDrive specific changes to get link to raw file"""
        fileid = self.parsed.path.replace('/file/d/', '').split('/')[0]
        self.url = self.GDRIVE_LINK_TEMPLATE.format(fileid=fileid)

    def _transform_dropbox_url(self):
        """DropBox specific changes to get link to raw file"""
        self.url = requests.utils.urlunparse(
            self.parsed._replace(query='dl=1'))

    def get_filename(self, headers):
        """Attempt to get filename from content-dispositions header.

        If not found: get filename from parsed path
        If both fail: use DEFAULT_FILENAME to save file
        """
        header = headers.get('content-disposition')

        if header is not None:
            _, params = cgi.parse_header(header)
            filename = params.get('filename')
        else:
            try:
                filename = self.parsed.path.split('/')[-1]
            except IndexError:
                filename = None

        return filename if filename is not None else self.DEFAULT_FILENAME

    def download(self, filepath=''):
        '''Downloading and saving file'''

        if not os.path.exists(filepath):
            os.mkdir(filepath)

        response = requests.get(self.url)
        filename = self.get_filename(response.headers)

        full_filename = os.path.join(filepath, filename)

        if response.status_code == 200:
            with open(full_filename, "wb") as f:
                f.write(response.content)

            print(f'File saved as {full_filename}')
        else:
            print('Bad request')


def get_arguments():
    a_p = argparse.ArgumentParser(
        "Download content from github, googledrive and/or drop-box with a single url or list of urls in a file.")
    a_p.add_argument("--url", "-u", default="",
                     help="Url of the file to download, it must start with http(s)://'")
    a_p.add_argument("--file", "-f", default="",
                     help="File containing valid urls of objects to download.")
    a_p.add_argument("--dir_out", "-o", default="downloaded",
                     help="Directory to save downloaded files.")
    args = a_p.parse_args()

    return args


def main():
    args = get_arguments()

    if args.url != "":
        downloader = Downloader(args.url)
        downloader.download(args.dir_out)

    if args.file != "":
        urls = []
        try:
            with open(args.file, "r") as rf:
                for url in rf.readlines():
                    urls.append(url.strip())
        except FileNotFoundError:
            print(f"No such file {args.file} found")

        for url in urls:
            downloader = Downloader(url)
            downloader.download(args.dir_out)


if __name__ == "__main__":
    main()
    print("print all downloading completed!")
