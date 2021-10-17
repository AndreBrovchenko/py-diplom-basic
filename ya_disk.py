from pprint import pprint

import requests
import datetime


class YaUploader:
    """
    Класс для работы с Яндекс.Диск
    """
    def __init__(self, token_ya: str):
        """
        :param token_ya: значение ТОКЕНА для доступа к Яндекс.Диск-у
        """
        self.token = token_ya

    def get_headers(self):
        """
        Метод для формирования атрибута "headers" запроса
        :return:
        """
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def get_files_list(self):
        """
        Метод для получения списка файлов
        :return:
        """
        url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
        headers = self.get_headers()
        response = requests.get(url=url, headers=headers)
        return response.json()

    def _get_upload_link(self, disk_file_path):
        """
        Метод для получения ссылки для загрузки файла на Яндекс.Диск
        :param disk_file_path: Путь к файлу на Яндекс.Диске
        :return:
        """
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload(self, file_path: str, file_to_disk):
        """
        Метод загружает файл на Яндекс.Диск c локального диска
        :param file_path: Путь к файлу на локальном диcке для загрузки на Яндекс.Диск
        :param file_to_disk:  Путь к файлу на Яндекс.Диске
        :return:
        """
        response = self._get_upload_link(file_to_disk)
        download_link = response.get('href', '')
        response = requests.put(url=download_link, data=open(file_path, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print("Success")

    def upload_on_url(self, file_url: str, file_to_disk):
        """
        Метод загружает файл на Яндекс.Диск по URL
        :param file_url: URL файла для загрузки на Яндекс.Диск
        :param file_to_disk:  Путь к файлу на Яндекс.Диске
        :return:
        """
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {
            'url': file_url,
            'path': file_to_disk
        }
        response = requests.post(url=upload_url, headers=headers, params=params)
        response.raise_for_status()
        if response.status_code == 202:
            print(f"Файл {file_to_disk} записан на Я.Диск")

    def create_folder(self, name_forder):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = {'path': name_forder}
        response = requests.put(url=url, headers=headers, params=params)
        response.raise_for_status()
        if response.status_code == 201:
            print(f"Папка {name_forder} создана на Я.Диске")
