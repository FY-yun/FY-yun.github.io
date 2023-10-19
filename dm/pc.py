import requests
from bs4 import BeautifulSoup
from html import escape

# 创建一个HTML文件
html_file = open("zy.html", "w", encoding='utf-8')

# 写入HTML文件的头部
html_file.write("<html>\n<head>\n<title>动画信息</title>\n")
html_file.write('<style>\n')
html_file.write('a.download-link { text-decoration: none; }\n')
html_file.write('a.download-link::after { content: " \u2193"; }\n')  # 添加下载图标
html_file.write('</style>\n')
html_file.write('<script>\n')
html_file.write('function copyMagnetLink(link) {\n')
html_file.write('  var textArea = document.createElement("textarea");\n')
html_file.write('  textArea.value = link;\n')
html_file.write('  document.body.appendChild(textArea);\n')
html_file.write('  textArea.select();\n')
html_file.write('  document.execCommand("copy");\n')
html_file.write('  document.body.removeChild(textArea);\n')
html_file.write('  alert("磁力链接已复制到剪贴板: " + link);\n')
html_file.write('}\n')
html_file.write('function cantCopyDownload(link) {\n')
html_file.write('  var confirmation = confirm("无法复制下载链接。是否要跳转到下载页面？");\n')
html_file.write('  if (confirmation) {\n')
html_file.write('    window.location.href = "https://fengyegf.com.cn/dm/zy.html";\n')
html_file.write('  }\n')
html_file.write('}\n')
html_file.write('</script>\n')
html_file.write('</head>\n<body>\n')

# 处理多个页面
for page in range(1, 3):
    # 发送HTTP请求获取网页内容
    url = f'https://dmhy.iwiki.icu/topics/list/page/{page}'
    response = requests.get(url)

    # 检查响应是否成功
    if response.status_code == 200:
        # 使用BeautifulSoup解析网页内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找所有带有指定属性的<td>标签
        td_tags = soup.find_all('td', {'width': '98'})
        times = [td.text.strip() for td in td_tags if '今天' in td.text.strip()]  # 只存储今天的时间

        td_tags = soup.find_all('td', {'nowrap': 'nowrap', 'align': 'center'})
        magnet_links = []  # 存储磁力链接
        for td in td_tags:
            # 查找包含磁力链接的<a>标签
            a_tag = td.find('a', {'class': 'download-arrow', 'title': '磁力下载'})
            if a_tag:
                magnet_link = a_tag.get('href')  # 获取<a>标签中的href属性值
                magnet_links.append(magnet_link)

        # 查找包含所需<a>标签的内容
        a_tags = soup.find_all('a', href=True, target='_blank')
        names = []  # 存储名称
        # 提取<a>标签中的文本内容，但排除指定的文本
        excluded_texts = ['tedmind.com', '22年4月番组表开放编辑', '动画资源标题格式说明', '搜索小提示',"意见建议"]
        for a_tag in a_tags:
            text_inside_a = a_tag.text  # 获取<a>标签中的文本内容
            # 排除包含指定文本的文本内容
            if not any(text in text_inside_a for text in excluded_texts):
                names.append(text_inside_a)

        # 写入时间，名称，下载链接到HTML文件
        for time, name, magnet_link in zip(times, names, magnet_links):
            download_link = f'<a class="download-link" href="javascript:void(0);" onclick="copyMagnetLink(\'{escape(magnet_link)}\')">{escape(name)}</a>'
            cant_copy_link = f'<a class="download-link" href="javascript:void(0);" onclick="copyMagnetLink(\'{escape(magnet_link)}\')">{escape(name)}</a>'
            html_file.write(f'<p>时间: {escape(time)}, 名称: {cant_copy_link}</p>\n')
    else:
        html_file.write('<p>无法获取网页内容。</p>\n')

# 写入HTML文件的尾部
html_file.write("</body>\n</html>")
html_file.close()
