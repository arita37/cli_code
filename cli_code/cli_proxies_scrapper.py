"""
A simple commandline script to gather a list of fresh proxies across multiple sources on the web.
A list of all available sources can be checked in the help menue of the utility. 
You can choose one, many and all sources to gather proxies.

Usage:

cli_proxies_scrapper -l 

cli_proxies_scrapper -s ssl us -o p_list.txt
"""

import sys
import traceback
from re import findall, sub

import argparse
import requests
from requests.exceptions import ConnectionError


class ScrapperException(BaseException):
    pass


class Proxies(object):
    """
    Proxies is the response data type of getProxies function
    """

    def __init__(self, proxies, category):
        """
        Initialize the proxies class
        :param proxies: is the list of proxies.
        :param category: is the category for proxies.
        """
        self.proxies = proxies
        self.len = len(proxies)
        self.category = category


class Proxy(object):
    """
    Proxy is the class for proxy.
    """

    def __init__(self, ip, port):
        """
        Initialization of the proxy class
        :param ip: ip address of proxy
        :param port: port of proxy
        """
        self.ip = ip
        self.port = port


class Scrapper:
    """
    Scrapper class is use to scrape the proxies from various websites.
    """

    SSL = 'https://www.sslproxies.org/'
    GOOGLE = 'https://www.google-proxy.net/'
    ANANY = 'https://free-proxy-list.net/anonymous-proxy.html'
    UK = 'https://free-proxy-list.net/uk-proxy.html'
    US = 'https://www.us-proxy.org/'
    NEW = 'https://free-proxy-list.net/'
    SPYS_ME = 'http://spys.me/proxy.txt'
    PROXYSCRAPE = 'https://api.proxyscrape.com/?request=getproxies&proxytype=all&country=all&ssl=all&anonymity=all'
    PROXYNOVA = 'https://www.proxynova.com/proxy-server-list/'
    PROXYLIST_DOWNLOAD_HTTP = 'https://www.proxy-list.download/HTTP'
    PROXYLIST_DOWNLOAD_HTTPS = 'https://www.proxy-list.download/HTTPS'
    PROXYLIST_DOWNLOAD_SOCKS4 = 'https://www.proxy-list.download/SOCKS4'
    PROXYLIST_DOWNLOAD_SOCKS5 = 'https://www.proxy-list.download/SOCKS5'
    ALL = 'ALL'

    def __init__(self, category='SSL', print_err_trace=False):
        """
        Initialization of scrapper class
        :param category: Category of proxy to scrape.
        :param print_err_trace: (True or False) are you required the stack trace for error's if they occured in the program
        """
        # init with Empty Proxy List
        self.proxies = []
        self.category = category.upper()
        self.Categories = {
            'SSL': self.SSL,
            'GOOGLE': self.GOOGLE,
            'ANANY': self.ANANY,
            'UK': self.UK,
            'US': self.US,
            'NEW': self.NEW,
            'SPYS.ME': self.SPYS_ME,
            'PROXYSCRAPE': self.PROXYSCRAPE,
            'PROXYNOVA': self.PROXYNOVA,
            'PROXYLIST_DOWNLOAD_HTTP': self.PROXYLIST_DOWNLOAD_HTTP,
            'PROXYLIST_DOWNLOAD_HTTPS': self.PROXYLIST_DOWNLOAD_HTTPS,
            'PROXYLIST_DOWNLOAD_SOCKS4': self.PROXYLIST_DOWNLOAD_SOCKS4,
            'PROXYLIST_DOWNLOAD_SOCKS5': self.PROXYLIST_DOWNLOAD_SOCKS5,
            'ALL': self.ALL
        }
        self.print_trace = print_err_trace

    def getProxies(self):
        """
        getProxies() gives the proxies scrapped from websites.
        :return: the object of proxies class
        """
        if self.Categories[self.category] == 'ALL':
            for Cat in self.Categories:
                # Skip iteration for ALL category
                if Cat == 'ALL':
                    continue

                self.category = Cat
                self.proxies += self._get()
            self.category = 'ALL'
            self.filter_proxies_remove_duplicates()
        else:
            self.proxies = self._get()
        self.proxies = [Proxy(proxy.split(':')[0], proxy.split(':')[1])
                        for proxy in self.proxies]
        return Proxies(proxies=self.proxies, category=self.category)

    def _get(self):
        """
        _get() is the actual scrapper to scrape proxies by REGEX.
        :return: returns the list of proxies according to the category of proxies
        """
        try:
            r = requests.get(url=self.Categories[self.category])
            if self.category == 'SPYS.ME' or self.category == 'PROXYSCRAPE':
                proxies = findall(
                    pattern=r'\d+\.\d+\.\d+\.\d+:\d+', string=r.text)
            elif self.category == 'PROXYNOVA':
                matches = findall(
                    pattern=r'\d+\.\d+\.\d+\.\d+\'\)\;</script>\s*</abbr>\s*</td>\s*<td\salign=\"left\">\s*\d+',
                    string=r.text)
                proxies = [sub(r"\'\)\;</script>\s*</abbr>\s*</td>\s*<td\salign=\"left\">\s*", ":", m) for m in
                           matches]
            elif self.category in {'PROXYLIST_DOWNLOAD_HTTP', 'PROXYLIST_DOWNLOAD_HTTPS',
                                   'PROXYLIST_DOWNLOAD_SOCKS4', 'PROXYLIST_DOWNLOAD_SOCKS5'}:
                matches = findall(
                    pattern=r'\d+\.\d+\.\d+\.\d+</td>\s*<td>\d+', string=r.text)
                proxies = [sub(r"</td>\s*<td>", ":", m) for m in matches]
            else:
                matches = findall(
                    pattern=r'\d+\.\d+\.\d+\.\d+</td><td>\d+', string=r.text)
                proxies = [m.replace('</td><td>', ':') for m in matches]
            return proxies
        except ConnectionError:
            print('Connection Error in getting SSL Proxies')
            if self.print_trace:
                print(traceback.format_exc())
            return []

    def filter_proxies_remove_duplicates(self):
        """
        filter_proxies_remove_duplicates() is the filter for the proxy list. To get the unique proxies it just get
        the LIST of proxies from self object convert it to SET and then convert to LIST.

        :return: Update the UNIQUE LIST of proxies.
        """
        self.proxies = list(set(self.proxies))


__author__ = "Sameer Narkhede"
__copyright__ = "Copyright (C) 2020 Sameer Narkhede"
__license__ = "MIT LICENCE"
__version__ = "0.1.0"


def get_arguments():
    p = argparse.ArgumentParser(
        description="Gather proxies from a list of online, freely available sources")

    p.add_argument("--source", "-s", default=None, nargs='*',
                   help="Specify one or multiple sources from the available sources list")
    p.add_argument("--list", "-l", action="store_true",
                   help="Show a list of available sources")
    p.add_argument("--dir_out", "-o", default="proxies_list.txt",
                   help="Output file name to store all the proxies")

    args = p.parse_args()
    return args


if __name__ == "__main__":

    args = get_arguments()

    if args.list:
        print("""Use key(s) from the following key list (case insensitive) as a source parameter.
            PROXYLIST_DOWNLOAD_HTTP     :   https://www.proxy-list.download/HTTP
            PROXYLIST_DOWNLOAD_HTTPS    :   https://www.proxy-list.download/HTTPS
            PROXYLIST_DOWNLOAD_SOCKS4   :   https://www.proxy-list.download/SOCKS4
            PROXYLIST_DOWNLOAD_SOCKS5   :   https://www.proxy-list.download/SOCKS5
            SSL           :   https: //www.sslproxies.org/
            GOOGLE        :   https://www.google-proxy.net/
            ANANY         :   https://free-proxy-list.net/anonymous-proxy.html
            UK            :   https://free-proxy-list.net/uk-proxy.html
            US            :   https://www.us-proxy.org/
            NEW           :   https://free-proxy-list.net/
            SPYS_ME       :   http://spys.me/proxy.txt
            PROXYSCRAPE   :   https://api.proxyscrape.com/?request=getproxies&proxytype=all&country=all&ssl=all&anonymity=all
            PROXYNOVA     :   https://www.proxynova.com/proxy-server-list/
            ALL           :   For all sources combined""")

    if args.source != None:
        categories = [cat.lower() for cat in args.source]

        if 'all' not in categories:
            p_list = []
            for cat in categories:
                # initialize the scrapper with given category
                scrapper = Scrapper(category=cat, print_err_trace=False)

                # Get the proxies from this source
                data = scrapper.getProxies()

                # Print these scrapped proxies
                print(f"Obtained {data.len} proxies from {data.category}")

                for item in data.proxies:
                    p_list.append("{}:{}".format(item.ip, item.port))
                    # print("{}:{}".format(item.ip, item.port))

            with open(args.dir_out, "w") as out_file:
                for proxy in p_list:
                    out_file.write(proxy)
                    out_file.write("\n")
        else:
            # initialize the scrapper with given category
            scrapper = Scrapper(category='ALL', print_err_trace=False)

            # Get the proxies from this source
            data = scrapper.getProxies()

            # Print these scrapped proxies
            print(f"Obtained {data.len} proxies from {data.category} source.")

            with open(args.dir_out, "w") as out_file:
                for item in data.proxies:
                    out_file.write("{}:{}".format(item.ip, item.port))
                    out_file.write("\n")

    else:
        print("Please specify a source. use '-l' flag to see a list of all sources.")
