简介：使用Scrapy框架，爬取京东上某件(些)商品的评价，通过MongoDB存储数据。

# 配置环境

- python：3.7.9
- scrapy：2.4.1
- pymongodb：3.11.4
- MongoDB：4.4.6

# 使用

步骤：

- 找到想要抓取的商品的购买页，在"商品介绍"找到商品编号，复制到`productIds`列表中；
- 将`settings.py`中的`MONGODB_URI`修改为自己的MongoDB的URI。
- 在本级目录下，`PowerShell`运行：`scrapy crawl comment jd_comment_spider`即可。或者，直接运行`begin_spider.py`文件。

# ProxyIP

可在ProxyIP.txt中写入代理ip地址和端口，每次请求会通过代理发送。txt文档中每行为一个代理地址，格式为：`ip地址:端口`。

爬虫启动时，会读取PorxyIP.txt中的所有地址，写入到`PROXY_LIST`中，再添加一个None元素，表示不通过代理。每次发送请求时，会在`PROXY_LIST`中随机抽取一个代理地址。

# Todo

- [x] 增加代理IP池
- [ ] 增加随机User Agent
- [ ] 将爬取过的商品号和页面放入数据库，在发送请求前对url进行去重处理

