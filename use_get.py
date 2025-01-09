import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

def get_job_data(keyword):
    url = f'https://www.104.com.tw/jobs/search/?jobsource=index_s&keyword={keyword}&mode=s&page=1'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    page = 1

    job_list = []

    while soup.find_all('article', class_="b-block--top-bord job-list-item b-clearfix js-job-item"):
        for job in soup.find_all('article', class_="b-block--top-bord job-list-item b-clearfix js-job-item"):
            job_data = {}
            job_data["職缺名稱"] = job['data-job-name']  # 職缺名稱
            job_data["職缺連結"] = 'https:' + job.a['href']  # 職缺連結
            job_data["公司名稱"] = job['data-cust-name']  # 公司名稱
            job_data["工作地區"] = job.select('ul.b-list-inline.b-clearfix.job-list-intro.b-content li')[0].text  # 工作地區
            
            salary_info = job.find('div', class_="job-list-tag b-content")

            # 處理薪資資訊
            if salary_info.select('span') and salary_info.span.text == "待遇面議":
                e = salary_info.span.text
            else:
                e = salary_info.a.text
            
            job_data["薪資待遇"] = e
            job_data["計薪方式"] = e[:2]  # 計薪方式
            salary = ''
            for char in e:
                if char.isdigit() or char == '~':
                    salary += char
            
            if '~' in salary:
                low_salary = salary[:salary.find('~')]
                high_salary = salary[salary.find('~') + 1:]
            else:
                low_salary = salary
                high_salary = ''  # 沒有`~`符號時，給high_salary一個預設空值
            
            job_data["薪資下限"] = int(low_salary) if low_salary.isdigit() else 40000
            job_data["薪資上限"] = int(high_salary) if high_salary.isdigit() else 40000

            job_list.append(job_data)
        
        page += 1
        res = requests.get(f'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword={keyword}&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=14&asc=0&page={page}&mode=s&jobsource=index_s&langFlag=0&langStatus=0&recommendJob=1&hotJob=1')
        soup = BeautifulSoup(res.text, "html.parser")

    return job_list

def analyze_job_data(job_list):
    df = pd.DataFrame(job_list)
    total_jobs = len(df)
    max_salary = df["薪資上限"].max()
    min_salary = df["薪資下限"].min()
    avg_salary = df[["薪資下限", "薪資上限"]].mean().mean()

    return total_jobs, max_salary, min_salary, avg_salary

def save_to_excel(df, filename):
    if not os.path.exists(filename):
        wb = Workbook()
        ws = wb.active
        ws.title = "104職缺資料"
        for r in dataframe_to_rows(df, index=False, header=True):
            ws.append(r)
        wb.save(filename)
    else:
        with pd.ExcelWriter(filename, mode='a', if_sheet_exists='new') as writer:
            df.to_excel(writer, sheet_name='104職缺資料', index=False)

if __name__ == "__main__":
    keyword = input("請輸入要搜尋的職缺關鍵字: ")
    job_list = get_job_data(keyword)
    total_jobs, max_salary, min_salary, avg_salary = analyze_job_data(job_list)
    
    # 通知資料爬取完成
    print("資料爬取完成")

    # 使用者輸入選項
    user_input = input("請輸入選項 (1: 印出資料, 2: 存入Excel): ")

    current_date = datetime.now().strftime("%Y-%m-%d")

    if user_input == '1':
        print(f"執行日期: {current_date}")
        print(f"職缺數量: {total_jobs}")
        print(f"職缺最高薪: {max_salary}")
        print(f"職缺最低薪: {min_salary}")
        print(f"職缺平均薪資: {avg_salary:.2f}")
    elif user_input == '2':
        df = pd.DataFrame(job_list)
        filename = f"{current_date}_104職缺資料.xlsx"
        save_to_excel(df, filename)
        print(f"資料已存入 {filename}")
    else:
        print("無效的選項")