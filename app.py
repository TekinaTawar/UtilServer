from flask import Flask, request
from flask_restful import Resource, Api

import lambda_function
import survey_con

app = Flask(__name__)
api = Api(app)

@app.route('/')
def main():
    return '<h1>This is the email sender api </h1>'

class SendEmail(Resource):
    def post(self):
        data = request.get_json()
        print(lambda_function.sendEmail(data))
        survey_con.convert_it()
        return {"status": 200}


api.add_resource(SendEmail, '/sendemail')

if __name__ == "__main__":
    app.run(debug=True)
