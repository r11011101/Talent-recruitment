import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

# 啟動無頭模式
options = Options()
options.headless = True

# 使用 Firefox 瀏覽器
driver = webdriver.Firefox(options=options)

# 爬取 104 求職網頁面
url = 'https://www.104.com.tw/jobs/search/?jobcat=2007000000&isJobList=1&jobsource=joblist_search&searchJobs=1&indcat=1012001000&page=1'
driver.get(url)

# 等待頁面加載
time.sleep(5)

# 模擬滾動以加載更多職位資訊
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # 滾動到頁面底部
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # 等待內容加載

    # 獲取網頁 HTML 並使用 BeautifulSoup 解析
    soup = BeautifulSoup(driver.page_source, 'lxml')

    # 獲取包含職業資訊的 <script> 標籤
    script_tag = soup.find('script', type='application/ld+json')

    # 解析 JSON 數據
    if script_tag:
        data = json.loads(script_tag.string)
        # 進行數據處理
        # ...

    # 計算新的頁面高度
    new_height = driver.execute_script("return document.body.scrollHeight")

    # 如果新高度與最後一個高度相同，則停止滾動
    if new_height == last_height:
        break

    last_height = new_height


# 獲取網頁 HTML 並使用 BeautifulSoup 解析
soup = BeautifulSoup(driver.page_source, 'lxml')

# 獲取包含職業資訊的 <script> 標籤
script_tag = soup.find('script', type='application/ld+json')

print('script_tag',script_tag)
# 解析 JSON 數據
if script_tag:
    data = json.loads(script_tag.string)

    # 根據 data 的實際結構來提取職業資訊
    if isinstance(data, list):
        for item in data:
            if 'mainEntity' in item:
                job_list = item['mainEntity'][0]['itemListElement']
                for job in job_list:
                    job_name = job['item']['name']
                    job_url = job['item']['url']
                    job_description = job['item']['description']  # 獲取職位描述

                    print(f'職位名稱: {job_name}')
                    print(f'職位連結: {job_url}')
                    print(f'職位描述: {job_description}')  # 打印職位描述
                    print('-' * 20)
else:
    print('未找到職業資訊')

# 關閉瀏覽器
driver.quit()
