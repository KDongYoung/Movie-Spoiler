from bs4 import BeautifulSoup
import requests
import urllib.request as req
import pandas as pd

def get_text(final_url):
   try :
      ##Title, Body
      res = req.urlopen(final_url)
      soup = BeautifulSoup(res, 'html.parser')
      temp = soup.select("#se_textarea")
      
      ##Title
      list=[]
      title = soup.head.find("meta", {"property":"og:title"}).get('content')
      list.append(title)


      ##Body
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
         
   except: # Fail
      print("크롤링 실패")

# Write Naver Blog Review CSV File
f = open("url.txt", 'r')
lines = f.readlines()
results = []
movie_title={1:"겟아웃",2:"부산행",3:"서치",4:"해피데스데이",5:"곡성"} 
            # Get out, Train to Busan, Search, Happy Deathday, The Wailing
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
