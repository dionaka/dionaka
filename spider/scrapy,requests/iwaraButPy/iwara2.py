import requests
#from lxml import etree
#import pprint
#requests库只负责发送HTTP请求和接收响应，它不会解析HTML或xml内容，所以如果想用xpath来解析HTML或xml，需要用到lxml或beautifulsoup这样的库
page=0
while True:
    page+=1
    print('===正在爬取第{}页数据==='.format(page))
    url="https://api.iwara.tv/search?type=video&page={}&query=%E5%8E%9F%E7%A5%9E".format(page)
    headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
    response1=requests.get(url=url,headers=headers)
    json_data=response1.json()
    video_data=json_data['results']
    #pprint.pprint(video_data)
    #列表里包含字典，每个字典都是不同视频
    #https://www.iwara.tv/video/%s/hmv
    for one_data in video_data:
        try:
            data1=one_data['title']+'.mp4'#标题
            #data2="https://www.iwara.tv/video/%s/hmv"%one_data['id']#每个视频对应网页：不是视频地址，通过数据库search?type...找到对应网址(即url)
            data2 ="https://api.iwara.tv/video/%s"%one_data['id']  #每个视频对应url动态生成,通过视频所在网址数据库oze...中找到
            #data3视频url就在HTML中,而data3是动态加载的,在json中,data3采用xpath提取
            #这里也和先前一样，动态网址，无法用xpath获取到视频url地址并且观察到视频url地址不断变化，etree方法返回源代码不全等
            #response2=requests.get(url=data2,headers=headers)
            #tree=etree.HTML(response2.text)
            #data3=tree.xpath("//div[@id='vjs_video_3']/video/@src")#以上代码只针对静态网页HTML提取，动态网站应找json

            #现在从json格式的url2中提取视频地址
            response2=requests.get(url=data2,headers=headers)
            json_data2=response2.json()
            if 'fileUrl' in json_data2:
                data3=json_data2['fileUrl']
                if data3 is None:
                    #字符串'null'解析结果是None而不是null字符本身
                    #print('null')
                    continue
                else:
                    response3=requests.get(url=data3,headers=headers)
                    json_data3=response3.json()
                    if json_data3=='None':
                        #print("NO files in 'fileUrl'")
                        continue
                    else:
                        dict=json_data3[0]
                        data4=dict['src']['view']
                        #print(data4)
                        #continue
            else:
                #print("NO FOUND 'fileUrl'")
                continue
        except:
            break

        if data4:
            response4=requests.get(url='https:'+data4,headers=headers).content#视频数据:.content:取出二进制数据
            #保存数据
            #非法字符:'/','\\',':','*','?','"','|','<','>'
            safedata=data1.replace('|','_')
            safedata=safedata.replace('\\', '_')
            safedata=safedata.replace('/', '_')
            safedata=safedata.replace(':', '_')
            safedata=safedata.replace('?', '_')
            safedata=safedata.replace('*', '_')
            safedata=safedata.replace(':', '_')
            with open('videos2\\'+safedata,mode='wb') as f:
                print('正在保存:',data1)
                f.write(response4)
        else:
            print("NO VIDEO SOURCE FOUND")
    else:
        continue
    break        
