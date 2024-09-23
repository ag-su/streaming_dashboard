from flask import Flask
from flask_restx import Resource, Api
from dashboard.apis.artist import artist_ns
from dashboard.apis.song import song_ns
from dashboard.apis.record import record_ns
from dashboard.apis.prediction import prediction_ns


def create_app(): 
    # flask 애플리케이션 인스턴스 생성 
    app = Flask(__name__)

    # ========== api ==========
    api = Api(app)
    api.add_namespace(artist_ns, '/artists')
    api.add_namespace(song_ns, '/songs')
    api.add_namespace(record_ns, '/records')
    api.add_namespace(prediction_ns, '/predictions')

    return app

