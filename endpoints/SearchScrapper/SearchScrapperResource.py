from flask import request, jsonify
from flask_restful import Resource
from resources.scrapper import SearchScrapper

class SearchScrapperResource(Resource):
  def __init__(self):
    self.scrapper = SearchScrapper()
  
  def get(self):
    params = request.args
    searchString = params.get('s')
    res = self.scrapper.scrap(searchString)
    return res
