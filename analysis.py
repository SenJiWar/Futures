
import re
import datetime
import requests
from user_agents import parse
from collections import OrderedDict
import json

# 常量定义
class Constants:

    def __init__(self):
        pass

    REQUEST_TIME = 'request_time'
    METHOD = 'method'
    URL = 'url'
    STATUS = 'status'
    BYTES = 'bytes'
    REFERER = 'referer'
    USER_AGENT = 'user_agent'
    CLIENT_IP = 'client_ip'

class LogAnalysis:
    # access log 是可配的，日志格式可能不一样，根据实际情况更改
    pat = (r''
           '(\d+.\d+.\d+.\d+)\s-\s-\s'  # 代理IP(可忽略)
           '\[(.+)\]\s'  # 时间
           '"(.+)\s\w+/.+"\s'  # 请求地址
           '(\d+)\s'  # 请求状态
           '(\d+)\s'  # 请求内容大小
           '"(.+)"\s'  # 来源地址
           '"(.+)"\s'  # user_agent
           '"(.+)"'  # 客户端IP
           )

    # 解析的日志数组
    logs = []

    def __init__(self, log_b):
        self.log_b = log_b

    def parse(self):
        line = self.log_b.readline()
        
        while line:
            try:
                log = self.process_line(line)
                self.logs.append(log)
            except e as Exception:
                print(e)
            finally:
                line = self.log_b.readline()

    def run(self,isDetail=False):

        self.parse()

        res1 = self.ipAnalysis(limit=20,detail=isDetail)
        res2 = self.browserAnalysis()
        res3 = self.spiderAnalysis()
        res4 = self.domadeAnalysis()

        return res1+res2+res3+res4

    def process_line(self, line):
        res = re.findall(self.pat, line)
        if not res:
            return False
        res_tuple = res[0]

        return self.early_process(res_tuple)

    def early_process(self, res_tuple):
        info = {}

        r_time = res_tuple[1].split(' ')[0]
        str_time = datetime.datetime.strptime(r_time, '%d/%b/%Y:%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        info[Constants.REQUEST_TIME] = str_time

        r_url = res_tuple[2]
        r_url_arr = r_url.split(' ')
        method = r_url_arr[0]
        url = r_url_arr[1].split('?')[0]
        info[Constants.METHOD] = method
        info[Constants.URL] = url

        info[Constants.STATUS] = res_tuple[3]
        info[Constants.BYTES] = res_tuple[4]

        info[Constants.REFERER] = res_tuple[5]
        info[Constants.USER_AGENT] = res_tuple[6]
        info[Constants.CLIENT_IP] = res_tuple[0]
        return info

    def ipAnalysis(self,limit=20,detail=False):

        res = "<br>--------------------------------IP分析--------------------------------<br><br>"

        ips = OrderedDict()

        for log in self.logs:
            try:
                ip = log[Constants.CLIENT_IP]
                ips[ip] = ips.get(ip,0)+1 
            except Exception as e:
                pass

        ips = OrderedDict(sorted(ips.items(), key=lambda t: t[1],reverse=True))

        # 获取访问次数高的IP
        index = 0
        for (key,value) in ips.items():
            if index >= limit:
                break

            index = index+1

            if (detail):
                r = requests.get("http://ip.taobao.com/service/getIpInfo.php",params={"ip":key})
                resp = json.loads(r.text)
                ad = "%s%s%s%s" %(resp['data']["country"],resp['data']["region"],resp['data']["city"],resp['data']["isp"])
                ad = ad.replace("XX","未知")
                fstr = "IP地址：%s \t 访问次数：%d" %((key+"("+ad+")").ljust(25),value)
                res = res + fstr + "<br>"
            else:
                fstr = "IP地址：%s \t 访问次数：%d" %(key.ljust(35),value)
                res = res + fstr + "<br>"

        return res

    def browserAnalysis(self):
        
        res = "<br>--------------------------------浏览器分析--------------------------------<br><br>"
        ips = OrderedDict()

        for log in self.logs:
            try:
                ug = parse(log[Constants.USER_AGENT])
                if ug.is_bot:
                    continue
                browser = ug.browser.family                
                ips[browser] = ips.get(browser,0)+1
            except Exception as e:
                pass

        ips = OrderedDict(sorted(ips.items(), key=lambda t: t[1],reverse=True))

        for (key,value) in ips.items():
            fstr = "浏览器：%s \t 访问次数:%d" %(key.ljust(35),value)
            res = res + fstr + "<br>"

        return res

    def spiderAnalysis(self):

        res = "<br>--------------------------------爬虫分析--------------------------------<br><br>"
        ips = OrderedDict()

        for log in self.logs:
            try:
                ug = parse(log[Constants.USER_AGENT])
                if ug.is_bot == False:
                    continue
                browser = ug.browser.family                
                ips[browser] = ips.get(browser,0)+1
            except Exception as e:
                pass

        ips = OrderedDict(sorted(ips.items(), key=lambda t: t[1],reverse=True))

        for (key,value) in ips.items():
            fstr = "爬虫：%s \t 访问次数:%d" %(key.ljust(35),value)
            res = res + fstr + "<br>"

        return res

    def domadeAnalysis(self):

        res = "<br>--------------------------------站点分析--------------------------------<br><br>"
        ips = OrderedDict()

        for log in self.logs:
            try:
                refer = log[Constants.REFERER] 

                if (refer.find("qhjujian") >= 0):
                    refer = "期货居间网"
                elif (refer.find("qihuofy") >= 0):
                    refer = "期货返佣网"
                else:
                    url = log[Constants.URL]
                    if (url == "/"):
                        refer = "居间网或者返佣网"
                    else:
                        continue

                ips[refer] = ips.get(refer,0)+1

            except Exception as e:
                pass

        ips = OrderedDict(sorted(ips.items(), key=lambda t: t[1],reverse=True))

        for (key,value) in ips.items():
            fstr = "站点：%s \t 访问次数:%d" %(key.ljust(35),value)
            res = res + fstr + "<br>"

        return res

if __name__ == "__main__":

    log_file = open('/Users/zhihuashen/Desktop/access.log', 'r')

    la = LogAnalysis(log_file)
    la.parse()

    res = la.run(isDetail=False)

    log_file.close()