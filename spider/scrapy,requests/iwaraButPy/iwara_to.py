import requests
headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
data ="https://himeko.iwara.tv/view?filename=69e210a8-2322-496d-aabf-bfa8555ead57_540.mp4&path=2024%2F07%2F05&expires=1720553105&hash=9a672d081fc47486a9dbe7dc359263882d4aba1d057d7e1858488bc9bbb237ac"#可改
response=requests.get(url=data,headers=headers).content
name="太卜大人，你也不想自慰的视频被发到网上吧？"
with open('videos_to\\'+name+'.mp4',mode='wb') as f:
    print('正在保存')
    f.write(response)