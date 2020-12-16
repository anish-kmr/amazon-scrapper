from flask import request, jsonify
from flask_restful import Resource
from resources.scrapper import ReviewScrapper

class ReviewScrapperResource(Resource):
  def __init__(self):
    self.scrapper = ReviewScrapper()
  
  def get(self):
    params = request.args
    review_page_url = params.get('url')
    num_reviews = params.get('n')
    if num_reviews:
      num_pages = int(int(num_reviews)/10)
    else:
      num_pages=10
    res = self.scrapper.scrap(review_page_url,num_pages)
    return res
