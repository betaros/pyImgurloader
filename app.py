from flask import Flask
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix

from src import config
from src.imgurapi import ImgurAPI
from src.packer import Packer

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='pyImgurloader',
          description='Creates a file from imgur link',
          )

config_namespace = api.namespace('config', description='Config settings')
imgur_namespace = api.namespace('imgur', description='Imgur API')
packer_namespace = api.namespace('packer', description='Packs images')

config_model = api.model('Config_model', {
    'client_id': fields.String(required=True, description='Client id'),
    'client_secret': fields.String(required=True, description='Client secret')
})


@config_namespace.route('/')
class Configuration(Resource):

    @config_namespace.doc('Get current config')
    def get(self):
        return config.get_config()

    @config_namespace.doc('Set current config')
    @config_namespace.expect(config_model)
    @config_namespace.marshal_with(config_model)
    def put(self):
        conf = config.set_config(api.payload)

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


@packer_namespace.route('/<string:album_hash>')
@imgur_namespace.param('album_hash', "Hash string of the album")
class Packer(Resource):

    def get(self):

        return None


if __name__ == '__main__':
    app.run()
