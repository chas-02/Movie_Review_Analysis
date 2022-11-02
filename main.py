"""
@author: ‘WhiteRed‘
@software: PyCharm
@file: main.py
@time: 2022/10/31 16:54
"""

import stylecloud
from Movie_Analysis import Reviews_Analysis

if __name__ == '__main__':
    # 创建词频统计对象
    Movie_Analysis = Reviews_Analysis()
    # 获取top100电影评论链接的列表
    url_list = Movie_Analysis.get_movie_link(reviews_count=105)
    print(url_list)

    # # 统计评论数量
    # size_commit = 0
    # for url_commit in url_list:
    #     size_commit += Movie_Analysis.get_movie_commit(url_commit, print_mess=True)  # 影评写入到文件中，并打印爬虫信息
    # print("共获取到%d条评论" % size_commit)
    #
    # print("开始统计高频词...")
    # word_high_fre_dct, word_fre_len = Movie_Analysis.word_fre_analysis(file_dir="commits.txt", print_mess=True)
    # print("词典大小:{} 共统计了{}个高频词".format(word_fre_len, word_high_fre_dct.__len__()))
    #
    # # 使用stylecloud库绘制词云图
    # stylecloud.gen_stylecloud(file_path="word_high_fre.txt",  # 指定词频路径
    #                           icon_name='fas fa-thumbs-up',  # 指定词云形状名称
    #                           stopwords=False,  # 不使用停用词
    #                           font_path='C:\\Windows\\Fonts\\simhei.ttf',  # 指定字体文件，避免中文乱码
    #                           output_name='wordscloud.png',  # 指定输出图片名称
    #                           )
    # print("已绘制词云图")
