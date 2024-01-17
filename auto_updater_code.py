import requests
import PySimpleGUI as sg
from bs4 import BeautifulSoup
from datetime import datetime
import os.path

def main():

def save_to(dir,myStr):
    f = open(dir, "w")
    f.write(myStr)
    f.close()

def get_i_from_cat(cat):
    if cat == "Generic":
        return 0
    elif cat == "Computer sciences":
        return 1
    elif cat == "Mathematics":
        return 2
    elif cat == "Computer utils":
        return 3
    else:
        return 0

if __name__ == "__main__":
    main()