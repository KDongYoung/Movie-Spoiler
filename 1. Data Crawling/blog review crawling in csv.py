from bs4 import BeautifulSoup
import requests
import urllib.request as req
import pandas as pd

def get_text(final_url):
   try :
      ##제목과 본문부분 추출
      res = req.urlopen(final_url)
      soup = BeautifulSoup(res, 'html.parser')
      temp = soup.select("#se_textarea")
      
      ##title 추출
      list=[]
      title = soup.head.find("meta", {"property":"og:title"}).get('content')
      list.append(title)


      ##본문 추출
      temp = soup.findAll("div", {"id":"postViewArea"})
      if temp == []:
          temp = soup.findAll("div", {"class":"se-module se-module-text"})
      if temp == []:
          temp = soup.findAll("p", {"class":"se_textarea"})

      text_str = ""
      for a in temp:
         text_str += a.get_text()
      list.append(text_str)
      list.append(final_url)
      return list
         
   except:
      print("크롤링실패")


f = open("url.txt", 'r')
lines = f.readlines()
results = []
movie_title={1:"겟아웃",2:"부산행",3:"서치",4:"해피데스데이",5:"곡성"}
for i, url in enumerate(lines):
    i += 1
    if i%20 == 0:
        results.append(get_text(url))
        data = pd.DataFrame(results)
        data = data.applymap(lambda x: x.replace('\xa0','').replace('\xa9','').replace('\u200b','').replace('\ufeff','').replace('\u119e',''))
        data.columns = ['title', 'contents', 'url']
        title = "%s_네이버블로그리뷰.csv" %(movie_title[i/20])
        data.to_csv(title, encoding = 'cp949')
        print("%s 파일생성 완료" %(movie_title[i/20]))
        results = []
    else:
        results.append(get_text(url))

f.close()
