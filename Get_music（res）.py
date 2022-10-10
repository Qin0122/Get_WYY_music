import requests
import time
import re
import json
from jsonpath import jsonpath
import os


class Get_music(object):
    def __init__(self):
        with open('./歌手信息库/网易歌手信息库2.json', 'r', encoding='utf-8') as f:
            # 获取信息库中的json数据，并转换为python字符串
            data = json.load(f)
            # 获取信息库中的歌手名字
            self.names = jsonpath(data, '$..name')
            # 获取歌手对应的链接
            self.hrefs = jsonpath(data, '$..href')

    # 获取音乐
    def get_music(self): # 接收（歌手，href）
        singer = input('请输入歌手名：')
        if singer not in self.names:
            print('抱歉，没有此歌手。')
            return

        print('请等待下载……')

        # 遍历数据，并获取对应的歌手名和href传给下载音乐的函数
        for info in list(zip(self.names, self.hrefs)):
            if info[0] == singer:
                if not os.path.exists(f'{info[0]}'):
                    os.makedirs(f'{info[0]}')

                #构建请求头
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
                }

                res = requests.get(info[1], headers)

                # 获取歌曲名字
                name = re.findall('<a href="/song\?id=\d*">(.*?)</a>', res.text)
                # 获取歌曲的id
                id = re.findall('<a href="/song\?id=(\d*)">', res.text)

                #保存音乐
                for k in range(len(id)):
                    # 发送请求，获取响应
                    url = f'http://music.163.com/song/media/outer/url?id={id[k]}'
                    res = requests.get(url, headers = headers)
                    #保存入文件中
                    with open(f'./{info[0]}/{name[k]}.mp3', 'wb') as f:
                        f.write(res.content)
                    print(f'{name[k]} - 下载成功')
                return

    # 获取单首歌曲
    def download_one(self):
        song = input('请输入歌名：')
        singer = input('请输入歌手名：')

        if singer not in self.names:
            print('抱歉，没有此歌手。')
            return

        print('请等待下载……')
        # 遍历数据，并获取对应的歌手名和href传给下载音乐的函数
        for info in list(zip(self.names, self.hrefs)):
            if info[0] == singer:
                if not os.path.exists(f'{info[0]}'):
                    os.makedirs(f'{info[0]}')

                #构建请求头
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
                }

                res = requests.get(info[1], headers)

                # 获取歌曲名字
                name = re.findall('<a href="/song\?id=\d*">(.*?)</a>', res.text)
                # 获取歌曲的id
                id = re.findall('<a href="/song\?id=(\d*)">', res.text)

                #保存音乐
                for k in range(len(id)):
                    if song not in name:
                        print('抱歉，没有查到此歌曲。')
                        return

                    elif song == name[k]:
                        # 发送请求，获取响应
                        url = f'http://music.163.com/song/media/outer/url?id={id[k]}'
                        res = requests.get(url, headers = headers)
                        #保存入文件中
                        with open(f'./{info[0]}/{name[k]}.mp3', 'wb') as f:
                            f.write(res.content)
                        print(f'{name[k]} - 下载成功')
                        return

    def run(self):
        while True:
            print('~'*10 + '功能界面' + '~'*9)
            print('1、根据歌手名下载歌曲（下载多首）')
            print('2、根据歌曲名和歌手名下载歌曲（下载单首）')
            print('3、退出功能')
            print('~'*25)
            func = input('请选择功能：')
            if func == '1':
                self.get_music()
            elif func == '2':
                self.download_one()
            elif func == '3':
                break
        print('欢迎下次使用！ ≧◠◡◠≦')
        time.sleep(2)


if __name__ == '__main__':
    get_music = Get_music()
    get_music.run()






