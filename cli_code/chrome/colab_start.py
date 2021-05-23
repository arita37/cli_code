import pyautogui as k
import os
import time


url = "https://colab.research.google.com/drive/1x2D43aA7VWBSXfjBdwWrg-ZM1ItiuDaB"


os.system('start chrome')
time.sleep(1)
k.typewrite( url )
k.press('enter')
k.sleep(5)
k.keyDown('pagedown')
time.sleep(1)
k.keyUp('pagedown')
k.keyDown('ctrl')
k.press('f9')
#k.keyUp('ctrl')
time.sleep(5)

k.keyDown('ctrl') ; k.press('t')
k.typewrite( "https://dashboard.ngrok.com/endpoints/status" )


time.sleep(20)

"""
try_again =0
k.keyDown('ctrl')
k.press('enter')

k.keyDown('ctrl') ; k.press('T')
k.typewrite( "https://dashboard.ngrok.com/endpoints/status" )
"""



"""


Action  Shortcut
Open the Chrome menu    Alt + f or Alt + e
Show or hide the Bookmarks bar  Ctrl + Shift + b
Open the Bookmarks Manager  Ctrl + Shift + o
Open the History page in a new tab  Ctrl + h
Open the Downloads page in a new tab    Ctrl + j
Open the Chrome Task Manager    Shift + Esc
Set focus on the first item in the Chrome toolbar   Shift + Alt + t
Set focus on the rightmost item in the Chrome toolbar   F10 
Switch focus to unfocused dialog (if showing) and all toolbars  F6
Open the Find Bar to search the current page    Ctrl + f or F3
Jump to the next match to your Find Bar search  Ctrl + g
Jump to the previous match to your Find Bar search  Ctrl + Shift + g
Open Developer Tools    Ctrl + Shift + j or F12
Open the Clear Browsing Data options    Ctrl + Shift + Delete
Open the Chrome Help Center in a new tab    F1
Log in a different user or browse as a Guest    Ctrl + Shift + m
Open a feedback form    Alt + Shift + i
Turn on caret browsing  F7


"""




"""

download_path = r'C:/Users/Hp/Downloads'
mobX_path = 'C:/Users/Hp/PycharmProjects/MobaXterm_Portable_v20.2/MobaXterm.exe'
file_list=(os.listdir(download_path))
print(len(file_list))
for i in file_list:
    if 'ngrok_port' in str(i):
        print(i)
for i in file_list:
    if 'ngrok_port' in str(i):
        os.remove(os.path.join(download_path,i))
        print('Deleted old port file')




k.keyUp('ctrl')
b_while = True
while(b_while==True):
    file_list=(os.listdir(download_path))
    if 'ngrok_port.txt' in file_list:
        file= open(os.path.join(download_path,'ngrok_port.txt'),'r')
        port = file.read()
        print(port)
        b_while = False
    else:
        try_again=try_again+1
        if try_again<4:
            print("Trying Again")
            time.sleep(20)

os.system('start '+mobX_path)
time.sleep(7)
k.keyDown('ctrl')
k.keyDown('shift')
k.press('n')
k.keyUp('ctrl')
k.keyUp('shift')
time.sleep(3)
k.typewrite('0.tcp.ngrok.io')
time.sleep(1)
k.press('tab')
time.sleep(.5)
k.press('tab')
time.sleep(.5)
k.press('tab')
time.sleep(.5)
k.typewrite(port)
time.sleep(.5)
k.press('tab')
k.press('enter')
time.sleep(3)
k.typewrite('root')
time.sleep(2)
k.press('enter')
time.sleep(2)
k.typewrite('TestPassword')
k.press('enter')
time.sleep(1)
k.press('enter')
"""