from flask import request, jsonify
from flask_restful import Resource
from resources.scrapper import DetailProductScrapper

class DetailProductScrapperResource(Resource):
  def __init__(self):
    self.scrapper = DetailProductScrapper()
  
  def get(self):
    params = request.args
    detail_page_url = params.get('url')
    res = self.scrapper.scrap(detail_page_url)
    return res
