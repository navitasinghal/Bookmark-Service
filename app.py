from flask import Flask, jsonify
from flask_restplus import Resource, Api
import chrome_bookmarks
import json
from flask_cors import CORS
# from db import db

app = Flask(__name__)
CORS(app)
api = Api(app)


@api.route('/health')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

@api.route('/bookmark/folder' , endpoint='bookmark')
class Bookmark(Resource):
    def get(self):
        array=[]
        i=0
        for folder in chrome_bookmarks.folders:
            array.append({"folderName" : folder.name, "urls":[] })
            for url in folder.urls:
                array[i]["urls"].append(url)
            i+=1
        data=(json.dumps({"data":array}))
        return array, 201

@api.route('/bookmark/urls')
class Url(Resource):
    def get(self):
        x=[]
        for url in chrome_bookmarks.urls:
            print(url)
            x.append(url)
        return (x) , 201


if __name__ == "__main__":
    # db.init_app(app)
    app.run(port=5000, debug=True)

