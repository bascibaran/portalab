from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal
from .model import Dataset
from app import db

dataset_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'type': fields.String
}

dataset_list_fields = {
    'count': fields.Integer,
    'datasets': fields.List(fields.Nested(dataset_fields)),
}

dataset_post_parser = reqparse.RequestParser()
dataset_post_parser.add_argument('name', type=str, required=True, location=['json'],
                              help='name parameter is required')
dataset_post_parser.add_argument('type', type=str, required=True, location=['json'],
                              help='type parameter is required')


class DatasetsResource(Resource):
    def get(self, dataset_id=None):
        if dataset_id:
            dataset = Dataset.query.filter_by(id=dataset_id).first()
            return marshal(dataset, dataset_fields)
        else:
            args = request.args.to_dict()
            limit = args.get('limit', 0)
            offset = args.get('offset', 0)

            args.pop('limit', None)
            args.pop('offset', None)

            dataset = Dataset.query.filter_by(**args).order_by(Dataset.id)
            if limit:
                dataset = dataset.limit(limit)

            if offset:
                dataset = dataset.offset(offset)

            dataset = dataset.all()

            return marshal({
                'count': len(dataset),
                'datasets': [marshal(u, dataset_fields) for u in dataset]
            }, dataset_list_fields)

    @marshal_with(dataset_fields)
    def post(self):
        args = dataset_post_parser.parse_args()

        dataset = Dataset(**args)
        db.session.add(dataset)
        db.session.commit()

        return dataset

    @marshal_with(dataset_fields)
    def put(self, dataset_id=None):
        dataset = Dataset.query.get(dataset_id)

        if 'name' in request.json:
            dataset.name = request.json['name']

        db.session.commit()
        return dataset

    @marshal_with(dataset_fields)
    def delete(self, dataset_id=None):
        dataset = Dataset.query.get(dataset_id)

        db.session.delete(dataset)
        db.session.commit()

        return dataset