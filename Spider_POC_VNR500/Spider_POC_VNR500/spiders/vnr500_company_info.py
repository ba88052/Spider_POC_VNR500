import scrapy
from bs4 import BeautifulSoup
import json
from Spider_POC_VNR500.items import SpiderPocVnr500Item
from datetime import datetime

today = datetime.today()
this_year = today.year
today = today.strftime('%-m/%-d')


class VnrCompanyInfoSpider(scrapy.Spider):
    name = 'vnr500_company_info'
    BQ_TABLE_ID = f'company_info_{this_year}_{today}'
    
    
    #---------------設定爬取的網站，可調整year的年份，可從2008-2022----------------#
    def start_requests(self):
        for chart_id in [1, 2]:
            url = f'https://vnr500.com.vn/Charts/Index?chartId={chart_id}&year={this_year}'
            yield scrapy.Request(url, callback=self.parse, cb_kwargs={'chart_id': chart_id, 'year': this_year})

                
    #---------------用以找到所有公司的連結，並傳給parse_data----------------#
    def parse(self, response, chart_id, year):
        soup = BeautifulSoup(response.text, 'html.parser')
        elems = soup.find_all('span', class_ = "name_1")
        # print(f"Total Company Number: {len(elems)}")
        self.num = 1
        for elem in elems:
            company = elem.find('a')
            company_link = company.get('href')
            if elem:
                yield scrapy.Request(url = 'https://vnr500.com.vn' + company_link, callback= self.parse_data, cb_kwargs={'chart_id': chart_id, 'year': year})
                

    #---------------用以從每個公司的連結中提取資料----------------#
    def parse_data(self, response, chart_id, year):
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            print(f'Error in connecting to website: {e}')
            return
        #存取回傳資料用
        SPIDER_POC_VNR500_ITEM = SpiderPocVnr500Item()
        SPIDER_POC_VNR500_ITEM['CHART_ID'] = chart_id
        SPIDER_POC_VNR500_ITEM['YEAR'] = year
        SPIDER_POC_VNR500_ITEM['INDEX'] = self.num
        self.num += 1
        #找出公司名稱
        COMPANY_NAME = soup.find_all('h2', {'class': 'home-title'})[0].text
        SPIDER_POC_VNR500_ITEM['COMPANY_NAME'] = COMPANY_NAME

        #找出公司資料表格
        column_names = ['COMPANY_VNR500_Rating', 'COMPANY_MDN', 'COMPANY_STOCK_CODE','COMPANY_HEADQUARTERS',
                        'COMPANY_TEL', 'COMPANY_FAX', 'COMPANY_EMAIL', 'COMPANY_WEB', 'COMPANY_FOUNDED_YEAR']
        company_info = soup.find('table', {'class': 'conpany_info'})
        rows = company_info.find_all('tr')
        for column_name, row in zip(column_names, rows):
            cols = row.find_all('td')
            cols = [col.text.strip() for col in cols]
            SPIDER_POC_VNR500_ITEM[column_name] = str(cols[1])

        #找出公司簡介
        company_summary = soup.find('div', {'class': 'dn-gioi-thieu'}).text
        SPIDER_POC_VNR500_ITEM['COMPANY_SUMMARY'] = company_summary.replace('\n', '').replace('\xa0', ' ')

        #找出公司管理層職位與姓名
        try:
            COMPANY_LEADER = {}
            company_leader = soup.find('table', {'class': 'ban_lanh_dao'})
            rows = company_leader.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [col.text.strip() for col in cols]
                COMPANY_LEADER["NAME"] = str(cols[0])
                COMPANY_LEADER["POSITION"] = str(cols[1])
            SPIDER_POC_VNR500_ITEM['COMPANY_LEADER'] = json.dumps(COMPANY_LEADER)
        except:
            SPIDER_POC_VNR500_ITEM['COMPANY_LEADER'] = None



        #找出公司新聞
        company_news = soup.find('div', {'class': 'item-news'})
        ttdn_items = company_news.find_all('div', {'class': 'col-xs-12 col-sm-6 ttdn-item'})
        news = {}
        index_num = 0
        for ttdn_item in ttdn_items:
            a_tag = ttdn_item.find('a')
            # 取得新聞連結
            a_link = a_tag['href']
            # 取得新聞title
            a_title = a_tag['title']
            # 取得新聞簡述
            post_intro = ttdn_item.find('p', {'class': 'post-intro'})
            post_intro = post_intro.text.replace('\n', '').replace('\xa0', ' ')
            # 取得新聞日期
            date = ttdn_item.find('p', {'class': 'date'})
            # 印出每一個 ttdn_item 的資訊
            news[index_num] = {'TITLE': str(a_title), 'LINK': str(a_link), 
                            'INTRO': str(post_intro), 'DATE': str(date.text)}
            index_num += 1
        SPIDER_POC_VNR500_ITEM['COMPANY_NEWS'] = json.dumps(news)

        yield SPIDER_POC_VNR500_ITEM



