import pyautogui
import webbrowser
from time import sleep

webbrowser.open("https://web.whatsapp.com/send?phone=+543435199006")
sleep(10)
pyautogui.typewrite("Hola estoy es un mensaje automatico?\n")
pyautogui.press("enter")
