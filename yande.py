#!/usr/bin/python3

import requests
import re
import random
import subprocess
import time

url_params = {'tags' : 'landscape order:random'}
yande_url = 'https://yande.re/post'
download_dir = '/home/midorikawa/图片/yande_wallpaper/'
fit_flag = 0

def is_resolution_fit(photo_resolution):
    res = re.match('(\S+) x (\S+)', photo_resolution)
    print(res.group(0))
    if int(res.group(1)) > 1600 and int(res.group(2)) > 900 and int(res.group(1)) > int(res.group(2)):
        return True
    else:
        return False

def get_photos_resolution_list(html_text):
    return re.findall('<span class="directlink-res">(\S+ x \S+)<.span', html_text, re.M|re.L)

def get_photos_url_list(html_text):
    return re.findall('href="(https\S+jpg)"', html_text, re.M|re.I)

def download_photo(url):
    r = requests.get(url)
    with open(download_dir + 'wallpaper.jpg', "wb") as code:
        code.write(r.content)

def main():
    fit_flag = 0

    time_stamp = time.localtime()
    file_name = 'wallpaper-' + '%02d%02d%02d'%(time_stamp.tm_hour, time_stamp.tm_min, time_stamp.tm_sec) + '.jpg'

    random_num = random.randint(0,39)
    
#    subprocess.call(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", "file://" + download_dir + file_name])
    page_html = requests.get(yande_url, params = url_params)

    photo_url_list = get_photos_url_list(page_html.text)
    photo_res_list = get_photos_resolution_list(page_html.text)

    while fit_flag == 0:
        random_num = random.randint(1,40)
        if is_resolution_fit(photo_res_list[random_num]):
            fit_flag = 1
            cmd = 'wget -O ' + download_dir + file_name + ' %s'%photo_url_list[random_num]
            subprocess.call(cmd, shell = True)
#            download_photo('%s'%photo_url_list[random_num])
#            subprocess.call('mv ' + download_dir + 'wallpaper.jpg ' + download_dir + time_stamp + 'wallpaper_done.jpg', shell = True)

    subprocess.call('PID=$(pgrep gnome-session) && export DBUS_SESSION_BUS_ADDRESS=$(grep -z DBUS_SESSION_BUS_ADDRESS /proc/$PID/environ|cut -d= -f2-) && gsettings set org.gnome.desktop.background picture-uri "file://' + download_dir + file_name + '"', shell = True)
    


if __name__ == '__main__':
    main()
