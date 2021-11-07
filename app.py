from flask import Flask
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix

from src import config
from src.imgurapi import ImgurAPI
from src.packerapi import PackerAPI

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='pyImgurloader',
          description='Creates a file from imgur link',
          )

config_namespace = api.namespace('config', description='Config settings')
imgur_namespace = api.namespace('imgur', description='Imgur API')
packer_cbz_namespace = api.namespace('packer_cbz', description='Packs images to cbz')
packer_pdf_namespace = api.namespace('packer_pdf', description='Packs images to pdf')
packer_zip_namespace = api.namespace('packer_zip', description='Packs images to zip')

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


@packer_cbz_namespace.route('/<string:album_hash>')
@imgur_namespace.param('album_hash', "Hash string of the album")
class Packer(Resource):

    def get(self, album_hash):
        packer_api = PackerAPI()
        packer_api.pack_cbz_or_zip(album_hash, False)
        return True


@packer_pdf_namespace.route('/<string:album_hash>')
@imgur_namespace.param('album_hash', "Hash string of the album")
class Packer(Resource):

    def get(self, album_hash):
        packer_api = PackerAPI()
        packer_api.pack_pdf(album_hash)
        return True


@packer_zip_namespace.route('/<string:album_hash>')
@imgur_namespace.param('album_hash', "Hash string of the album")
class Packer(Resource):

    def get(self, album_hash):
        packer_api = PackerAPI()
        packer_api.pack_cbz_or_zip(album_hash, True)
        return True


if __name__ == '__main__':
    app.run()
