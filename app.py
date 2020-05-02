from flask import Flask, request
from flask_restful import Resource, Api
import json
import lambda_function

app = Flask(__name__)
api = Api(app)


class SendEmail(Resource):
    def post(self):
        data = request.get_json()
        print(lambda_function.sendEmail(data))
        return json.dumps({"status": 200})


api.add_resource(SendEmail, '/sendemail')

if __name__ == "__main__":
    app.run(debug=True)
