import pandas as pd
import requests
import logging
 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76'}
def getAir(city_en,city_zh):
    for page in range(1, 13): 
        url = f'http://www.tianqihoubao.com/aqi/{city_en}-2019{page:02d}.html'
        response=requests.get(url,headers=headers)
        df = pd.read_html(response.content,encoding='gbk')[0]
        if page < 10:
            if page == 1:
                df.to_csv(f'2019年{city_zh}空气质量数据.csv', mode='a+', index=False, header=False)
            else:
                df.iloc[1:,::].to_csv(f'2019年{city_zh}空气质量数据.csv', mode='a+', index=False, header=False)
        else:
            df.iloc[1:,::].to_csv(f'2019年{city_zh}空气质量数据.csv', mode='a+', index=False, header=False)
        logging.info(f'{page}月空气质量数据下载完成！')
getAir("guangzhou","广州")
getAir("shanghai","上海")
