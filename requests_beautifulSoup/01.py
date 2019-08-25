import requests
from bs4 import BeautifulSoup

def get_html(url):
  try:
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    r.encoding = 'utf-8'
    return r.text
  except:
    return " ERROR "


def get_content(url):
  content = []
  html = get_html(url)
  soup = BeautifulSoup(html, 'lxml', )
  liTags = soup.find_all('li', class_='j_thread_list clearfix')
  for li in liTags:
    obj = {}
    try:
      obj['title'] = li.find('div', class_='j_th_tit').text.strip()
      obj['link'] = "http://tieba.baidu.com/" + li.find('a', class_="j_th_tit")['href']
      obj['name'] = li.find('span', class_='tb_icon_author').text.strip()
      obj['time'] = li.find('span', class_='pull-right is_show_create_time').text.strip()
      obj['replyNum'] = li.find('span', class_='threadlist_rep_num center_text').text.strip()
      content.append(obj)
    except Exception as e:
      print('���˵�С����')
      print(e)
  return content


def out_file(dict):
  with open('data.txt', 'a+', encoding='utf-8') as f:
    for comment in dict:
      f.write('���⣺ {} \t ���ӣ�{} \t �����ˣ�{} \t ����ʱ�䣺{} \t �ظ������� {} \n'.format(
        comment['title'], comment['link'], comment['name'], comment['time'], comment['replyNum']))

  print('�������')


def main(base_url, deep):
  list = []
  # ��ȡҳ��
  for i in range(0, deep):
    list.append(base_url + '&pn=' + str(50 * i))
  # ѭ������
  for url in list:
    content = get_content(url)
    # д���ļ���
    out_file(content)


deep = 3
base_url = 'http://tieba.baidu.com/f?kw=%E8%A5%BF%E5%AE%89%E9%82%AE%E7%94%B5%E5%A4%A7%E5%AD%A6&fr=index&red_tag=v2541657634&ie=utf-8'
if __name__ == '__main__':
  main(base_url, deep)
