#!/usr/bin/env python2.7
""" Print all of the (git/ssh or http) urls for all repos (public or
private+public with personal_token) in a GitHub account (user or organization).
Usage example::
    [HTTP_URLS=1] python2.7 list-all-repos.py account_name [personal_token]
It requires the pygithub3 module, which you can install on macos (Mac OSX) like this::
    # get pip if you don't have it
    sudo python -m ensurepip
    # In macos versions El Capitan and later, you must deal with System Integrity Protection
    pip2 install --user pygithub3
Advanced usage.  This will actually clone all the repos for a
GitHub organization or user::
    for url in $(python2.7 list-all-repos.py); do git clone $url; done
"""

import os
import sys
import pygithub3

gh = None


def gather_clone_urls(account, no_forks=True):
    try:
        all_repos = gh.repos.list_by_org(account, type='all').all()
    except pygithub3.exceptions.NotFound:
        all_repos = gh.repos.list(user=account).all()

    for repo in all_repos:

        # Don't print the urls for repos that are forks.
        if no_forks and repo.fork:
            continue

        if os.environ.get('HTTP_URLS'):
            yield repo.clone_url
        else:
            yield repo.ssh_url


if __name__ == '__main__':
    argc = len(sys.argv) - 1
    if argc < 1:
        print "Usage: [HTTP_URLS=1] python2.7 {} account_name [personal_token]".format(sys.argv[0])
        sys.exit()
    else:
        account = sys.argv[1]
    if argc > 1:
        token = sys.argv[2]
        gh = pygithub3.Github(token=token)
    else:
        gh = pygithub3.Github()

    clone_urls = gather_clone_urls(account=account)
    for url in clone_urls:
        print urls