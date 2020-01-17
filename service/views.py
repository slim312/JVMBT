from flask_restful import Resource, reqparse
from flask_api import status
import logging

# Internal packages:
from service.operators import run_build
from service.static import Request
from service import api, app


logger = logging.getLogger(__name__)
abst_request_parser = reqparse.RequestParser(bundle_errors=True)
abst_request_parser.add_argument('transactionId', type=str, required=True)
abst_request_parser.add_argument('boxId', type=str, required=True)


class SubmitBuild(Resource):
    def post(self):
        submit_parser = abst_request_parser.copy()
        submit_parser.add_argument('build_type', type=str, location='json', required=True)
        submit_parser.add_argument('git_url', type=str, location='json', required=True)
        submit_parser.add_argument('branch', type=str, location='json', required=True)
        submit_parser.add_argument('run_script_path', type=str, location='json', required=True)
        args = submit_parser.parse_args()
        try:
            logger.debug(f"Arguments parsed: {args}")
            request = Request(input_json={
                "build_type": args.build_type,
                "git_url": args.git_url,
                "branch": args.branch,
                "transactionId": args.transactionId,
                "boxId": args.boxId,
                "run_script_path": args.run_script_path
            }
            )
            logger.debug(f"Request built! Running build (transaction: {args.transactionId})...")
            app.logger.info(f"POST request received! Arguments: {args}")
            run_build(request=request)
        except Exception as e:
            return {"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR

    def get(self):
        return {"message": "Helloooo ;)"}, status.HTTP_200_OK


api.add_resource(SubmitBuild, "/build")
