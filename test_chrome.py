from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json

# 初始化 webdriver
driver = webdriver.Chrome()
driver.get("https://www.104.com.tw/jobs/search/?jobcat=2007000000&isJobList=1&jobsource=joblist_search")

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # 滾動到頁面底部
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # 等待內容加載

    # 獲取網頁 HTML 並使用 BeautifulSoup 解析
    soup = BeautifulSoup(driver.page_source, 'lxml')

    # 獲取所有 <script> 標籤
    script_tags = soup.find_all('script')

    for script_tag in script_tags:
        if script_tag.get('type') == 'application/ld+json':
            data = json.loads(script_tag.string)
            for job in data[1]["mainEntity"][0]["itemListElement"]:
                job_details = job["item"]
                print(f"職位名稱: {job_details['name']}")
                print(f"職位連結: {job_details['url']}")
                print(f"職位描述: {job_details['description']}")
                print("--------------------")

    # 計算新的頁面高度
    new_height = driver.execute_script("return document.body.scrollHeight")

    # 如果新高度與最後一個高度相同，則停止滾動
    if new_height == last_height:
        break

    last_height = new_height

driver.quit()
