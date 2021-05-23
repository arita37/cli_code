import pyautogui as k
import os
import time


download_path = r'C:\Users\Hp\Downloads'
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
os.system('start chrome')
time.sleep(5)
k.typewrite('https://colab.research.google.com/drive/1qj39LJEs-YH9KDYArVP1hUz8Gter47eg#scrollTo=_p3B61DaYVAd')
k.press('enter')
k.sleep(10)
k.keyDown('pagedown')
time.sleep(1)
k.keyUp('pagedown')
k.keyDown('ctrl')
k.press('f9')
k.keyUp('ctrl')
time.sleep(180)
try_again =0
k.keyDown('ctrl')
k.press('enter')

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
