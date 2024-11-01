import pandas as pd
import logging
 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
 
for page in range(1, 13):   # 12个月
    if page < 10:
        url = f'http://www.tianqihoubao.com/aqi/guangzhou-20190{page}.html'
        df = pd.read_html(url, encoding='gbk')[0]
        if page == 1:
            df.to_csv('2019年广州空气质量数据.csv', mode='a+', index=False, header=False)
        else:
            df.iloc[1:,::].to_csv('2019年广州空气质量数据.csv', mode='a+', index=False, header=False)
    else:
        url = f'http://www.tianqihoubao.com/aqi/guangzhou-2019{page}.html'
        df = pd.read_html(url, encoding='gbk')[0]
        df.iloc[1:,::].to_csv('2019年广州空气质量数据.csv', mode='a+', index=False, header=False)
    logging.info(f'{page}月空气质量数据下载完成！')