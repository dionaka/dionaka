# *爬虫*

## 爬虫基础之爬虫的基本介绍

- uri：统一资源标识符
- url：统一资源定位符，url是uri子集
- url组成：`scheme://[username:password@]host[:port][/path][;parameters][?query][#fragment]`

  - scheme资源使用协议：http,https,ftp
  - username:password：用户名与密码,访问ftp时会用到
  - host：主机地址，域名或ip
  - port：端口，http:80,https:443
  - path：资源在服务器地址
  - parameters：参数，用来指定访问某个资源时的附加信息
  - query：查询，多个查询用&隔开
  - fragment：片段，标识次级资源，用于单页面路由，html锚点
    - ?后查询字符发送服务器，fragment #不会
    - 默认Google搜索引擎忽略#后字符串，#！会被引擎读取

- 爬虫基本架构
  - 爬虫调度器
  - url管理器,通过内存、数据库、缓存数据库来实现
  - 网页下载器,伪装处理模拟浏览器访问、下载网页，常用库为 urllib、requests 等
  - 网页解析器
  - 数据储存器

- robots协议
  - 查看网站 robots 协议，网站 url 加上后缀 robotst.txt 即可

## HTTP协议的基本原理介绍

- 计算机网络模型
  - tcp/ip 4层模型
  - tcp/ip 5层模型
  - osi 7层模型

    - ### 应用层：主要协议

      - 文件传输协议
        - ftp (文件传输协议)
        - tftp (简单文件传输协议)

      - 远程登录与安全管理
        - telnet (远程登录协议)
        - ssh (安全外壳协议)
        - snmp (简单网络管理协议)

      - 超文本与网页
        - http (超文本传输协议)
        - https (安全超文本传输协议)

      - 邮件相关
        - smtp (简单邮件传输协议)
        - pop3 (邮局协议版本3)
        - imap (互联网消息访问协议)

      - 域名与配置
        - dns (域名系统协议)
        - dhcp (动态主机配置协议)

    - ### 表示层

    - ### 会话层

    - ### 传输层

      - tcp (传输控制协议)
      - udp（用户数据报协议）

    - ### 网络层

      - ip (internet协议)
      - icmp (internet控制报文协议)
      - igmp (igmp协议)
      - arp (arp协议)

    - ### 数据链路层

    - ### 物理层：负责传输比特流的硬件部分

- HTTP请求方法 ：GET、POST、PUT、DELETE、HEAD、OPTIONS、TRACE、CONNECT