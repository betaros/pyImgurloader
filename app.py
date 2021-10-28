from flask import Flask
from flask_restx import Api, Resource
from werkzeug.middleware.proxy_fix import ProxyFix

from src import config
from src.imgurapi import ImgurAPI

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='pyImgurloader',
          description='Creates a file from imgur link',
          )

config_namespace = api.namespace('config', description='Config settings')
imgur_namespace = api.namespace('imgur', description='Imgur API')
packer_namespace = api.namespace('packer', description='Packs images')


@config_namespace.route('/')
class Configuration(Resource):

    @config_namespace.doc('Get current config')
    def get(self):
        return config.get_config()

    @config_namespace.doc('Set current config')
    def put(self, client_id, client_secret):
        conf = config.set_config(client_id, client_secret)

        return conf


@imgur_namespace.route('/<string:album_hash>')
@imgur_namespace.param('album_hash', 'Hash string of the album')
class Imgur(Resource):

    @imgur_namespace.doc('Get album infos')
    def get(self, album_hash):
        imgur_api = ImgurAPI()
        return imgur_api.get_infos(album_hash)

    @imgur_namespace.doc('Download images')
    def post(self, album_hash):
        imgur_api = ImgurAPI()
        return imgur_api.get_images(album_hash)


@packer_namespace.route('/')
class Packer(Resource):

    def get(self):
        return None


if __name__ == '__main__':
    app.run()
