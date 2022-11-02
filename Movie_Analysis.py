"""
@author: ‘WhiteRed‘
@software: PyCharm
@file: Movie_Analysis.py
@time: 2022/11/1 21:34
"""

import requests
import json
import jieba
from lxml import etree

class Reviews_Analysis:
    def __init__(self, headers={}):
        '''
        procedure SetUp
        :param headers: A request header is passed in. By default, the native header is used
        '''
        if headers == {}:  # 指定默认请求头
            self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
            }
        else:
            self.headers = headers

    def get_movie_link(self, reviews_count=100, print_mess=True):
        '''
        Get links to top 100 rated movie reviews
        :param reviews_count: The number of movie reviews crawled. The default is 100
        :param print_mess: Whether to print debugging information. The default value is True
        :return: Returns a list of links to movie reviews
        '''
        try:
            url_list = []  # 电影评论链接列表
            interger_count = reviews_count//25
            left_count = reviews_count - interger_count * 25
            for i in range(interger_count + 1):
                url = "https://movie.douban.com/top250?start=" + str(i * 25) + "&filter="
                # 发送get请求
                r = requests.get(url, headers=self.headers)
                r.encoding = r.apparent_encoding

                # 如果请求异常，则返回空列表
                if r.status_code < 200 or r.status_code > 299:
                    # 打印状态信息
                    print("第{}页爬取失败, 状态码:{}".format(i+1, r.status_code))
                else:
                    parse_html = etree.HTML(r.text)
                    data = parse_html.xpath("//div[@class='hd']/a/@href")
                    url_list += data

            if left_count:
                url_list = url_list[:reviews_count+left_count-1]

            if print_mess:
                print("已获取到%d条电影链接" % url_list.__len__())

            return url_list

        except Exception as e:
            print("In get_movie_link function:", e)
            return []

    def get_movie_commit(self, url, print_mess=False):
        '''
        Get a movie review and save it to a file
        :param url: You need to pass in a link to the movie review, in string format
        :param print_mess: Whether to print debugging information. The default value is False
        :return: Returns the number of comments retrieved
        '''

        url += 'reviews'  # 影评链接
        try:
            r = requests.get(url, headers=self.headers)
            r.encoding = r.apparent_encoding

            # 查看请求信息
            if r.status_code < 200 or r.status_code > 299:
                print("获取评论失败, 状态码:", r.status_code)
                return 0

            parse_html = etree.HTML(r.text)
            movie_name = parse_html.xpath("//div[@id='content']/h1/text()")[0]
            commit_id = parse_html.xpath("//div[@data-cid]/@data-cid")
            commits_len = 0
            with open("commits.txt", 'a+', encoding="utf-8") as f:
                for idx in commit_id:
                    commit_url = "https://movie.douban.com/j/review/" + str(idx) + "/full"
                    r = requests.get(commit_url, headers=self.headers)
                    r.encoding = r.apparent_encoding

                    words = json.loads(r.text)['body']
                    words = etree.HTML(words)
                    words = words.xpath("//p/text()")

                    commit = ""
                    for strings in words:
                        commit += strings

                    if commit != "":
                        commits_len += 1
                        f.write(commit)

            if print_mess:
                print("{}获取了{}条评论".format(movie_name, commits_len))
            return commits_len

        except Exception as e:
            print("In get_movie_commit function:", e)
            return 0

    def load_stopwords(self):
        '''
        Gets the stop list. The default is to use the built-in stop list
        :return: Return a list of stop words
        '''

        # 停用词列表
        stopwords = [' ', '\n']

        # 中文停用词
        with open("stopwords/cn_stopwords.txt", 'r', encoding='utf-8') as f:
            for line in f:
                line = line.replace('\n', '')
                stopwords.append(line)

            f.close()

        # 英文停用词
        with open("stopwords/en_stopwords.txt", 'r', encoding='utf-8') as f:
            for line in f:
                line = line.replace('\n', '')
                stopwords.append(line)

            f.close()

        return stopwords

    def word_fre_analysis(self, file_dir, print_mess=False, use_stopwords=True):
        '''
        Analyze the most frequent words in the dictionary and order them from most to least frequent
        :param print_mess: Whether to print debugging information. The default value is False
        :param use_stopwords: Whether to use the stop word. The default is True
        :param file_dir: Comment file path, default in the project directory
        :return: Returns the high frequency dictionary and the dictionary length
        '''

        if use_stopwords:
            stopwords = self.load_stopwords()
        else:
            stopwords = []

        # 构建词频字典
        word_fre_dct = {}
        with open(file_dir, 'r', encoding='utf-8') as f:
            for line_words in f:
                for word in jieba.lcut(line_words):  # 使用jieba库进行分词
                    if word not in stopwords and word.__len__() > 1:  # 使用停用词表过滤停用词
                        word_fre_dct[word] = word_fre_dct.get(word, 0) + 1

            f.close()

        # 按照词频从大到小排序
        def cmp(x):
            return (-x[1], x[0])  # 你好 1023

        # 词频排序
        word_fre_list = sorted(word_fre_dct.items(), key=cmp)
        # 构建高频词典
        word_high_fre_dct = {}
        with open("word_high_fre.txt", 'w+', encoding='utf-8') as f:
            for idx, (word, number) in enumerate(word_fre_list):  # 获取索引,词语和词频信息
                word_fre_dct[word] = number
                if number >= 100:
                    word_high_fre_dct[word] = number
                    f.write("{:<4} {:<5} {:}\n".format(idx + 1, word, number))
                    if print_mess and idx < 100:  # 打印前100条高频词
                        try:
                            print("{:<4} {:<5} {:}".format(idx + 1, word, number))
                        except:
                            pass
                else:
                    break
            f.close()

        return word_high_fre_dct, word_fre_dct.__len__()

    def load_word_fre_file(self, word_fre_path):
        '''
        Load the word frequency file into a dictionary
        :param word_fre_path: Dictionary path
        :return: Return a dictionary
        '''
        word_fre_dict = {}
        with open(word_fre_path, 'r', encoding='utf-8') as f:
            for word in f:
                word = word.split()
                word_fre_dict[word[1]] = int(word[2])

            f.close()

        return word_fre_dict