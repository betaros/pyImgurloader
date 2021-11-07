from pathlib import Path

from PIL import Image
from zipfile import ZipFile

from src.utils import get_project_root


class PackerAPI:

    def __init__(self):
        self.root = get_project_root()

    def pack_cbz_or_zip(self, album_hash, zip_archive):
        if zip_archive:
            file_path = Path(self.root, 'temp', album_hash, f'{album_hash}.zip')
        else:
            file_path = Path(self.root, 'temp', album_hash, f'{album_hash}.cbz')

        folder_path = Path(self.root, 'temp', album_hash).glob('*.jpg')

        if not file_path.is_file():
            with ZipFile(file_path, 'w') as cbzObj:
                for element in folder_path:
                    cbzObj.write(str(element.name))

    def pack_pdf(self, album_hash):
        file_path = Path(self.root, 'temp', album_hash, f'{album_hash}.pdf')
        folder_path = Path(self.root, 'temp', album_hash).glob('*.jpg')

        if not file_path.is_file():
            with ZipFile(file_path, 'w') as pdfObj:
                image_list = []

                for element in folder_path:
                    image = Image.open(str(element))
                    im = image.convert('RGB')
                    image_list.append(im)

                image_list[0].save(file_path, save_all=True, append_images=image_list[1:])
