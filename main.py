from pprint import pprint

import requests
import datetime
import json

from vk_user import VkUser
from ya_disk import YaUploader


def get_list_photos(token_vk):
    """
    Функция для получения списка фотографий с определенного аккаунат VK.
    В качестве фотографии, выбирается файл с максимальным разрешением.
    :return: Функция возвращает списко файлов фотографий
    """
    vk_client = VkUser(token_vk, '5.81')
    print(f'Получаем список фотографий в профиле VK \n ----')
    user_photos = vk_client.photos_get('profile', ext=1)
    out_data = []
    print(f'Анализируем полученные данные и формируем список фотографий \n ----')
    for photo in user_photos:
        date_photo = str(photo['date'])
        print(f'Дата фотографии: {date_photo}')
        count_likes = str(photo['likes']['count'])
        print(f'Количество лайков: {count_likes}')
        max_size_photo = str(photo['sizes'][-1]['type'])
        print(f'Выбираем фотографию наибольшего размера: {max_size_photo}')
        url_photo = photo['sizes'][-1]['url']
        print(f'URL этой фотографии: {url_photo}')
        if not any(item_photo.get('file_name', None) == (count_likes + ".jpg") for item_photo in out_data):
            file_name_photo = count_likes + ".jpg"
        else:
            file_name_photo = count_likes + "_" + date_photo + ".jpg"
        print(f'Добавляем в список фото с именем : {file_name_photo} \n ----')
        out_data.append(
            {"file_name": file_name_photo, "size": max_size_photo, "url_photo": url_photo}
        )
    return out_data


def upload_file_list(name_dir, file_list, count_photo=5):
    """
    Функция для загрузки файлов согалсно списка на Я.Диск
    :param name_dir: Имя папки, в которую помещаются файлы фотографий
    :param file_list: Список содержащий списко фотографий подлежащих загрузке на Я.Диск
    :param count_photo: Количество фотографий подлежащих загрузке на Я.Диск
    :return:
    """
    # # путь к файлу по URL
    # path_to_file = "https:\\"
    # # Путь к файлу на Яндекс.Диске
    # path_to_disk = "backup\\name_photo"
    i = 1
    for item_f in file_list:
        if i <= count_photo:
            uploader.upload_on_url(item_f['url_photo'], f"{name_dir}/{item_f['file_name']}")
            i += 1
            # print(item_f['file_name'])
    # uploader.upload_on_url(path_to_file, path_to_disk)


def mk_dir(name_dir):
    """
    Функция создает папку name_dir на Я.Диске
    :param name_dir: Имя папки
    :return:
    """
    creator.create_folder(name_dir)


if __name__ == '__main__':
    print(f'Запрашиваем ID пользователя VK\n ----')
    token_vk = input('Введите ID пользователя VK: ')
    print(f'Запрашиваем токен от пользователя\n ----')
    token_ya = input('Введите ТОКЕН для Я.Диск: ')
    list_photos = get_list_photos(token_vk)
    creator = YaUploader(token_ya)
    print(f'Генерируем имя папки для фотографий\n ----')
    cur_date = str(int(datetime.datetime.today().timestamp()))
    name_folder = 'backup_' + cur_date
    print(f'Создаем папку для фотографий\n ----')
    mk_dir(name_folder)
    uploader = YaUploader(token_ya)
    print(f'Записываем фотографии на Я.Диск\n ----')
    upload_file_list(name_folder, list_photos, 5)
    # Удаляем ключ 'url_photo'
    for item in list_photos:
        del item['url_photo']
    print('Выгружаем json в файл')
    with open('myfile.json', 'w') as f:
        json.dump(list_photos, f, sort_keys=True, indent=2)
