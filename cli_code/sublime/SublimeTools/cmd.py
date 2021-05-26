
import os
import webbrowser
import sublime
import sublime_plugin
import sys
from SublimeTools.gitutil import GitUtil, main

if sys.version_info < (3, 0):
    from urllib import quote as quote_param
else:
    from urllib.parse import quote_plus as quote_param


def search(q, url=''):
    settings = sublime.load_settings("google_search.sublime-settings")
    # Attach the suffix and the prefix
    q = settings.get('prefix', '') + quote_param(q) + \
        settings.get('suffix', '')
    if url == '':
        fullUrl = settings.get(
            'domain', 'https://www.google.com') + "/search?q=%s" % q
    else:
        fullUrl = url + '/search?q=%s' % q
    browser = settings.get('default_browser', '')

    if browser:
        try:
            webbrowser.get(browser).open(fullUrl)
        except:
            webbrowser.open(fullUrl)
    else:
        webbrowser.open(fullUrl)


def git_command(path, command_string):
    g = GitUtil(path)
    # g.test()
    print("adding files")
    files = g.add()  # change the number to filter files on size , size in bytes
    print('committing files')
    g.commit(files)
    print('done')


class TestCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        project_path = self.view.window().project_file_name()
        if project_path == None:
            project_path = self.view.window().folders()[0]
        file_name = self.view.file_name()  # return file path
        for region in self.view.sel():
            if region.empty():
                return
            else:
                if not region.empty():
                    selected_text = self.view.substr(region)
            # return selected text
            

        query_list = selected_text.split('::')
        if len(query_list) != 2:
            print('query string is invalid')
            return
        for region in self.view.sel():
            self.view.erase(edit, r=region)
        command = query_list[0].lower()
        command_string = query_list[1].lower()
        if command == 'git':
            git_command(project_path, command_string)
        elif command == 'stack':
            search(command_string, 'https://stackoverflow.com')
