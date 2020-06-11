# GitHub-Monitor
根据关键词监控github上的更新信息，并通过[Server酱](http://sc.ftqq.com/3.version)推送到微信上。

# 使用
1.`git clone https://github.com/gtfly/GitHub-Monitor`

2.修改`monitor.py`75~80行，将自己想要监听的关键字添加到`key_words`中，设置更新的时间间隔`intval`(建议改大点，否则请求频率过大会被拒绝连接)，并修改`SCKEY`为自己的Server酱的KEY：

``` python
# set your config
    config = {
        "key_words": ['cve', 'password'],
        "intval": 200,  # 发送间隔, 单位为s;
        "SCKEY": '12345678',  # Server酱 KEY
    }
```

3.运行：

    python3 monitor.py
    # 后台运行
    nohup python3 monitor.py > log.log &

# 效果
![截图1](http://www.gtfly.top:81/202006110510.png)

![截图2](http://www.gtfly.top:81/202006110511.jpg)

![截图3](http://www.gtfly.top:81/202006110512.jpg)
