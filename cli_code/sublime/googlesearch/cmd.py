
import os, sys, webbrowser, sublime, sublime_plugin
from .gitutil import GitUtil, main

if sys.version_info < (3, 0):
    from urllib import quote as quote_param
else:
    from urllib.parse import quote_plus as quote_param



#####################################################################################
class TestCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        project_path = self.view.window().project_file_name()
        if project_path == None:
            project_path = self.view.window().folders()[0]


        file_name = self.view.file_name()  # return file path
        for region in self.view.sel():
            if region.empty():
                #### Select Full 
                selected_text = self.view.substr( self.view.line( self.view.sel()[0]))   
            else:
                if not region.empty():
                    selected_text = self.view.substr(region)
            # return selected text
            
        query_list = selected_text.split(':')
        if len(query_list) != 2:
            query_list = ['gg' , query_list[0] ]
            #print('query string is invalid')
            #return


        #### Delete ##############################################
        region = self.view.line(self.view.sel()[0])
        self.view.erase(edit, r=region)

        for region in self.view.sel():
            self.view.erase(edit, r=region)


        ##########################################################
        cmd        = query_list[0].lower().strip()
        cmd_string = query_list[1].lower().strip()
        print(cmd)

        if   cmd == 'git'    : do_git_command(cmd, project_path, cmd_string)

        elif cmd == 'stack'  : do_search('google', cmd_string, 'stackoverflow.com')

        elif cmd == 'github' : do_search('github', cmd_string, '')

        elif cmd == 'go'     : do_gowebsite('go', cmd_string, '')
            
        else :                 do_search('google', cmd_string, '')    ### Default Google



###############################################################################
###### List of Actions  #######################################################
def do_search(cmd='', q='', url=''):
    settings = sublime.load_settings("google_search.sublime-settings")
    # Attach the suffix and the prefix
    q = settings.get('prefix', '') + quote_param(q) + settings.get('suffix', '')


    if cmd == 'google':
        if  url != '' : 
            fullUrl = settings.get('domain', 'https://www.google.com') +  "/search?q={q}+sites%3A{url}".format(q=q, url=url)
        else :
            fullUrl = settings.get('domain', 'https://www.google.com') + "/search?q={q}".format(q=q)



    else:
        fullUrl = url + '/search?q=%s' % q


    browser_open(fullUrl, settings)    

  


def do_git_command(path, command_string):
    g = GitUtil(path)
    # g.test()
    print("adding files")
    files = g.add()  # change the number to filter files on size , size in bytes
    print('committing files')
    g.commit(files)
    print('done')



def do_gowebsite(cmd='', q='', url=''):
    settings = sublime.load_settings("google_search.sublime-settings")
    # Attach the suffix and the prefix
    # q = settings.get('prefix', '') + quote_param(q) + settings.get('suffix', '')
    print(q)

    if    'utilmy'   in q : fullUrl = 'https://github.com/arita37/myutil/tree/main/utilmy'
    elif  'cli_code' in q : fullUrl = 'https://github.com/arita37/cli_code/tree/dev/cli_code/sublime/googlesearch'



    else:
        fullUrl = url + '/search?q=%s' % q


    browser_open(fullUrl, settings)




def browser_open(fullUrl, settings):
    ### Open 
    browser = settings.get('default_browser', '')
    if browser:
        try:
            webbrowser.get(browser).open(fullUrl)
        except:
            webbrowser.open(fullUrl)
    else:
        webbrowser.open(fullUrl)
  

