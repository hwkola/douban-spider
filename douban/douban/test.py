tags = [
    {
        "url": "https://www.douban.com/channel/27615252",
        "id": "27615252",
        "name": "科幻",
        "is_channel": True,
        "uri": "douban://douban.com/channel/27615252"
    },
    {
        "url": "https://www.douban.com/channel/30168840",
        "id": "30168840",
        "name": "喜剧片",
        "is_channel": True,
        "uri": "douban://douban.com/channel/30168840"
    },
    {
        "url": "https://www.douban.com/channel/30168839",
        "id": "30168839",
        "name": "爱情片",
        "is_channel": True,
        "uri": "douban://douban.com/channel/30168839"
    },
    {
        "url": "https://www.douban.com/channel/30168722",
        "id": "30168722",
        "name": "奇幻",
        "is_channel": True,
        "uri": "douban://douban.com/channel/30168722"
    },
    {
        "url": "https://www.douban.com/channel/30168823",
        "id": "30168823",
        "name": "香港电影",
        "is_channel": True,
        "uri": "douban://douban.com/channel/30168823"
    },
    {
        "url": "https://www.douban.com/channel/30169747",
        "id": "30169747",
        "name": "环保",
        "is_channel": True,
        "uri": "douban://douban.com/channel/30169747"
    },
    {
        "url": "https://www.douban.com/channel/30168833",
        "id": "30168833",
        "name": "搞笑片",
        "is_channel": True,
        "uri": "douban://douban.com/channel/30168833"
    },
    {
        "url": "https://www.douban.com/channel/30168718",
        "id": "30168718",
        "name": "童话",
        "is_channel": True,
        "uri": "douban://douban.com/channel/30168718"
    }
]

res = [i['name'] for i in tags]

print(res)