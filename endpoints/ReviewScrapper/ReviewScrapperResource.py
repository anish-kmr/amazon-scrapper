from flask import request, jsonify
from flask_restful import Resource
from resources.scrapper import ReviewScrapper

class ReviewScrapperResource(Resource):
  def __init__(self):
    self.scrapper = ReviewScrapper()
  
  def get(self):
    params = request.args
    review_page_url = params.get('url')
    res = self.scrapper.scrap(review_page_url)
    return res
