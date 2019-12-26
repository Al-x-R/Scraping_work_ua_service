import requests
from bs4 import BeautifulSoup as BS
import time

session = requests.Session()
# для обхода блокировки прописываем headers
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }
#base_url = 'https://www.work.ua/jobs-zaporizhzhya-python/'
base_url = 'https://www.work.ua/jobs-kyiv-python/'
domain = 'https://www.work.ua'
jobs = []
urls = []
urls.append(base_url)

# делаем запрос
req = session.get(base_url, headers=headers)
if req.status_code == 200:
    bsObject = BS(req.content, 'html.parser')
    pagination = bsObject.find('ul', attrs={'class': 'pagination'})
    if pagination:
        pages = pagination.find_all('li', attrs={'class': False})
        for page in pages:
            urls.append(domain+page.a['href'])

for url in urls:
    time.sleep(2.0)
    req = session.get(url, headers=headers)
    if req.status_code == 200:
        bsObject = BS(req.content, 'html.parser') #структура стринички
        div_lis = bsObject.find_all('div', attrs={'class': 'job-link'})
        for div in div_lis:
            title = div.find('h2')
            price = div.find('b').text
            description = div.p.text # для того чтоб не прогонять постоянно по атрибутам т.к. р в диве только 1
            href = title.a['href']
            company = 'no name'
            logo = div.find('img')
            if logo:
                company = logo['alt']
            jobs.append({
                'company': company,
                'title': title.text,
                'price': price,
                'description': description,
                'href': domain + href
            })
    # print(price)
    # print(description)
    # print(domain + href)
#data = bsObject.prettify()#encode('utf8')

template = '<!doctype html><html lang="en"><head><meta charset="utf-8"></head><body>'
end = '</body></html>'
content = '<h2> Work.ua</h2>'
for job in jobs:
    content += '<a href="{href}" target="_blank">{title}</a><br/><p>Зарплата: {price}</p><br><p>{description}</p><p>{company}</p><br/>'.format(**job)
    content += '<hr/><br/><br/>'

data = template + content + end
handle = open('jobs.html', 'w')
handle.write(str(data))
handle.close()