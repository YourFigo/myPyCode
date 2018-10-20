import my_mysql
import matplotlib.pyplot as plt
import matplotlib

# 迭代器
# x = [(1,2),(3,4),(5,6)]
# y = [y[0] for y in x]

# 对sql语句的搜索结果取前topNum个记录
# 返回[4*topNum个搜索结果,搜索结果中分title计数结果中的title_name，搜索结果中分title计数结果中的title_num]
def title_top(topNum = 100):
    # 用于配合 selectSql 组成四个维度的sql语句
    orderName = ['wk.collectNum', 'wk.replyNum', 'wk.likeNum', 'wk.commentNum']
    order_results = []
    for li in orderName:
        selectSql = 'SELECT wk.keyword,wk.title,wk.collectNum,wk.replyNum,wk.likeNum,wk.commentNum FROM tb_wukong wk ORDER BY ' + li + ' DESC;'
        order_results.append(my_mysql.selectTable(selectSql))
    # 从 收藏、回答、点赞、评论 四个维度，各取topNum，每个topNum存为 result_topNum_4 的一个元素，每个topNum有topNum个元素
    topNum = topNum
    result_topNum_4 = []
    for result in order_results:
        result_topNum = result[0:topNum]
        result_topNum_4.append(result_topNum)
    # top_all_in = []
    # for i in result_topNum_4[0]:
    #     if i in result_topNum_4[1] and i in result_topNum_4[2] and i in result_topNum_4[3]:
    #         top_all_in.append(i)

    dic_title = {
        "科技": 0, "美食": 0, "军事": 0, "财经": 0, "动漫": 0, "汽车": 0, "热门": 0, "国际": 0, "育儿": 0, "旅游": 0,
        "三农": 0, "文化": 0, "数码": 0, "家居": 0, "时尚": 0, "科学": 0, "游戏": 0, "历史": 0, "收藏": 0,
        "健康": 0, "心理": 0, "电影": 0, "教育": 0, "宠物": 0, "职场": 0, "娱乐": 0, "社会": 0, "体育": 0
    }
    print(dic_title.keys())
    print(dic_title.values())

    # 这400个数据中，只要出现一次 专题，就对字典对应的key的value加一操作，统计每个 专题出现的频数
    for result_topNum in result_topNum_4:
        for one in result_topNum:
            if one[0] in dic_title:
                value = dic_title[one[0]]
                dic_title[one[0]] = value + 1
            else:
                print(one[0], ' not in dic_title')

    sum = 0
    # 输出操作后的字典的 key-value对 和其中value的总和
    # 迭代的过程中删除会报错 RuntimeError: dictionary changed size during iteration
    delKeys = []
    for key in dic_title:
        print(key, ' -- ', dic_title[key])
        sum = sum + dic_title[key]
        if dic_title[key] <= 10:
            delKeys.append(key)
            # del dic_title[key]
    print('sum = ', sum)
    # for delKey in delKeys:
    #     del dic_title[delKey]

    x = dic_title.items()
    # sorted() 对 可迭代对象有效，item 代表 dic_title.items() 在某一次迭代中的值，而item这个元祖有两个数据：key和value
    print(sorted(dic_title.items(), key=lambda item: item[1], reverse=True))
    # 对 专题数进行降序排序，排序后的结果为可迭代对象 [(title1,num1),(title2,num2),...]
    title_num_from_top_100 = sorted(dic_title.items(), key=lambda item: item[1], reverse=True)
    # 通过迭代器分别获得 [(title1,num1),(title2,num2),...] 中的 [title1,title2,...] 和 [num1,num2,...]

    title_name = [x[0] for x in title_num_from_top_100]
    title_num = [x[1] for x in title_num_from_top_100]
    print(title_name)
    print(title_num)
    return [result_topNum_4, title_name, title_num]

# 取前 maxNum 个title 画条形图
def title_bar_plot(title_name,title_num,maxNum = 10):
    # 设置中文字体和负号正常显示
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    matplotlib.rcParams['axes.unicode_minus'] = False

    # 条形图
    plt.figure()
    rects = plt.bar(title_name[0:maxNum], title_num[0:maxNum], width=0.4)
    # 设置横纵坐标的名称以及对应字体格式
    font2 = {
        'weight': 'normal',
        'size': 12
    }
    plt.ylabel('频数', font2)
    plt.xlabel('专题名', font2)
    plt.title('收藏、回答、点赞、评论四个维度各取top100后，400个数据分专题频数统计(取前10)', font2)
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height + 0.3, str(height), ha="center", va="bottom")

# 取前 maxNum 个title 画饼图
def title_pie_plot(title_name,title_num,maxNum = 10):
    # 饼图
    # 设置中文字体和负号正常显示
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    matplotlib.rcParams['axes.unicode_minus'] = False
    plt.figure()
    plt.pie(title_num[0:maxNum], labels=title_name[0:maxNum], autopct='%3.1f%%')
    font2 = {
        'weight': 'normal',
        'size': 12
    }
    plt.title('收藏、回答、点赞、评论四个维度各取top100后，400个数据分专题占比(取前10)', font2)
    # plt.legend(loc=0,ncol=2)
    plt.axis('equal')
    plt.show()

if __name__ == '__main__':
    # 获得专题的记录数
    selectCountSql = 'SELECT keyword,COUNT(*) AS num FROM tb_wukong GROUP BY keyword ORDER  BY num DESC'
    countResult = my_mysql.selectTable(selectCountSql)
    print('-----悟空问答大家关注的专题top5-----')
    for i in range(5):
        print('第 {} 名：'.format(i + 1),countResult[i][0])

    resultList = title_top(100)

    result_top_num = 10
    result_top100_4 = resultList[0]
    result_top100_collectNum = result_top100_4[0]
    result_top100_replyNum = result_top100_4[1]
    result_top100_likeNum = result_top100_4[2]
    result_top100_commentNum = result_top100_4[3]
    print('-----悟空问答 收藏数 top10的问题-----')
    for i in range(result_top_num):
        print('第 {} 名：'.format(i + 1),result_top100_collectNum[i][1])
    print('-----悟空问答 回答数 top10的问题-----')
    for i in range(result_top_num):
        print('第 {} 名：'.format(i + 1),result_top100_replyNum[i][1])
    print('-----悟空问答 点赞数 top10的问题-----')
    for i in range(result_top_num):
        print('第 {} 名：'.format(i + 1),result_top100_likeNum[i][1])
    print('-----悟空问答 评论数 top10的问题-----')
    for i in range(result_top_num):
        print('第 {} 名：'.format(i + 1),result_top100_commentNum[i][1])


    title_name = resultList[1]
    title_num = resultList[2]
    title_bar_plot(title_name,title_num)
    title_pie_plot(title_name,title_num)