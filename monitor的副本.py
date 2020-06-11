#_*_ coding: utf-8 _*_
# @Author: gtfly
# @Date: 2020-06-11 15:06

import requests
import json
import time


def Request(api, key):
    return requests.get(api.format(key)).text


def getTotal(api, key):
    content = json.loads(Request(api, key))
    return int(content["total_count"])


def getInfo(api, key, index, send_count):
    content = json.loads(Request(api, key))
    for i in range(send_count):
        info_list[index][str(i)] = {
            "name": content["items"][i]["name"],
            "description": content["items"][i]["description"],
            "url": content["items"][i]["html_url"]
        }


# 初始化，获取初始count
def Init(api, key_words):
    for index in range(len(key_words)):
        time.sleep(60)
        key = key_words[index]
        info_list[index]["key word"] = key
        info_list[index]["flag_total"] = getTotal(api, key)


# 判断count后将信息存到列表中
def Update(api, key_words):
    for index in range(len(key_words)):
        time.sleep(60)
        key = key_words[index]
        total = getTotal(api, key)
        if info_list[index]["flag_total"] < total:
            send_count = total - info_list[index]["flag_total"]
            info_list[index]["flag_total"] = total # update
            getInfo(api, key, index, send_count)


# 发送到Server酱
def Send(info_list, key):
    url = 'https://sc.ftqq.com/{}.send'.format(key)
    for i in range(len(info_list)):
        title = "Github监控更新提醒：{}".format(info_list[i]["key word"])
        desp = ""
        if "name" in str(info_list[i]):
            count = len(info_list[i]) - 2
            for k in range(count):
                desp += "名称：{}\n\n简介：{}\n\n地址：{}\n\n".format(info_list[i][str(k)]["name"], info_list[i][str(k)]["description"], info_list[i][str(k)]["url"])
                del(info_list[i][str(k)])

            data = {
                "text": title,
                "desp": desp
            }
            res = requests.post(url, data=data)



if __name__ == '__main__':
    print("initial...                " + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))

    api = 'https://api.github.com/search/repositories?q={}&sort=updated'

    # set your config
    config = {
        "key_words": ['cve', 'password'],
        "intval": 200,  # 发送间隔, 单位为s;
        "SCKEY": '12345678',  # Server酱 KEY
    }

    info_list = []
    for i in range(len(config["key_words"])):   
        info_list.append({})

    Init(api, config["key_words"])
    
    while 1:
        print("waiting to update...      " + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        time.sleep(config["intval"])
        Update(api, config["key_words"])
        print(info_list) # 控制台打印信息
        Send(info_list, config["SCKEY"]) # 推送信息到微信