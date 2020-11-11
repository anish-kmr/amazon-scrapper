from abc import ABC, abstractmethod, abstractproperty
from selectorlib import Extractor
import requests 
import json
import os
import logging as log


log.basicConfig(level=log.DEBUG)
PATH = os.path.abspath(os.getcwd())

class Scrapper(ABC):
  @abstractmethod
  def __init__(self):
    self.headers = headers = {
      'authority': 'www.amazon.com',
      'pragma': 'no-cache',
      'cache-control': 'no-cache',
      'dnt': '1',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'sec-fetch-site': 'none',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-dest': 'document',
      'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    self.base_url = 'https://www.amazon.in'
    self.selectors_path = PATH + '/resources/selectors/'

  @abstractmethod
  def scrap(self):
    pass
    
class SearchScrapper(Scrapper):
  def __init__(self):
    super().__init__()
    self.search_selector_path = self.selectors_path+'search_result_selector.yaml'
    self.extractor = Extractor.from_yaml_file(self.search_selector_path)

  
  def scrap(self,searchString,num_pages=1):
    searchString = '+'.join(searchString.split(' '))
    log.debug(f"Scrapping  : {self.base_url}/s?k={searchString}")
    scrap_url = self.base_url+'/s?k='+searchString
    result={'products':[]}
    i=0
    while(i<num_pages):
      log.debug(f"Scrapping {scrap_url} Page Number {i+1}")
      res = requests.get(scrap_url, headers=self.headers)
      if res.status_code > 500:
          log.debug("Error : Status code 500 returned from request")
          continue
      scrapped_res = self.extractor.extract(res.text)
      # print(json.dumps(scrapped_res,indent=2))
      if(scrapped_res['products']):
        result['products'].extend(scrapped_res['products'])
        log.debug(f"scrapped {len(scrapped_res['products'])} result in page {i+1}")
      else:
        continue
      if(scrapped_res['next_page']):
        scrap_url = self.base_url+scrapped_res['next_page']
      else:
        break
      i+=1

    return result
  
    
class DetailProductScrapper(Scrapper):
  def __init__(self):
    super().__init__()
    self.search_selector_path = self.selectors_path+'detail_product_selector.yaml'
    self.extractor = Extractor.from_yaml_file(self.search_selector_path)

  
  def scrap(self,detail_page_url):
    log.debug(f"Scrapping  : {self.base_url}/{detail_page_url}")
    scrap_url = self.base_url+detail_page_url
    result={'review_page_url':''}
    res = requests.get(scrap_url, headers=self.headers)
    if res.status_code > 500:
      log.debug("Error : Status code 500 returned from request")
    scrapped_res = self.extractor.extract(res.text)
    # print(json.dumps(scrapped_res,indent=2))
    if(scrapped_res['review_page_url']):
      result['review_page_url']= scrapped_res['review_page_url']

    return result
  
    
class ReviewScrapper(Scrapper):
  def __init__(self):
    super().__init__()
    self.search_selector_path = self.selectors_path+'reviews_selector.yaml'
    self.extractor = Extractor.from_yaml_file(self.search_selector_path)

  
  def scrap(self,review_page_url,num_pages=10):
    log.debug(f"Scrapping  : {self.base_url}/{review_page_url}")
    scrap_url = self.base_url+review_page_url
    result={'reviews':[]}
    i=0
    while(i<num_pages):
      log.debug(f"Scrapping {scrap_url} Page Number {i+1}")
      res = requests.get(scrap_url, headers=self.headers)
      if res.status_code > 500:
        log.debug("Error : Status code 500 returned from request")
        continue
      scrapped_res = self.extractor.extract(res.text)
      # print(json.dumps(scrapped_res,indent=2))
      if(scrapped_res['reviews']):
        result['reviews'].extend(scrapped_res['reviews'])
        log.debug(f"scrapped {len(scrapped_res['reviews'])} result in page {i+1}")
      else:
        continue
      if(scrapped_res['next_page']):
        scrap_url = self.base_url+scrapped_res['next_page']
      else:
        break
      i+=1

    return result
  



# s=DetailProductScrapper()
# r = s.scrap('/Redmi-Note-Pro-Interstellar-Snapdragon/dp/B077PWBC78/ref=sr_1_1?dchild=1&keywords=redmi+note+9+pro&qid=1604995381&sr=8-1')
# r = json.dumps(r,indent=4)
# print(r)