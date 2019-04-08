from mitmproxy import ctx
import re
import requests
import json
import csv

from lxml import etree

def down_detil(url):
    headers = {
        # "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        # "Accept-Encoding":"gzip, deflate, br",
        # "Accept-Language":"zh-CN,zh;q=0.9",
        # "Cache-Control":"max-age=0",
        "Connection": "keep-alive",
        "cookie": "xhsTrackerId=8e993978-8150-4204-c245-f2417e4ce69b; xhsuid=jHNcslZpozk1QmD4; Hm_lvt_b344979f0455853bf22b3ef05fa7b4ac=1544432527; Hm_lvt_9df7d19786b04345ae62033bd17f6278=1544585706,1545118427; Hm_lvt_d0ae755ac51e3c5ff9b1596b0c09c826=1544429753,1544585706,1545118427; xhs_spses.5dde=*; extra_exp_ids=; ANTI=e77b3b070e|1545121441|e6cfaa768e; beaker.session.id=6c7fb8dbecd7a5bc5253c2206ae836d227b8e2cfgAJ9cQEoVQhfZXhwaXJlc3ECY2RhdGV0aW1lCmRhdGV0aW1lCnEDVQoH4gwTAygPA/NihVJxBFUDX2lkcQVVIDEzN2IwOGMxMzkzODRhZjdhYWExZTljN2UzMGE5YzE0cQZVDl9hY2Nlc3NlZF90aW1lcQdHQdcGKzf0gpBVDl9jcmVhdGlvbl90aW1lcQhHQdcEIHpNLXN1Lg==; Hm_lpvt_9df7d19786b04345ae62033bd17f6278=1545120995; Hm_lpvt_d0ae755ac51e3c5ff9b1596b0c09c826=1545120995; xhs_spid.5dde=6e70bc4555378797.1544585706.2.1545120998.1544586019.e6345f79-d932-408f-9c96-049f1195eb72",
        "Host": "www.xiaohongshu.com",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
    }
    html=requests.get(url=url,headers=headers).text
    # print(html)
    new_html=etree.HTML(html)
    star=new_html.xpath('//span[@class="star"]//text()')[0]
    comment=new_html.xpath('//span[@class="comment"]//text()')[0]
    return [star,comment]


contents_all=[]

try:
    # 所有的请求都会经过request
    def request(flow):

        # ctx.log.warn(str(flow.request.headers))
        #
        # info = ctx.log.info
        # info(flow.request.url)
        # info(str(flow.request.headers))
        # info(str(flow.request.cookies))
        # # info(flow.request.host)
        # info(flow.request.method)
        # # info(str(flow.request.port))
        # # info(flow.request.scheme)
        # print(flow.request.method,"\n",flow.request.url,"\n",flow.request.headers,"\n",flow.request.cookies)
        # print(type(str(flow.request.headers)))

        if 'https://www.xiaohongshu.com/sapi/wx_mp_api/sns/v1/search/notes' in flow.request.url:
            aaa=[]
            session_id=re.findall("session\.(\d+)",flow.request.url)[0]
            authorization=re.findall("authorization',.*?'(.*?)'\)",str(flow.request.headers))[0]
            auth=re.findall("auth',.*?'(.*?)'\)",str(flow.request.headers))[0]
            auth_sign=re.findall("auth-sign',.*?'(.*?)'\)",str(flow.request.headers))[0]
            aaa.append([session_id,auth,auth_sign])
            print(aaa)
            url=flow.request.url
            headers = {

                "charset": "utf-8",
                "Accept-Encoding": "gzip",
                "referer": "https://servicewechat.com/wxffc08ac7df482a27/147/page-frame.html",
                "authorization":authorization,
                "auth":auth,
                "content-type": "application/json",
                "auth-sign": auth_sign,
                "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; SM-G925F Build/LMY48Z) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Safari/537.36 MicroMessenger/6.6.7.1321(0x26060736) NetType/WIFI Language/zh_CN MicroMessenger/6.6.7.1321(0x26060736) NetType/WIFI Language/zh_CN",
                "Host": "www.xiaohongshu.com",
                "Connection": "Keep-Alive",}

            html = requests.get(url=url, headers=headers).text
            content = json.loads(html)
            for i in range(len(content["data"]["notes"])):
                id = content["data"]["notes"][i]["id"]
                title = content["data"]["notes"][i]["title"]
                note_url = "https://www.xiaohongshu.com/discovery/item/" + str(id)
                star1=down_detil(note_url)[0]
                comment1=down_detil(note_url)[1]
                img_url = content["data"]["notes"][i]["images_list"]
                like = content["data"]["notes"][i]["likes"]
                user = content["data"]["notes"][i]["user"]["nickname"]
                user_id = content["data"]["notes"][i]["user"]["userid"]
                user_url = "https://www.xiaohongshu.com/user/profile/" + str(user_id)

                ccc="标题：{}, 链接：{},喜欢：{},评论：{},加星：{},用户名：{},个人主页：{}".format(title,note_url,like,star1,comment1,user,user_url)+"\n"
                print(ccc)
                with open("xhsinfo5.txt", "a", encoding='utf-8') as f:
                    f.write(ccc)
                list=[title,note_url,like,star1,comment1,user,user_url]
                contents_all.append(list)

                with open("xhsinfo5.csv","a",encoding='utf-8',newline="") as f:


                    k = csv.writer(f, dialect="excel")
                    with open("xhsinfo5.csv", "r", encoding='utf-8', newline="") as f:
                        reader = csv.reader(f)
                        if not [row for row in reader]:
                            k.writerow(["标题", "链接", "喜欢", "评论", "加星","用户名", "个人主页"])
                            k.writerow(list)
                        else:
                            k.writerow(list)
except:
    with open("xhsinfo3.csv", "w", encoding='utf-8', newline="") as f:
        k = csv.writer(f, dialect="excel")
        k.writerow(["标题", "链接", "喜欢", "用户名", "个人主页"])
        for lis in contents_all:
            k.writerow(lis)
