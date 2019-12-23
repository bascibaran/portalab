from flask import Flask, jsonify
from flask_restful import Api
from flask_pymongo import PyMongo
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import default_exceptions
import settings
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code

for ex in default_exceptions:
    app.register_error_handler(ex, handle_error)


app.config['MONGO_URI'] = settings.MONGO_URI
#app.config['BUNDLE_ERRORS'] = settings.BUNDLE_ERRORS

mongo = PyMongo(app)
api = Api(app)
api.prefix = '/api'

# from endpoints.datasets.resource import DatasetsResource
# #from endpoints.connectors.resource import ConnectorsResource

# api.add_resource(DatasetsResource, '/datasets', '/users/<int:user_id>')
# #api.add_resource(ConnectorsResource, '/connectors', '/todos/<int:todo_id>')
@app.route('/dataset', methods=['GET'])
def get_all_datasets():
  dataset = mongo.db.datasets
  output = []
  for s in dataset.find():
    output.append({'name' : s['name'], 'ds_type' : s['ds_type']})
  return jsonify({'result' : output})

@app.route('/dataset/', methods=['GET'])
def get_one_dataset(name):
  dataset = mongo.db.datasets
  s = dataset.find_one({'name' : name})
  if s:
    output = {'name' : s['name'], 'ds_type' : s['ds_type']}
  else:
    output = "No such name"
  return jsonify({'result' : output})

@app.route('/dataset', methods=['POST'])
def add_dataset():
  dataset = mongo.db.datasets
  name = request.json['name']
  ds_type = request.json['ds_type']
  dataset_id = dataset.insert({'name': name, 'ds_type': ds_type})
  new_dataset = dataset.find_one({'_id': dataset_id })
  output = {'name' : new_dataset['name'], 'ds_type' : new_dataset['ds_type']}
  return jsonify({'result' : output})

if __name__ == '__main__':
    app.run()