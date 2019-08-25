# -*- coding: UTF-8 -*-
import requests
import bs4


def get_html(url):
  try:
    r = requests.get(url, timeout=80)
    r.raise_for_status()
    r.encoding = 'gbk'
    return r.text
  except Exception as e:
    print('err', e)


def get_content(url):
  html = get_html(url).replace("\n", '')
  soup = bs4.BeautifulSoup(html, 'lxml')

  movie_list = soup.find('ul', class_="picList")
  movies = movie_list.find_all("li")
  # 追加前先清空文件
  with open("./data.txt", 'r+', encoding='utf-8') as f:
    f.truncate()
  for top in movies:
    img_url = top.find('img')['src']
    name = top.find('span', class_="sTit").a.text
    # 防止时间字段不存在
    try:
      time = top.find('span', class_="sIntro").text
    except:
      time = "暂无上映时间"
    # 防止演员字段不存在
    try:
      actors = top.find('p', class_="pActor").find_all('a')
      actor = []
      for act in actors:
        actor.append(act.text)
      actor = ",".join(actor)
    except:
      actor = "暂无"
    # 防止介绍文案不存在
    try:
      intro = top.find('p', class_="pTxt pIntroHide").contents[0].strip()
    except:
      intro = top.find('p', class_="pTxt pIntroShow").contents[0].strip()
    # 写入
    with open("./data.txt", 'a+', encoding='utf-8') as f:
      f.write("片名：{}\n时间：{}\n演员：{}\n介绍：{} \n\n".format(name, time, actor, intro))
    # 写入的时候去掉时间戳，把有英文:的名字改成用中文连接
    with open("./img/" + name.replace(":", "：") + ".png", 'wb+') as f:
      f.write(requests.get('http:' + img_url.split("?")[0]).content)


url = 'http://dianying.2345.com/top/'
get_content(url)
