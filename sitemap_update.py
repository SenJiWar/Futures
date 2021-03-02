
import requests
import sys
import io
import argparse

def download():

    url1 = "http://a145456.hostedsitemap.com/4054282/sitemap.xml"
    req = requests.get(url1)

    f = open("/root/QiHuo/statics/sitemap.xml", 'w')
    f.write(req.text)
    f.close()

    url2 = "http://a145456.hostedsitemap.com/4054283/sitemap.xml"

    req = requests.get(url2)

    f = open("/root/FanYong/statics/sitemap.xml", 'w')
    f.write(req.text)
    f.close()


def build_sitemap():

    data = {
        'email':'zhcoder2016@gmail.com',
        'injs':'true',
        'op':'login',
        'password_md5':'ab6cadc2896371622337a1976d809064',
    }
    headers = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
    login_url = 'https://pro-sitemaps.com/index.php'

    session = requests.Session()

    resp = session.post(login_url, data, verify=False)

    ref_url = "https://pro-sitemaps.com/site/4054282/refresh/?submit=true"
    refResp = session.post(ref_url,{"confirm":"true"},verify=False)

    ref_url = "https://pro-sitemaps.com/site/4054283/refresh/?submit=true"
    refResp = session.post(ref_url,{"confirm":"true"},verify=False)


if __name__ == "__main__":

    try:
        parser = argparse.ArgumentParser(description='SiteMap使用帮助：')

        parser.add_argument('--action', action="store", default=None, help="build or download")
        
        args = parser.parse_args()

        action = args.action

        if action is not None:
            if action == "build":
                build_sitemap()
            elif action == "download":
                download()
            else:
                print("请使用python3 main.py --h查看用法。")
        else:
            print("请使用python3 main.py --h查看用法。")

    except BaseException as er:
        print(er)
        print("请使用python3 main.py --h查看用法。")
    