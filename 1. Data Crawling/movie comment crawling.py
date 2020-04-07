import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

def get_data(url,resp,html):
    resp = requests.get(url)
    html = BeautifulSoup(resp.content, 'html.parser')
    score_result = html.find('div', {'class': 'score_result'})
    lis = score_result.findAll('li')
    results=[]
    for li in lis:        
        nickname = li.findAll('a')[0].find('span').getText()
        created_at = datetime.strptime(li.find('dt').findAll('em')[-1].getText(), "%Y.%m.%d %H:%M")
        review_text = li.find('p').getText()
    
        review=[nickname,review_text,created_at]
        results.append(review) 
    return results

# Write movie comment CSV File
f = open("네이버평점url.txt", 'r')
final_url = f.readlines()
movie_title={1:"겟아웃",2:"부산행",3:"서치",4:"해피데스데이",5:"곡성"}
              # Get out, Train to Busan, Search, Happy Deathday, The Wailing
for i,url in enumerate(final_url):
    resp = requests.get(final_url[i])
    html = BeautifulSoup(resp.content, 'html.parser')
    print("\n"+movie_title[i+1])
    final_result=[]
    for j in range(1,101):
        url = final_url[i] + '&page=' + str(j)
        print('url: "' + url + '" is parsing....')
        final_result.extend(get_data(url,resp,html))
    data = pd.DataFrame(final_result)
    data.columns = ['nickname', 'contents', 'datetime']
    title = "%s_네이버평점.csv" %(movie_title[i+1])
    data.to_csv(title, encoding = 'cp949')
    print("%s 파일 생성 완료" %(movie_title[i+1]))

    f.close()
