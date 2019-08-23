# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import re


def get_html(url):
  try:
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    r.encoding = 'utf-8'
    return r.text
  except Exception as e:
    print(e)


def get_content(url):
  url_list = []
  html = get_html(url)
  soup = BeautifulSoup(html, 'lxml')
  category_list = soup.find_all('div', class_="index_toplist")
  history_finished_list = soup.find_all('div', class_="index_toplist")
  # 获取还未完本的小说
  for cate in category_list:
    # 获取当前tab的名字
    name = cate.find('div', class_="toptab").span.string
    # 写入txt中
    with open('novel.txt', 'w+', encoding='utf-8') as f:
      f.write("\n小说种类: {}".format(name))
    # 获取当前tab的小说
    general_list = cate.find(style='display: block;')
    book_list = general_list.find_all("li")
    # 遍历小说
    for book in book_list:
      # 获取link
      link = "http://www.qu.la/" + book.a['href']
      # 获取title
      title = book.a['title']
      # 链接插入url_list中
      url_list.append(link)
      # 写入txt文件中
      with open('novel.txt', 'w+', encoding='utf-8')as f:
        f.write('小说名:{:<}\t 小说地址：{:<}\n'.format(title, link))
  # 获取已经完本的小说
  for cate in history_finished_list:
    # 获取当前tab的名字
    name = cate.find("div", class_="toptab").span.string
    # 写入txt中
    with open('novel.txt', 'w+', encoding='utf-8') as f:
      f.write("\n小说种类{}\n".format(name))
    # 获取当前tab的小说
    general_list = cate.find(style='display: block;')
    book_list = general_list.find_all("li")
    # 遍历小说
    for book in book_list:
      # 获取link
      link = 'http://www.qu.la/' + book.a['href']
      # 获取title
      title = book.a['title']
      # 链接插入url_list中
      url_list.append(link)
      # 写入txt文件中
      with open('novel.txt', 'w', encoding='utf-8') as f:
        f.write("小说名：{:<} \t 小说地址：{:<} \n".format(title, link))
  url_list = list(set(url_list))
  return url_list


def get_txt_url(url):
  url_list = []
  html = get_html(url)
  soup = BeautifulSoup(html, 'lxml')
  lista = soup.find_all('dd')
  txt_name = soup.find('h1').text
  with open("./data/{}.txt".format(txt_name), 'w+', encoding='utf-8') as f:
    f.write('小说标题:{}\n'.format(txt_name))
    for url in lista:
      _url = 'http://www.qu.la' + url.a['href']
      _name = url.text
      if url.a['href'].find("book") != -1:
        f.write('章节名:{}\t 链接:{}\n'.format(_name, _url))
      url_list.append(url)

  return url_list, txt_name


def get_one_txt(url, txt_name):
  html = get_html(url).replace('<br />', '\n')
  soup = BeautifulSoup(html, 'lxml')
  try:
    txt = soup.find('div', id="content").text.replace('chaptererror();', '')
    title = soup.find('title').text.split('_')[0]

    with open("./data/{}.txt".format(txt_name + title), 'w+', encoding='utf-8') as f:
      f.write(txt)
  except Exception as e:
    print(e)


# url = 'https://www.qu.la/paihangbang/'
# get_content(url)
# url2 = 'http://www.qu.la//book/394/'
# get_txt_url(url2)
url3 = 'http://www.qu.la/book/394/296441.html'
get_one_txt(url3, '遮天')
