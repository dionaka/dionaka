#命令行
#playwright codegen 
# -o <filename>将生成的脚本保存到指定文件
# -b <browser>指定要使用的浏览器，默认为 chromium。可选值包括 chromium、firefox、webkit
# --target <language>指定生成的脚本语言，默认为 Python。可选值包括 python、javascript、csharp、java
# --save-trace <filename>记录会话的跟踪并将其保存到文件中，便于调试
# --timeout <milliseconds>页面加载的超时时间，单位为毫秒
# --user-agent <user-agent-string>
# --viewport-size <width>,<height>指定浏览器窗口的大小，格式为 宽度,高度
"""
<meta charset="utf-8">
<p>pip install playwright</p>
<p>playwright install安装完成后仍会报错找不到chrome_elf.dll文件,</p>
<p>即使从chrom安装目录将此文件补充到该目录仍会报错(Error: Target page, context or browser has been closed)</p>
<p>此时定位到报错所显示的目录，找到“chromium-1148”文件，</p>
<p>通过playwright install运行时控制台显示的压缩包下载地址自行下载</p>
<p>解压完成后，替换并改名为“chromium-1148”</p>
<p>接下来可以在控制台使用自动化命令来测试 playwright codegen -o script.py</p>
"""
#定位元素由自动化程序进行
#需要自行设置等待
"""
#固定等待1秒
page.wait_for_timeout(1000)
#等待事件
page.wait_for_event(event)
#等待加载状态
page.get_by_role("button").click()
page.wait_for_load_state()
"""
"""
#添加事件发起请求时打印URL
page.on("request",print_request_sent)
#请求完成时打印URL
page.on("requestfinished",print_request_finished)
page.goto("https://baidu.com")
#删除事件
page.remove_listener("requestfinished", print_request_finished)
"""
#反检测
"""withopen('./stealth.min.js','r') as f:
js=f.read()
#添加UserAgent
page = browser.new_page(
user_agent='Mozilla/5.0(Windows NT 10.0;Win64;x64)AppleWebKit/537.36(KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
)
#执行JS代码
page.add_init_script(js)
"""