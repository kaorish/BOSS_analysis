import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
from urllib.parse import urljoin
import random
import time
import os

url = f"https://www.zhipin.com/web/geek/job?query=python&city=101110100&page=1"

# 创建浏览器实例
driver = webdriver.Chrome()
# 打开浏览器
driver.get(url)
input('请在网页中完成登录，登录完成输入回车结束')
# 记录程序开始时间
start_time = time.time()
# 输入关键词
key_words = ['Python']
# 输入不同的城市代码

city_list = [101010100, 101020100, 101280100, 101210100, 101030100]
# 设置循环的页数
max_page = 10
for city in city_list:
    for key_word in key_words:
        for page in range(1, max_page + 1):
            # 创建url
            url = f"https://www.zhipin.com/web/geek/job?query={key_word}&city={city}&page={page}"
            # 打开浏览器
            driver.get(url)
            driver.execute_script("window.scrollBy(0, 1000);") 
            time.sleep(random.uniform(1, 3))
            driver.execute_script("window.scrollBy(0, -1000);")  
            try:
                wait = WebDriverWait(driver, 30)
                wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="job-name"]')))
            except:
                print('主页面未加载')
                print('请打开浏览器通过验证，输入回车结束')
                input()
            
            page_source = driver.page_source
            tree = etree.HTML(page_source)
            url_list = tree.xpath('//ul[@class="job-list-box"]/li/div/a/@href')
            for job_detail_url in url_list:
                full_url = urljoin(url, job_detail_url)
                driver.get(full_url)         
                driver.execute_script("window.scrollBy(0, 1000);")
                time.sleep(random.uniform(2, 3))
                driver.execute_script("window.scrollBy(0, -1000);")  
                try:
                    wait = WebDriverWait(driver, 30)
                    wait.until(EC.presence_of_element_located((By.XPATH, '//h1[@title]')))
                except:
                    print('详情页面未加载')
                    print('请打开浏览器通过验证，输入回车结束')
                    input()
                time.sleep(random.uniform(2, 3))
                page_source = driver.page_source
                tree = etree.HTML(page_source)
                try:
                    job_title = tree.xpath('//h1[@title]/text()')[0].strip()
                except:
                    job_title = 'None'
                try:
                    salary = tree.xpath('//span[@class="salary"]/text()')[0].strip()
                except:
                    salary = 'None'
                try:
                    job_location = tree.xpath('//a[@class="text-desc text-city"]/text()')[0].strip()
                except:
                    job_location = 'None'
                try:
                    experience = tree.xpath('//span[@class="text-desc text-experiece"]/text()')[0].strip()
                except:
                    experience = None
                try:
                    education = tree.xpath('//span[@class="text-desc text-degree"]/text()')[0].strip()
                except:
                    experience = None
                try:
                    company_name = tree.xpath('//li[@class="company-name"]/text()')[0].strip()
                except:
                    try:
                        company_name = tree.xpath('//div[@class="company-info"]/a[2]/text()')[0].strip()
                    except:
                        company_name = None
                try:
                    job_description = "".join(tree.xpath('//div[@class="job-sec-text"]/text()'))
                except:
                    job_description = None
                try:
                    skills = ",".join(tree.xpath('//ul[@class="job-keyword-list"]/li/text()'))
                except:
                    skills = None
                print(skills)
                print('当前的主页位于', url)
                file_exists = os.path.isfile(f'job_data_{key_word}.csv')
                with open(f'job_data_{key_word}.csv', mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    if not file_exists:
                        writer.writerow(
                            ['Job Title', 'Salary', 'Location', 'Experience', 'Education', 'Company Name',
                             'Job Description',
                             'Skills', 'URL'])
                    writer.writerow(
                        [job_title, salary, job_location, experience, education, company_name, job_description, skills,
                         full_url])
end_time = time.time()

print("程序工耗时间", end_time - start_time)
driver.close()
