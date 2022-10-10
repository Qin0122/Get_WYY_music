''' 注意：cookie需要是登录后的cookie'''

import requests
from lxml import etree
import json

class Singer(object):
    def __init__(self):

        # url = 'https://music.163.com/discover/artist/cat?id=1001&initial=-1'
        self.url = 'https://music.163.com/discover/artist/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
            'Cookie': '_ntes_nnid=45c1ede7b130f1b0bcc0a5ef1daddbb7,1647700789813; _ntes_nuid=45c1ede7b130f1b0bcc0a5ef1daddbb7; NMTID=00O93Gi3TTMra2iIkMctyXoJt-F2_4AAAF_op7CVA; WEVNSM=1.0.0; WNMCID=ysuzwh.1647700789957.01.0; WM_TID=GXMBggILFQhEBVBVVBNu%2F5wMxr2lMCWX; UM_distinctid=1801c4ff195bf6-052a23fc9f7fc1-9771539-144000-1801c4ff196aca; WM_NI=Fvf7X2YUuwH2vcFGKxsfdFC4HLzEpPl51kbsr9gmsMmfKOCx1BIK0wQx8t97liHVNM7jk6REqgiHqMltKOefHGjs%2BHKKCQFhrsPDjr%2FW3LTdY%2F0FJhi1KHIbqG%2BuF%2B%2FuNzQ%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eed2d833b78ebbb1ed619bbc8eb6d84a879a8ab0c84bb1b683d8c45a8fb89787f62af0fea7c3b92a86aaaad8db3a9b8bbb98cb3ab6bd8aa8ca74b1baaca7c2408c94b6a6f35cb0ebff8ce179b2e7a98ef247afba85b0c274f39e87acb37d93a8f895bc3db0b788b7cd47f5b6a5d7d14fb3b9a7a9f447b0ac85b0e86e8c99a694aa4489958db2c564b2ada0a5e97aed89fdadd7709bf100a7c964abef85a9cc6ab399e596c521edab829bd437e2a3; MUSIC_U=efaf0ef05dea529f21b1f3c6e1e915700c471eeb544c2ddf23b25180db6ffcd7993166e004087dd3adb1172ff4e28d91a3399127f50a3052762393ede8173b140e6f8ec5accfc554d4dbf082a8813684; __remember_me=true; __csrf=4bc09cd9a0f41db2da3ab1faf6da353e; ntes_kaola_ad=1; _iuqxldmzr_=32; JSESSIONID-WYYY=qb8BlD6%5Csb3WnPJ49kMo8AT62DgEwNwPmy4VMtIsxKK8U27CQTqHKFfzd8F%2B56KVf5u3MOp%5CN%5C0Uy2dtD3E3b7Bt6e555VPa45dtttxWwN5EY1NM8ngUheZWYOhhUaxnN6nRbnpIi8NPNT0thmfwVaGMsAi8g0NYfTpTSOjGn%2BpbPkt4%3A1656467924147',
            'Referer': 'https://music.163.com/'
        }


    # 获取各类歌手的id信息
    def get_info1(self):
        res = requests.get(self.url, headers=self.headers)
        html = etree.HTML(res.text)
        # 获取各类歌手的id信息
        self.ids_1 = html.xpath('//ul[@class="nav f-cb"]/li/a/@data-cat')
        del self.ids_1[0]

    # 根据各类歌手的id信息获取对应歌手的姓名和链接
    def get_info2(self):
        li = [-1, 0] + list(range(65,90))
        self.names = [] # 存储名字
        self.hrefs = [] # 存储链接
        for i in range(len(self.ids_1)):
            for j in li:
                url1 = f'https://music.163.com/discover/artist/cat?id={self.ids_1[i]}&initial={j}'
                res = requests.get(url1, headers=self.headers)
                html = etree.HTML(res.text)
                # 获取歌手的名字
                self.names += html.xpath('//ul[@id="m-artist-box"]/li/p/a[1]/text()')
                # 获取歌手的href
                self.hrefs += ['https://music.163.com'+ k.strip() for k in html.xpath('//ul[@id="m-artist-box"]/li/p/a[1]/@href')]

    def savefile(self):
        with open('网易歌手信息库2.json', 'a', newline="", encoding='utf-8') as f:
            # 将获取的名字和链接存入字典中
            for k in range(len(self.names)):
                data = {'name': self.names[k], 'href': self.hrefs[k]}
                # 将字典转换成json数据
                data_str = json.dumps(data, ensure_ascii=False)
                f.write(data_str + ',' + '\n')

    def run(self):
        self.get_info1()
        self.get_info2()
        self.savefile()

singer = Singer()
singer.run()
