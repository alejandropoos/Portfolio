import pyautogui
import webbrowser
from time import sleep

webbrowser.open("https://web.whatsapp.com/send?phone=+54xxxxxxxxx")
sleep(10)
pyautogui.typewrite("Hola! esto es un mensaje automatico!\n")
pyautogui.press("enter")