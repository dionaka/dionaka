import requests
url1="https://www.pixiv.net/ajax/user/3439325/profile/all?lang=zh&version=b84cb537b2ba819525e66eed415d9f17a2db86e5"
headers={'user-angent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
response1=requests.get(url=url1,headers=headers)
data1=response1.json()
data2=data1['body']
#插图
data3=data2['illusts']
#漫画//figure//a/img/@src
data4=data2['manga']
for x in data3:
    url2="https://www.pixiv.net/artworks/%s"%x
    response2=requests.get(url=url2,headers=headers)


