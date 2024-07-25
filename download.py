from concurrent.futures import ThreadPoolExecutor
import requests
import bs4
import os
import hashlib
from PIL import Image


def creat_folder(path):

    if not os.path.exists('image'):
        os.mkdir('image')


def img_search(album_url, web_url, user_agent):

    chapter_lists = []
    resp = requests.get(url=album_url,
                        headers={'User-Agent': user_agent},
                        stream=True
                        )
    soup = bs4.BeautifulSoup(resp.text, 'html.parser')
    angles = soup.select('div.episode>ul a')
    for angle in angles:
        incomplete_url = angle.get('href')
        complete_url = web_url + incomplete_url
        chapter_lists.append(complete_url)
    return chapter_lists


def img_write(img_name, resp):

    with open(img_name, 'wb') as file:
        file.write(resp.content)


def get_num(chapter_id,photo_num):

    if (chapter_id <= '220971'):
        return 0
    num = 10
    arr = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    if (chapter_id >= '220972' and chapter_id <= '268849'):
        return num
    key = chapter_id + photo_num
    key = ord(hashlib.md5(key.encode(encoding='utf_8')).hexdigest()[-1])
    if (chapter_id >= '268850' and chapter_id <= '421925'):
        key %= 10
        return arr[key]
    if (chapter_id >= '421926'):
        key %= 8
        return arr[key]


def fix_img(img_name, chapter_id, photo_num):

    num = get_num(chapter_id,photo_num)
    with Image.open(img_name) as original_img:
        size = original_img.size
        img_weight = size[0]
        img_height = size[1]
        cut_height = int(img_height/num)
        scrap_height = img_height % num
        new_img = Image.new(mode='RGB', size=(img_weight,img_height), color='white')
        for i in range(num):
            if i == num - 1:
                box = (0, cut_height * i, img_weight, cut_height * (i + 1) + scrap_height)
                piece = original_img.crop(box)
                fix_box = (0, img_height - cut_height * (i + 1) - scrap_height, img_weight, img_height - cut_height * i)
                new_img.paste(piece, fix_box)
            else:
                box = (0, cut_height*i, img_weight, cut_height*(i+1))
                piece = original_img.crop(box)
                fix_box = (0, img_height - cut_height*(i+1), img_weight, img_height - cut_height*i)
                new_img.paste(piece, fix_box)
        new_img.save(f'{img_name}.jpg')


def img_download(chapter_url, chapter_id, user_agent):

        resp = requests.get(url=chapter_url,
                            headers={'User-Agent': user_agent},
                            stream=True
                            )
        soup = bs4.BeautifulSoup(resp.text, 'html.parser')
        anchors = soup.select('div.container img.img-responsive-mw')
        for anchor in anchors:
            img = anchor.get('data-original')
            resp = requests.get(img,
                                headers={'User-Agent': user_agent},
                                stream=True
                                )
            pass_name = img[img.rfind('/', 0, img.rfind('/')) + 1:]
            if not pass_name.endswith('p'):
                pass_name = img[img.rfind('/', 0, img.rfind('/')) + 1:img.rfind('?')]
            photo_num = pass_name[pass_name.rfind('/') + 1:pass_name.rfind('.')]
            name = pass_name.replace('/', '')
            img_name = f'image/{name}'
            img_write(img_name, resp)
            fix_img(img_name, chapter_id, photo_num)


user_agent = input('请输入User-Agent：')
web_url = input('网站网址（不要加最后的斜杠）：')
album_url = input('漫画网址：')
path = os.getcwd()
creat_folder(path)
chapter_lists = img_search(album_url, web_url, user_agent)
with ThreadPoolExecutor(max_workers=64) as pool:
    for chapter_url in chapter_lists:
        chapter_id = chapter_url[chapter_url.rfind('/') + 1:]
        pool.submit(img_download, chapter_url, chapter_id, user_agent)




