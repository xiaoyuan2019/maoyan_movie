import requests
from lxml import etree
import pymysql,re,json

def get_HTMLcontent(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
    try:
        r = requests.get(url, headers=headers, timeout=30).text  # 模拟浏览器抓取url网页内容
        s = etree.HTML(r)
        return s
    except:
        return '获取网页内容异常'

def parse_html(s):
    # 利用xpath解析网页信息
    movie_list = s.xpath('//div[@class="movies-channel"]//dd')  # 相对路径，定位class为movie-list的d1标签
    title_list = []
    img_list = []
    score_list = []
    # 循环每个dd标签，使用xpath获取相关信息，并加入对应列表中
    for item in movie_list:
        title = item.xpath('./div[2]/a/text()')[0]  # 绝对路径，获取当前dd标签内的第二个div下面的a标签的内容，即电影名称
        title_list.append(title)
        # //*[@id="app"]/div/div[2]/div[2]/dl/dd[3]/div[1]/a/div/img[2]
        img = item.xpath('./div[1]/a/div/img[2]/@data-src')[0]  # 电影图片url
        img_list.append(img)
        score_tmp = item.xpath('./div[3]/text()') # 绝对路径，获取评分div是否有评分
        if '暂无评分' in score_tmp:
            score_list.append('暂无评分')
        else:
            score1 = item.xpath('./div[3]/i[1]/text()')  # 绝对路径，第一个评分
            score2 = item.xpath('./div[3]/i[2]/text()')  # 绝对路径，第二个评分
            score = [i + j for i, j in zip(score1, score2)]
            score_list.extend(score)
    # print(score_list, len(score_list))
    # print(img_list,len(img_list))
    # print(title_list,len(title_list))
    # print(img,len(img))
    # 通过yield生成器，将电影的3个信息一一对应起来形成字典格式，并逐一返回，前提是各信息列表的长度一致
    for i in range(len(title_list)):
        yield {
            'img': img_list[i],
            'title': title_list[i].replace("'", ' '),  # 替换掉单引号，避免存入数据库时产生语法错误
            'score': score_list[i],
        }

def save_to_db(info):
    conn = pymysql.connect(host='10.195.251.148', port=3306,
                           user='root', passwd='fhwsie', db='maoyan', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("insert into comedy2019 (title, score, img) \
     values ('{0}', '{1}', '{2}')".format(info['title'], info['score'], info['img'] ))
    conn.commit()
    cursor.close()
    conn.close()

def delete_table_data():
    conn = pymysql.connect(host='10.195.251.148', port=3306,
                           user='root', passwd='fhwsie', db='maoyan', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("delete from comedy2019;")
    conn.commit()
    cursor.close()
    conn.close()

def save_to_txt(content):
    with open('comedy2019.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False)+'\n')
        f.write('='*50+'\n')

if __name__ == '__main__':
    # 运行脚本之前，先清空表中数据，避免数据重复，保证电影信息是最新的
    delete_table_data()
    for i in range(5):
        # 豆瓣每一页显示25部电影，每一页的页面url是第一部电影的序号
        url = 'https://maoyan.com/films?showType=3&catId=2&yearId=14&offset={}'.format(i*30)
        result = parse_html(get_HTMLcontent(url))  # 解析网页内容，获取电影信息
        for item in result:
            # 写入txt文件
            # save_to_txt(item)
            # 写入数据库
            save_to_db(item)