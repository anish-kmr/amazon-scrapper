import sys
from flask import Flask
from flask_restful import Api

from endpoints import SearchScrapperResource, ReviewScrapperResource, DetailProductScrapperResource
import logging


sys.path.append('.')
logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__)
api = Api(app)



api.add_resource(SearchScrapperResource, '/search')
api.add_resource(ReviewScrapperResource, '/reviews')
api.add_resource(DetailProductScrapperResource, '/detail')

if __name__ == '__main__':
    app.run(debug=True,port=5001)
    