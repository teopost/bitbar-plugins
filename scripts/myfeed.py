#!/usr/bin/env python
# -*- coding: utf-8 -*-

# http://fa2png.io/

from lxml import html
import requests
import urllib
import sys
import os
import feedparser
import json

max_items = 25
inc = 0
icon = "iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAMAAAC6V+0/AAAAolBMVEUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACgESU6AAAANXRSTlMAAQMEBQYKCwwOICMrLTEzNDZKUlRXY3R3eHt8f4iPoqOlqLC0vMXHzs/T19na3Ojr9fn7/e2HK2EAAACnSURBVBgZBcGFQQMBAACxPDUo7u7ulHL7r0YCAAAAAAAvy+fTzRUAQFW/xxMAcFNVi/0BAIbZ9m3V/QgAML2qPlYBjEdg/lPvI4DvPg8nmL7W/QCoWuxh+lMHgKO3qsuBeS0mALOz6gRXdQzAxrI2mNbvCjCesVvvA7e1Cbb+uuC61tmpU/BVzczrnNV6Ao/1NzbUM0Mtwdrj1xaue8BdLwAAAAAA4B+XCBbdaR+cBQAAAABJRU5ErkJggg=="
#icon = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAATBJREFUeNqc0b1KQzEYxvFQq4i2kwiCDjo4dZIKQm+hm5tUUHDxBnQSF1cXh1IR3AqdBK+gLl5BURz82hy0Iq2lYkHqP/BGHsKxFgM/Tvvk5D3Jm7Rzro8OHtHABc7x6oYc/QSfqCH33wLBF8rIDiowj2Ws4wQvCYVuh92NH6NW7D4q8oaVpAVH2EMRk5KP4zChSG5QD/xtVDAr82voRcfJ/tXEd5SiIjpfDhMjmEETc0hbPoZVu85LXNlXCzafx5k1/GdMYAet6Gsl6Yk2tvbbLSziLjpO6MmG5L4vU7rIbysl/9vy8rFccVPyLR/uS1CXPuxGt5Ox/FTyqrMt6plDo/yCD8mLlm9K1kjZVnW07NmxGwhjyZ43ki34Att4QhcHuJYXHuT3tD2fJct8CzAAqHZ3QQFiFvsAAAAASUVORK5CYII="
bitbar_path = os.path.dirname(os.path.abspath(__file__))
script_name = os.path.basename(os.path.abspath(__file__))
readed_items = 'gray'
unreaded_items = 'black'


def save_as_readed(item):
    with open(bitbar_path + "/.pascal.dat", "a+") as file:
        for line in file:
            if item in line:
                break
        else: # not found, we are at the eof
            file.write(item + '\n')


def count_readed_items():
    if not os.path.isfile(bitbar_path + "/.pascal.dat"):
        with open(bitbar_path + "/.pascal.dat", "a+") as dfile:
            dfile.write('')
    articles = []
    with open(bitbar_path + "/.pascal.dat", "r") as dfile:
        for line in dfile:
            articles.append(line)
    return articles


def compose_menu_item_string(item_title, value, color):
    python_path = os.popen('which python').readlines()[0].rstrip('\n')
    row = '-- %s | length=65 terminal=false refresh=true color=%s bash=%s param1=%s/%s param2=%s param3=%s' % (item_title, color, python_path, bitbar_path, script_name, 'mark_single_item_as_read', value)
    return row.encode('utf-8')

# Dato l'url di un feed, deve restituire una lista di stringhe
def getFeedData(rss_url):
    feed = feedparser.parse(rss_url['url'])

    headlines = []
    headlines.append(rss_url['title'])
    for newsitem in feed['items'][:max_items]:
        headlines.append(compose_menu_item_string(newsitem['title'], newsitem['link'], rss_url['title']))
    return headlines


def getWebData(web_url):
    page = requests.get(web_url['url'])
    response = html.fromstring(page.content)
    inc=0
    file_to_save = []
    file_to_save.append(web_url['title'])
    for rows in response.xpath('//*[@id="main"]/div[3]/table/tr/td/a')[:max_items]:
        title = rows.xpath('text()')[0]
        url = rows.xpath('@href')[0].encode('utf-8')
        url = urllib.quote(url, safe=':/')
        row_data = compose_menu_item_string(title, url, readed_items)

        if url + '\n' not in count_readed_items():
            inc += 1
            file_to_save.append(row_data.replace('=' + readed_items, '=' + unreaded_items))
        else:
            file_to_save.append(row_data)
    return file_to_save


if __name__ == "__main__":
    # script action http://www.example.com
    if len(sys.argv) == 3:
        if sys.argv[1] == 'mark_single_item_as_read':
            save_as_readed(sys.argv[2])
            os.system('open ' + sys.argv[2])
            exit(0)
        if sys.argv[1] == 'mark_all_items_as_read': # not implemented!!!
            save_as_readed(sys.argv[2])
            os.system('open ' + sys.argv[2])
            exit(0)

    jsonString = '''
    [
        {
            "title": "ITT Pascal",
            "url": "http://www.itis-cesena.it/joomla/index.php?option=com_content&view=article&id=65&Itemid=160",
            "type": "web"
        },
        {
            "title": "Liceo artistico Serpieri",
            "url": "http://www.liceoserpieri.it/feed",
            "type": "feed"
        },
        {
            "title": "Corsaro nero",
            "url": "http://ilcorsaronero.info/rss",
            "type": "feed"
        },
        {
            "title": "Yahoo",
            "url": "http://news.yahoo.com/rss/",
            "type": "feed"
        }
    ]
    '''

    jsonObject = json.loads(jsonString)

    menu_items = []
    for news in jsonObject:
        if news['type'] == 'separator':
            menu_items += ['---']
        if news['type'] == 'feed':
            menu_items += getFeedData(news)
        if news['type'] == 'web':
            menu_items += getWebData(news)

    # Creating bitbar menu
    print '%s| size = 10 templateImage=%s' % (str(inc) if inc > 0 else '', icon)

    print '---'
    print "Universal Feed Reader"
    print '---'

    for item in menu_items:
        print item

    print '---'
    # print compose_item_row('Mark all as read', 'mark_all_items_as_read', file_to_save)
    print 'Refresh| refresh=true'
    print '---'
    print 'Edit script...| terminal=false bash=/usr/local/bin/atom param1=' + bitbar_path + '/' + script_name
