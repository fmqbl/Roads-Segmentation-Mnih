import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import logging
import traceback
import os
import pdb
import time

#Static path from my machine, you can adjust as per your machine
download_folder = "D:\\MasterDataScience\\Deep Learning\\Project\\dataset\\Testing\\testingOutput"

profile = {"plugins.plugins_list": [{"enabled": False,
                                         "name": "Chrome PDF Viewer"}],
               "download.default_directory": download_folder,
               "download.extensions_to_open": ""}

class downloader:
    
    def __init__(self):
        #logging information setup
        self.logger = logging.getLogger('MNihDataset Download LOG')
        self.logger.setLevel(logging.DEBUG)
        
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        
        self.logger.addHandler(ch)
        self.logger.propagate = False
        
        # application setting
        
        self.url = "https://www.cs.toronto.edu/~vmnih/data/mass_roads/test/map/index.html"
        
    def setupChrome(self):

        # Contains all chrome settings
        self.logger.info("Setting-up Chrome")
        self.settings = webdriver.ChromeOptions()
        #self.settings.add_argument("--incognito")
        self.settings.add_argument('--ignore-ssl-errors')
        self.settings.add_argument('--ignore-certificate-errors')
        self.settings.add_argument('–-disable-web-security')
        self.settings.add_argument('–-allow-running-insecure-content')
        self.settings.add_argument('--browser.download.folderList=2')
        self.settings.add_argument('--browser.helperApps.neverAsk.saveToDisk=text/csv')
        self.settings.add_experimental_option("prefs",profile)
        #Preferences to be set before.
        
    def loadBrowser(self):
        
        #pdb.set_trace()
        self.setupChrome()

        try:
            #self.browser = webdriver.Chrome("D:\\DataScrapping\\ProjectBigSchedules\\chromedriver.exe")
            #Chrome driver should be downloaded as per the chrome version you are using from https://chromedriver.chromium.org/downloads
            self.browser = webdriver.Chrome(chrome_options=self.settings, executable_path=r"D:\chromedriver.exe")
            self.browser.maximize_window()

        except Exception as e:
            self.logger.critical("Unable to load chrome driver. " + str(e))
        
        #Entering the URLc

        
        self.browser.get(self.url)
        
        self.downloadImages()

    def downloadImages(self):
        #Goes to path, downloaded each images iteratively
        elems = self.browser.find_elements_by_xpath("//a[@href]")
        counter = 1
        for elem in elems:
            self.logger.info("Downloading images number = " + str(counter) + " and the name is "+elem.text)

            if not os.path.exists(os.path.join(download_folder,elem.text)):
                elem.click()
                time.sleep(1)
            counter = counter +1
        print(counter)

if __name__ == '__main__':
    obj = downloader()
    obj.setupChrome()
    obj.loadBrowser()
