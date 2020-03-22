import cgi
import os
import re
import sys
import uuid

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
        self.url = requests.utils.urlunparse(self.parsed._replace(query='dl=1'))

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
            except:
                filename = None

        return filename if filename is not None else self.DEFAULT_FILENAME

    def download(self, filepath=''):
        '''Downloading and saving file'''
        response = requests.get(self.url)
        filename = self.get_filename(response.headers)

        full_filename = os.path.join(filepath, filename)

        if response.status_code == 200:
            with open(full_filename, 'wb') as f:
                f.write(response.content)

            print(f'File saved as {full_filename}')
        else:
            print('Bad request')

if __name__ == "__main__":

    args = sys.argv

    try:
        url = args[1]
        filepath = args[2]
    except IndexError:
        print('Make sure you pass the file URL')
        exit()

    print("Downloading", filepath)
    downloader = Downloader(url)
    downloader.download(filepath)
