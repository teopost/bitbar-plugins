#!/usr/bin/env python
# -*- coding: utf-8 -*-


# http://fa2png.io/

from lxml import html
import requests
import urllib
import sys
import os

news_title = "News - ITT Pascal Cesena"
max_items = 10
icon = "iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAMAAAC6V+0/AAAAolBMVEUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACgESU6AAAANXRSTlMAAQMEBQYKCwwOICMrLTEzNDZKUlRXY3R3eHt8f4iPoqOlqLC0vMXHzs/T19na3Ojr9fn7/e2HK2EAAACnSURBVBgZBcGFQQMBAACxPDUo7u7ulHL7r0YCAAAAAAAvy+fTzRUAQFW/xxMAcFNVi/0BAIbZ9m3V/QgAML2qPlYBjEdg/lPvI4DvPg8nmL7W/QCoWuxh+lMHgKO3qsuBeS0mALOz6gRXdQzAxrI2mNbvCjCesVvvA7e1Cbb+uuC61tmpU/BVzczrnNV6Ao/1NzbUM0Mtwdrj1xaue8BdLwAAAAAA4B+XCBbdaR+cBQAAAABJRU5ErkJggg=="

bitbar_path = os.path.dirname(os.path.abspath(__file__))
script_name = os.path.basename(os.path.abspath(__file__))


def save_as_readed(item):
    with open(bitbar_path + "/.pascal.dat", "a+") as file:
        for line in file:
            if item in line:
                break
        else: # not found, we are at the eof
            file.write(item + '\n')


def read_readed_items():
    if not os.path.isfile(bitbar_path + "/.pascal.dat"):
        with open(bitbar_path + "/.pascal.dat", "a+") as dfile:
            dfile.write('')
    articles = []
    with open(bitbar_path + "/.pascal.dat", "r") as dfile:
        for line in dfile:
            articles.append(line)
    return articles


def compose_item_row(item_title, action, value, color):
    python_path = os.popen('which python').readlines()[0].rstrip('\n')
    return ' %s | length=65 terminal=false refresh=true color=%s bash=%s param1=%s/%s param2=%s param3=%s' % (item_title, color, python_path, bitbar_path, script_name, action, value)


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

    # Read HTML of page
    url = 'http://www.itis-cesena.it/joomla/index.php?option=com_content&view=article&id=65&Itemid=160'

    page = requests.get(url)
    response = html.fromstring(page.content)

    file_to_save = []
    inc = 0
    for rows in response.xpath('//*[@id="main"]/div[3]/table/tr/td/a')[:max_items]:
        title = rows.xpath('text()')[0]
        url = rows.xpath('@href')[0].encode('utf-8')
        url = urllib.quote(url, safe=':/')
        row_data = compose_item_row(title, 'mark_single_item_as_read', url, 'black').encode('utf-8')

        if url + '\n' not in read_readed_items():
            inc += 1
            file_to_save.append('  ' + row_data.replace('=black', '=red'))
        else:
            file_to_save.append('  ' + row_data)

        #if url + '\n' in read_readed_items():
            #file_to_save.append('  ' + row_data)
        #else:
        #    inc = inc + 1
        #    file_to_save.append('* ' + row_data)

    # Creating bitbar menu
    print '%s| size = 10 templateImage=%s' % (str(inc) if inc > 0 else '', icon)

    print '---'
    print news_title
    print '---'

    for item in file_to_save:
        print item

    print '---'
    # print compose_item_row('Mark all as read', 'mark_all_items_as_read', file_to_save)
    print 'Refresh| refresh=true'
    print '---'
    print 'Edit script...| terminal=false bash=/usr/local/bin/atom param1=' + bitbar_path + '/' + script_name
