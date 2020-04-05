# coding:utf-8

import datetime
import codecs
import requests
import os
import time
from pyquery import PyQuery as pq
year = datetime.date.today().strftime('%Y')

def git_add_commit_push(date, filename):
    # year = datetime.date.today().strftime('%Y')
    cmd_git_add = 'git add {year}/{filename}'.format(year=year,filename=filename)
    cmd_git_commit = 'git commit -m "{date}"'.format(date=date)
    cmd_git_push = 'git push -u origin master'

    os.system(cmd_git_add)
    os.system(cmd_git_commit)
    os.system(cmd_git_push)


def createMarkdown(date, filename):
    # year = datetime.date.today().strftime('%Y')
    filepath = year + os.sep + filename
    with open(filepath, 'w') as f:
        f.write("## " + date + "\n")


def scrape(language, filename):

    HEADERS = {
        'User-Agent'		: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Accept'			: 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding'	: 'gzip,deflate,sdch',
        'Accept-Language'	: 'zh-CN,zh;q=0.8'
    }

    url = 'https://github.com/trending/{language}'.format(language=language)
    r = requests.get(url, headers=HEADERS)
    assert r.status_code == 200

    # print(r.encoding)

    d = pq(r.content)
    items = d('div.Box article.Box-row')

    print(len(items))

    # codecs to solve the problem utf-8 codec like chinese
    # year = datetime.date.today().strftime('%Y')
    filepath = year + os.sep + filename
    with codecs.open(filepath, "a", "utf-8") as f:
        f.write('\n#### {language}\n'.format(language=language))

        for item in items:
            i = pq(item)
            title = i(".lh-condensed a").text()
            owner = i(".lh-condensed span.text-normal").text()
            description = i("p.col-9").text()
            url = i(".lh-condensed a").attr("href")
            url = "https://github.com" + url
            # ownerImg = i("p.repo-list-meta a img").attr("src")
            # print(ownerImg)
            f.write(u"* [{title}]({url}):{owner}!{description}\n".format(title=title, url=url, description=description,owner=owner))


def job():

    strdate = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = '{date}.md'.format(date=strdate)

    # create markdown file
    # filepath = '2020'+os.sep +filename
    createMarkdown(strdate, filename)

    # write markdown
    scrape('python', filename)
    scrape('swift', filename)
    scrape('javascript', filename)
    scrape('go', filename)

    # git add commit push
    git_add_commit_push(strdate, filename)


if __name__ == '__main__':
    while True:
        job()
        time.sleep(24 * 60 * 60)
