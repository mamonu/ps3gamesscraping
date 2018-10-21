from lxml import html
import requests
from pprint import pprint
import unicodecsv as csv
from traceback import format_exc


brand="PS3"

def parse():
	for i in range(2): # try twice
		try:
			url='http://www.ebay.co.uk/b/Sony-PS3-Video-Games/139973/bn_446843?rt=nc&_udhi=5&LH_Auction=1'
			headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
			print ("Retrieving %s"%(url))
			response = requests.get(url, headers=headers, verify=False)
			print ("Parsing page")
			parser = html.fromstring(response.text)
			product_listings = parser.xpath('//li[contains(@class,"lvresult")]')
			raw_result_count = parser.xpath("//span[@class='rcnt']//text()")
			result_count = ''.join(raw_result_count).strip()
			print ("Found {0} results for {1}".format(result_count,brand))
			scraped_products = []

			for product in product_listings:
				raw_url = product.xpath('.//a[@class="vip"]/@href')
				raw_title = product.xpath('.//a[@class="vip"]/text()')
				raw_price = product.xpath(".//li[contains(@class,'lvprice')]//span[@class='bold']//text()")
				price  = ' '.join(' '.join(raw_price).split())
				title = ' '.join(' '.join(raw_title).split())
				data = {
							'url':raw_url[0],
							'title':title,
							'price':price
				}
				scraped_products.append(data)
			return scraped_products
		except Exception as e:
			print (format_exc(e))



scraped_data =  parse()
print ("Writing scraped data to %s-ebay-scraped-data.csv"%(brand))
	
with open('%s-ebay-scraped-data.csv'%(brand),'wb') as csvfile:
	fieldnames = ["title","price","url"]
	writer = csv.DictWriter(csvfile,fieldnames = fieldnames,quoting=csv.QUOTE_ALL)
	writer.writeheader()
	for data in scraped_data:
            writer.writerow(data)

	
import sys
import pandas as pd
import re
import numpy as np


game = pd.read_csv('EDGE9s10s.csv', encoding = 'latin1',usecols = ['Title','Format','Publisher','Issue','Score'])

def formatToArray (text):
    newText = filternonascii(text)
    newArr = newText.split()
    cleanArr = []
    
    for elem in newArr:
        output1 = ''.join([s for s in elem if ord(s) != 44])
        cleanArr.append(output1)
    return pd.Series(dict(output=cleanArr))


def filternonascii(text):
    output = ''.join([s for s in text if ord(s) < 127])
    return (output)

def isPS3(array):
    isThere = 0
    for elem in array:
        if elem == 'PS3':
            isThere +=1 
            break
    return pd.Series(dict(output=int(isThere)))

def onlyPS3(df):
    game = pd
    game['clean_format']=game['Format'].apply(filternonascii)
    game['arr_format']=game['clean_format'].apply(formatToArray)
    game['bool_PS3']=game['arr_format'].apply(isPS3)
