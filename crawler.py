from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

class Crawler:
    def __init__(self, page):
        self.options= Options()
        self.options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = self.options)
        self.page = page

    def open(self):
        self.driver.get(self.page)

    def close(self):
        self.driver.close()

    def iterateBuyList(self, buyList):
        for element in buyList:
            self.__search(element["cardName"])
            self.__selectSet(element["set"], element["cardName"])
            element["trend"] = self.__getPriceTrend()
            if float(element["trend"]) <= float(element["target"]):
                element["OK"] = True
        time.sleep(8)

    def iterateSellList(self, sellList):
        for element in sellList:
            self.__search(element["cardName"])
            self.__selectSet(element["set"], element["cardName"])
            element["trend"] = self.__getPriceTrend()
            if float(element["trend"]) >= float(element["target"]):
                element["OK"] = True


    def __search(self, cardName):
        searchBar = self.driver.find_elements("xpath", "//input[@id='ProductSearchInput']")[0]
        searchBar.click()
        searchBar.send_keys(cardName)
        searchButton = self.driver.find_elements("xpath", "//button[@id='search-btn']")[0]
        searchButton.click()

    def __selectSet(self, setName, cardName):
        results = self.driver.find_elements("xpath", "//div[@class='row g-0']")
        for result in results:
            if setName in result.get_attribute("innerHTML"):
                links = self.driver.find_elements("xpath", "//div[@id='"+result.get_attribute("id")+"']//a")
                for link in links:
                    if cardName in link.get_attribute("innerHTML"):
                        link.click()
                        break
                break

    def __getPriceTrend(self):
        dd = self.driver.find_elements("xpath", "//dl//dd")[6]
        trend = dd.get_attribute("innerHTML")
        trend = trend.replace("<span>", "")
        trend = trend.replace(" €</span>", "")
        trend = trend.replace(",",".")
        return trend
