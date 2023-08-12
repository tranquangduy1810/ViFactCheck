from bs4 import BeautifulSoup
import httpx
import pandas as pd
import Connection

topic =[]
title =[]
des =[]
content =[]
links=[]
tenbao=[]
date = []
news_type=[]
link_temp =[]
tenbao='VnExpress'
topiclist = {
"Thời sự": "https://vnexpress.net/thoi-su",
"Thế giới": "https://vnexpress.net/the-gioi",
"Kinh doanh": "https://vnexpress.net/kinh-doanh",
"Khoa học": "https://vnexpress.net/khoa-hoc",
"Bất động sản":"https://vnexpress.net/bat-dong-san",
"Giải trí":"https://vnexpress.net/giai-tri",
"Thể thao":"https://vnexpress.net/the-thao",
"Pháp luật":"https://vnexpress.net/phap-luat",
"Giáo dục":"https://vnexpress.net/giao-duc",
"Sức khoẻ":"https://vnexpress.net/suc-khoe",
}

def news_classifier(link):
  html = httpx.get(link,follow_redirects=True)
  soup = BeautifulSoup(html)
  if ("video" in link):
    a = (soup.find("h1",class_="title").get_text())
    b = (soup.find("div",class_="lead_detail").get_text(" ",strip=True))
    c = None
    d = (soup.find("span", class_="time").get_text())
    e= "Video"
    return a,b,c,d,e
  else:
    a = soup.title.get_text()
    b = (soup.find(attrs={"name": "description"}).attrs)['content']
    content_temp =""
    for i in soup.find_all("p"):
      content_temp += i.get_text("" ,strip=True)
    c = content_temp 
    d = (soup.find(attrs={"itemprop": "dateModified"}).attrs)['content']
    e= "Megazine"
    return a,b,c,d,e

def get_all_link(topiclist):
  for i in topiclist:
    print(topiclist[i])
    html = httpx.get(topiclist[i])
    soup = BeautifulSoup(html)
    for div in soup.find_all("h3" , class_="title-news"):
      links.append(div.find('a').get('href'))
      topic.append(i)

def parsing_link():
  content_temp=""
  for lk in links:
    html = httpx.get(lk,follow_redirects=True)
    soup = BeautifulSoup(html)
    try:
      a=(soup.find("h1",class_="title-detail").get_text())
      b=(soup.find("p", class_="description").get_text(strip=True))
      for i in soup.find_all("p",class_="Normal"):
        content_temp = content_temp + i.get_text() 
      c = content_temp
      d=(soup.find("span", class_="date").get_text(" ", strip=True))
      e="Text"
    except:
      a,b,c,d,e = news_classifier(lk)
      title.append(a)
      des.append(b)
      content.append(c)
      date.append(d)
      news_type.append(e)
    else: 
      title.append(a)
      des.append(b)
      content.append(c)
      date.append(d)
      news_type.append(e)


def df_to_DB():
  get_all_link(topiclist)
  parsing_link()
  df=pd.DataFrame([])
  df_temp = pd.DataFrame({ 'Title':title, 'Link':links, 'Topic':topic, 'Mô tả':des, "Nội dung":content,"Tên báo":tenbao, "Ngày đăng":date}) #Tạo DF
  df = pd.concat([df, df_temp], axis = 0, ignore_index=True) #nối DF
  df.to_csv("VNE.csv")




def main():
  df_to_DB()

if __name__ == "__main__":
    main()