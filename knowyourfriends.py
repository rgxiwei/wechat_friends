# -*- coding: UTF-8 -*-
from wxpy import *
import os
import re
import jieba
import pandas as pd 
import matplotlib.pyplot as plt
from scipy.misc import imread
from wordcloud import WordCloud,ImageColorGenerator
import numpy

def login():
    #初始化机器人
    bot=Bot()
    #获取所有微信好友
    my_friends=bot.friends()
    print (my_friends)
    return my_friends

def show_sex_ratio(friends):
    #使用一个字典来存储男生和女生的数量
    sex_dict={'male':0,'female':0}

    for friend in friends:
        if friend.sex==1:
            sex_dict['male']+=1
        elif friend.sex==2:
            sex_dict['female']+=1
    print(sex_dict)

def show_area_distribution(friends):
    #使用一个字典统计各省好友数量
    provinence_dict={'北京':0,'上海':0,'天津':0,'重庆':0,
        '河北':0,'山西':0,'吉林':0,'辽宁':0,'黑龙江':0,
        '陕西':0,'甘肃':0,'青海':0,'山东':0,'福建':0,
        '浙江':0,'台湾':0,'河南':0,'湖北':0,'湖南':0,
        '江西':0,'江苏':0,'安徽':0,'广东':0,'海南':0,
        '四川':0,'内蒙':0,'贵州':0,'云南':0,'新疆':0,
        '宁夏':0,'广西':0,'西藏':0,'香港':0,'澳门':0,
        '海外':0}
    
    #统计省份
    for Friend in friends:
        if Friend.province in provinence_dict.keys():
            provinence_dict[Friend.province]+=1
        else:
            provinence_dict['海外']+=1
    
    #为方便数据的呈现，生产Json格式
    data=[]
    for key,value in provinence_dict.items():
        data.append({'name':key,'value':value})
    print(data)

def write_txxt_file(path,txt):
    #xieru
    with open(path ,'a',encoding='gb18030',newline='') as f:
        f.write(txt)

def read_txt_file(path):
    with open(path,'r',encoding='gb18030',newline='') as f:
        return f.read()

def show_signature(friends):
    #tongji
    for friend in friends:
        #对所有数据进行清洗，将标点符号等去掉
        pattern=re.compile(r'[一-龥]+')
        filterdata=re.findall(pattern,friend.signature)
        write_txxt_file('signature.txt',''.join(filterdata))

    
def geb_cloudimg():
        #读取文件
    content=read_txt_file('signature.txt')
    segment=jieba.lcut(content)#切词
    words_df=pd.DataFrame({'segment':segment})#生产航列表
    
    #读取stop words
    stopwords=pd.read_csv('stopwords.txt',index_col=False,quoting=3,sep=" ",names=['stopword'])
    words_df=words_df[~words_df.segment.isin(stopwords.stopword)]
    print(words_df)

    words_stat=words_df.groupby(by=['segment'])['segment'].agg({'计数':numpy.size})
    words_stat=words_stat.reset_index().sort_values(by=['计数'],ascending=False)

    #设置云词属性
    color_mask=imread('background.jpg')
    wordcloud=WordCloud(font_path="simhei.ttf",
                    background_color="white",
                    max_words=100,
                    mask=color_mask,
                    max_font_size=100,
                    random_state=42,
                    width=1000,height=860,margin=2,
                    )
    word_frequence={x[0]:x[1]for x in words_stat.head(100).values}
    print (word_frequence)
    word_frequence_dict={}
    for key in word_frequence:
        word_frequence_dict[key]=word_frequence[key]

    wordcloud.generate_from_frequencies(word_frequence_dict)
    image_colors=ImageColorGenerator(color_mask)
    wordcloud.recolor(color_func=image_colors)
    wordcloud.to_file('output.png')
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()

def main():
    # friends=login()
    # show_sex_ratio(friends)
    # show_area_distribution(friends)
    # show_signature(friends)
    geb_cloudimg()

if __name__=='__main__':
    main()