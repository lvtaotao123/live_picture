import requests
import json
import multiprocessing 
import os
def par_huya(html):
    html = json.loads(html)
    datas = html['data']['datas']
    z = len(datas)
    if z > 0:
        for data in datas:
            url_img = data['screenshot']
            name = data['nick']
            yield url_img,name,z


def par_douyu(html):
    html = json.loads(html)
    datas = html['data']['r1']
    z = len(datas)
    if z > 0:
        for data in datas:
            url_img = data['rs1']
            name = data['nn']
            yield url_img,name,z
            
def down_img(url,name):
    img = requests.get(url).content

    fh = open('./img/'+name + '.jpg','wb')
    fh.write(img)
    fh.close()


def req(url,n,k):
    html = requests.get(url).text

    l = 0
    j = 0
    if n == 0:
        for i,name,z in par_huya(html):
            down_img(i, name)
            l += 1
            print('\r------当前虎牙第%d页---进度：%d/%d'%(k,l,z))
    
    if n == 1:
        for i,name,z in par_douyu(html):
            down_img(i, name)

            j += 1
            print('\r-----当前斗鱼第%d页---进度：%d/%d'%(k,j,z))

if  __name__ == '__main__':
    
    try:
        os.mkdir('img')
    except:
        pass
    urls = [
            'https://www.douyu.com/gapi/rknc/directory/yzRec/',
            'https://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&gameId=1663&tagAll=0&page='
            ]
    p = multiprocessing.Pool(3)
    for i in range(1,13):
        url = urls[0] + str(i)
        p.apply_async(req,args=(url,1,i,))
    for j in range(1,18):
        url = urls[1] + str(j)
        p.apply_async(req,args=(url,0,j,))
    p.close()
    p.join()
