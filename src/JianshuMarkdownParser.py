# HTML Tools

from HTMLParser import HTMLParser

import re
import os
import sys
import string

# Network
import urllib2
from bs4 import BeautifulSoup

def get_basic_imformation(dic):
    ccc = 1

def get_jianshu_html(url_code):
    url = "http://www.jianshu.com/p/" + url_code
    # url = "http://www.jianshu.com/p/99af00237cb8"
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36')
    con = urllib2.urlopen(req)
    doc = con.read()
    soup = BeautifulSoup(doc, "lxml")
    myStr = ''
    find_part = soup.find_all(class_='show-content')

    for one in find_part:
        for one_tag in one.children:
            myStr = myStr + str(one_tag)
            myStr = myStr + '\n'
    return myStr

def rep_p(html_code):
    html_code = html_code.replace('<p>', '')
    html_code = html_code.replace('</p>', '\n')
    html_code = html_code.replace('<br/>', '\n')
    return html_code

def rep_hr(html_code):
    html_code = html_code.replace('<hr/>', '---')
    html_code = html_code.replace('<hr>', '---')
    return html_code

def rep_a(html_code):
    tags = re.findall(r'<a.+?href=.+?>.+?</a>', html_code)
    rex = re.findall(r'<a href="(.*?)" target="(.*?)">(.*?)</a>', html_code)
    if len(tags) == len(rex):
        for i in range(0, len(tags)):
            href = rex[i][0]
            target = rex[i][1]
            inner = rex[i][2]
            new_string = '[' + inner + '](' + href + ')'
            html_code = html_code.replace(tags[i], new_string)
    return html_code

def rep_h(html_code):
    tags = re.findall(r'<h[^<]>', html_code)
    rex = re.findall(r'<h(.*?)>', html_code)
    if len(tags) == len(rex):
        for i in range(0, len(tags)):
            n = int(rex[i])
            new_string = ''
            for j in range(0, n):
                new_string = new_string + '#'
            new_string = new_string + ' '

            strinfo = re.compile(tags[i])
            html_code = strinfo.sub(new_string, html_code)

    tags = re.findall(r'</h[^<]>', html_code)
    for cle in tags:
        html_code = html_code.replace(cle, '')

    return html_code



def rep_pre(html_code):
    html_code = html_code.replace('<pre><code>', '{% highlight ruby %}\n')
    # <pre><code class="Objective-C">
    html_code = re.sub(r'<pre><code.+?>', '{% highlight ruby %}\n', html_code)
    html_code = html_code.replace('</code></pre>', '\n{% endhighlight %}')

    return html_code

def rep_img(html_code):
    tags = re.findall(r'<img.+?/>', html_code)
    rex = re.findall(r'<img .*? src="(.*?)"/>', html_code)
    if len(tags) == len(rex):
        for i in range(0, len(tags)):
            src = rex[i]
            tag = tags[i]
            new_string = '![](' + src + ')'
            html_code = html_code.replace(tag, new_string)
    return html_code

def del_div(html_code):
    # (r'<a.+?href=.+?>.+?</a>', html_code)
    html_code = re.sub(r'<div.+?>', '', html_code)
    html_code = re.sub(r'</div>', '', html_code)
    html_code = html_code.replace('<b>', '')
    html_code = html_code.replace('</b>', '')
    return html_code

def rep_strong(html_code):

    html_code = html_code.replace('<strong>', '**')
    html_code = html_code.replace('</strong>', '**')
    return html_code

def rep_code(html_code):
    html_code = html_code.replace('<code>', '`')
    html_code = html_code.replace('</code>', '`')
    return html_code

def GuaScriptMarkdownParserStartUp(buff):
    post = get_jianshu_html(buff)
    post = rep_p(post)
    post = rep_hr(post)
    post = rep_a(post)
    post = rep_h(post)
    post = rep_strong(post)
    post = del_div(post)
    post = rep_img(post)
    post = rep_pre(post)
    post = rep_code(post)
    print post
def main():
    print('Please Input Jianshu Post Code: ')
    buff = sys.stdin.readline()
    GuaScriptMarkdownParserStartUp(buff)


if __name__ == "__main__":
    sys.exit(main())