from flask_restful import Resource, reqparse

# Internal packages:
from service.operators import run_build
from service.static import Request
from service import api

abst_request_parser = reqparse.RequestParser(bundle_errors=True)
abst_request_parser.add_argument('transactionId', type=str, required=True)
abst_request_parser.add_argument('boxId', type=str, required=True)


class SubmitBuild(Resource):
    def post(self):
        submit_parser = abst_request_parser.copy()
        submit_parser.add_argument('build_type', type=str, location='json', required=True)
        submit_parser.add_argument('git_url', type=str, location='json', required=True)
        submit_parser.add_argument('branch', type=str, location='json', required=True)
        submit_parser.add_argument('runScriptPath', type=str, location='json', required=True)
        args = submit_parser.parse_args()
        request = Request(input_json={
            "build_type": args.build_type,
            "git_url": args.git_url,
            "branch": args.branch,
            "transactionId": args.transactionId,
            "boxId": args.boxId,
            "run_script_path": args.runScriptPath
        }
        )
        run_build(request=request)

    def get(self):
        return {"message": "Helloooo ;)"}, 200


api.add_resource(SubmitBuild, "/build")
