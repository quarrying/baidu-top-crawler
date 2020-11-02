import os
from datetime import datetime
from collections import OrderedDict

import requests
from bs4 import BeautifulSoup


def escape_records(records):
    dst_records = []
    for record in records:
        dst_record = []
        for part in record:
            dst_record.append(part.replace('|', '\|'))
        dst_records.append(dst_record)
    return dst_records

    
def save_markdown(filename, records, header):
    records = escape_records(records)
    dst_records = ['|'.join(header)]
    dst_records.append('|'.join(['---']*len(header)))
    for record in records:
        dst_records.append('|'.join(record))
    with open(filename, 'w', encoding='utf-8') as f:
        for item in dst_records:
            f.write(str(item) + '\n')


def crawler(buzz_no=1):
    response = requests.get('http://top.baidu.com/buzz?b={}'.format(buzz_no))
    response.encoding = 'gb18030'
    soup = BeautifulSoup(response.text, 'html.parser')
    table_tag = soup.find('table', {'class': 'list-table'})
    item_tags = table_tag.find_all('tr')
    keywords, search_indices = [], []
    for item in item_tags:
        keyword_tag = item.find('td', {'class': 'keyword'})
        last_tag = item.find('td', {'class': 'last'})
        if (keyword_tag is not None) and (last_tag is not None):
            keyword_title_tag = keyword_tag.find('a', {'class': 'list-title'})
            keywords.append(keyword_title_tag.text.strip())
            search_indices.append(last_tag.text.strip())
    return zip(keywords, search_indices)


def crawler_names():
    category_buzz_no = OrderedDict([
        ('热点人物',    258), 
        ('名家人物',    260), 
        ('公益人物',    612), 
        ('财经人物',    261), 
        ('体坛人物',    255), 
        ('主持人',      454), 
        ('历史人物',    259), 
        ('互联网人物',  257), 
        ('女明星',      1570), 
        ('男明星',      1569),
        ('欧美明星',    491),
    ])
    date_str = datetime.now().strftime('%Y%m%d')
    for category, buzz_no in category_buzz_no.items():
        records = crawler(buzz_no=buzz_no)
        filename = '{} 人物之{}.md'.format(date_str, category)
        save_markdown(filename, records, header=['关键词', '搜索指数'])


if __name__ == '__main__':
    date_str = datetime.now().strftime('%Y%m%d')
    filename = '{} 今日热点.md'.format(date_str)

    records = crawler()
    save_markdown(filename, records, header=['标题', '搜索指数'])
    crawler_names()


