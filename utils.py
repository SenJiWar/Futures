import datetime
import time
import base64
import hashlib
import os

def date_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

def date_base64_decode(base64str):
    if base64str.find("data:image/png;base64,") >= 0 :
        base64str = base64str.replace("data:image/png;base64,","")
        data = base64.b64decode(base64str)
        return (data,"png")
    elif base64str.find("data:image/jpeg;base64,") >= 0 :
        base64str = base64str.replace("data:image/jpeg;base64,","")
        data = base64.b64decode(base64str)
        return (data,"jpeg")
    else :
        return ("","")
        
def save_image(base64str):

    result = date_base64_decode(base64str)

    file_name = md5string(base64str)  + "." + result[1]

    file_path = "./html/resources/store_imgs/" + file_name

    file_exist = os.path.exists(file_path)

    if len(result[0]) == 0 and len(result[1]) == 0 :
        return base64str

    elif (file_exist == False) and len(result[1]) > 0 :

        f = open(file_path,'wb+')
    
        f.write(result[0])
        f.close()

        return file_path.replace("./html","")

    else:
        return file_path.replace("./html","")

def md5string(str):
    m = hashlib.md5()
    m.update(str.encode("utf-8"))
    return m.hexdigest()