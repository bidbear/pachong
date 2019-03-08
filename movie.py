import requests
from requests.exceptions import RequestException
import re
from multiprocessing import Pool
import json
def get_one_page(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return  r.text
        return None
    except RequestException:
        return None

def parse_result(result):
    patterns = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)" .*?name.*?<a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?</dd>',re.S)
    items = re.findall(patterns,result)
    for item in items:
        yield dict(index=item[0], img=item[1], title=item[2], yanyuan=item[3].strip()[3:], time=item[4].strip()[5:])
def write_to_text(content):
    with open('test.txt','a+',encoding='utf-8') as file:
        file.write(json.dumps(content,ensure_ascii=False)+'\n')

def main(num):
    url = 'https://maoyan.com/board/4?offset='+str(num)
    result = get_one_page(url)
    # print(result)
    list_re = parse_result(result)
    for list in list_re:
        write_to_text(list)
if __name__ == '__main__':
    # for i in range(10):
    #     main(i*10)
    p =Pool(4)
    p.map(main,[i*10 for i in range(10)])

