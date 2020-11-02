import os
from datetime import datetime

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

    
def save_markdown(filename, records, header, title):
    dst_records = ['## {}'.format(title)]
    dst_records.append('|'.join(header))
    dst_records.append('|'.join(['---']*len(header)))
    records = escape_records(records)
    for record in records:
        dst_records.append('|'.join(record))
    with open(filename, 'w', encoding='utf-8') as f:
        for item in dst_records:
            f.write(str(item) + '\n')


def crawler():
    response = requests.get('http://top.baidu.com/buzz?b=1')
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


if __name__ == '__main__':
    date_str = datetime.now().strftime('%Y%m%d')
    filename = '{}.md'.format(date_str)

    records = crawler()
    save_markdown(filename, records, header=['标题', '搜索指数'], title=date_str)


