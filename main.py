from crawler import Crawler
from xlHandler import XlHandler



handler = XlHandler(".\\input\\MKM.xlsx")
buyList = handler.readBuyList()
sellList = handler.readSellList()

crawler = Crawler("https://www.cardmarket.com/en/Magic")
crawler.open()
crawler.iterateBuyList(buyList)
crawler.iterateSellList(sellList)
crawler.close()

handler.writeBuyList(buyList)
handler.writeSellList(sellList)
handler.saveChanges()
