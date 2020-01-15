from flask_restful import Resource, reqparse
from flask import Request

# Internal packages:
from service.operators import build
from service import api

abst_request_parser = reqparse.RequestParser()
abst_request_parser.add_argument('transactionId', type=str, required=True)
abst_request_parser.add_argument('boxId', type=str, required=True)


class SubmitBuild(Resource):
    def post(self):
        submit_parser = abst_request_parser.copy()
        submit_parser.add_argument('build_type', type=str, location='json', required=True)
        submit_parser.add_argument('git_url', type=str, location='json', required=True)
        submit_parser.add_argument('branch', type=str, location='json', required=True)
        builder


api.add_resource(SubmitBuild, "/build")
