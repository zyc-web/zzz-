#爬虫基本步骤

# 1.获取数据相应的地址链接
# 2.发送指定的地址请求，获取数据
# 3.对数据进行解析和清洗
# 4.保存数据
#主要使用
'''
Xpath对html进行数据格式转换
具体看代码吧，懒得写
'''
import requests
import parsel
import os
import time

# 1.获取数据相应的地址链接

def one_page(url):
    f_headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"}

    # 2.发送指定的地址请求，获取数据
    try:
        resopnse = requests.get(url,headers=f_headers)
        print(resopnse.status_code)
        page_html = resopnse.text   #获取的是网页的字符串（一般用re解析），用Xpath不能直接解析，必须进行数据格式转换
    except:
        print("wocao!有毒！！")
    # print(page_html)

    # 3.对数据进行解析和清洗,Xpath中的parsel
    selector = parsel.Selector(page_html) #数据类型转换
    #获取ID值为post-list的div下面ul中所有li标签,,,//表示跨结点
    lis = selector.xpath("//div[@id='post-list']/ul/li")
    for li in lis:
        pic_title = li.xpath('.//h2/a/text()').get() # 获取相册标题
        pic_link = li.xpath('.//h2/a/@href').get()  # 获取相册的链接
        print("正在下载相册：",pic_title)
        #创建文件夹保存图片集
        if not os.path.exists('img1\\'+pic_title):
            os.mkdir('img1\\'+pic_title)
        #请求相册的详情页数据
        response_pic = requests.get(url=pic_link, headers=f_headers).text
        #对数据进行格式转换
        selector1 = parsel.Selector(response_pic)
        pic_url_list = selector1.xpath("//div[@class='entry-content']//img/@src").getall()#获取每个图片的url地址
        #通过每个pic_url来获取图片
        # print(pic_url_list)
        #遍历每一个图片链接
        for pic_url in pic_url_list:
            #发送图片链接请求，获取图片二进制数据
            try:
                img_data= requests.get(url= pic_url,headers=f_headers).content  #content获取数据的二进制流
            except:
               print("有点小毛病，我直接忽略！")
    # 4. 图片数据保存
            #获取图片的名称
            file_name = pic_url.split("/")[-1]
            # print(file_name)

        #     #将数据写入文件
            with open(f"img1\\{pic_title}\\{file_name}",mode='wb') as f:#f为占位符，指定路径保存
                f.write(img_data)
                print("下载完成！",file_name)
                time.sleep(1)
    f.close()
if __name__ =="__main__":
    for i in range(4,16): #这里如果能够进一步优化，多线程爬取就好了，for循环啊太慢
        one_page('https://www.jdlingyu.com/tag/%e5%b0%91%e5%a5%b3/page/'+str(i))
print("all over!")























