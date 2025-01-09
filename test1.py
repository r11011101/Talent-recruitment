from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 啟動無頭模式
options = Options()
options.headless = True

# 使用 Firefox 瀏覽器
driver = webdriver.Firefox(options=options)

# 爬取 104 求職網頁面
url = 'https://www.104.com.tw/jobs/search/?jobcat=2007000000&isJobList=1&jobsource=joblist_search&searchJobs=1&indcat=1012001000&page=1'
driver.get(url)

time.sleep(5)


# 等待頁面上的某個職缺元素可見，最多等 10 秒
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CLASS_NAME, 'b-block--top-bord'))
)

# 模擬逐步滾動，每次滾動一定的距離
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # 滾動至頁面底部
    driver.execute_script("window.scrollBy(0, 500);")  # 每次滾動500像素
    time.sleep(2)  # 等待 2 秒讓內容加載

    # 計算滾動後的頁面高度
    new_height = driver.execute_script("return document.body.scrollHeight")
    
    # 如果滾動到底部沒有新內容加載，則停止滾動
    if new_height == last_height:
        break
    last_height = new_height

# 獲取滾動後的網頁 HTML 並使用 BeautifulSoup 解析
soup = BeautifulSoup(driver.page_source, 'lxml')

# 和之前一樣解析職缺資訊
jobs = soup.find_all('article', class_='flex-grow-1 h3 jb-link-blue--visited info-name pl-0')

# 確保爬取職缺資訊
if jobs:
    for job in jobs:
        job_link_element = job.find('a', class_='flex-grow-1 h3 jb-link-blue--visited info-name pl-0')
        if job_link_element:
            job_title = job_link_element.text
            job_link = job_link_element['href']
            # 確認連結是完整的 URL，否則補上 'https:' 前綴
            if not job_link.startswith('https'):
                job_link = 'https:' + job_link
            print(f'職位名稱: {job_title}')
            print(f'職位連結: {job_link}')
            print('-' * 20)
else:
    print('未找到任何職缺')

# 關閉瀏覽器
driver.quit()




