import requests
import pprint
from lxml import etree
url="http://diona.sdos.top"
headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
response=requests.get(url=url,headers=headers)
response.encoding='utf-8'
tree=etree.HTML(response.text)
data=tree.xpath('//div[@id="border2"]//a/@href')
data2=tree.xpath('//div[@id="border2"]//a//text()')
print(data2)
i=0
for i in range(min(len(data2),len(data))):
    print(data[i]+'\t'+data2[i])

