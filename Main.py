import json
import os
import urllib
import urllib2


def GetLastRelease(httpaddress):
    httpstream = urllib2.urlopen(httpaddress)
    res = httpstream.read()
    res_json = json.loads(res)
    return res_json["tag_name"], res_json["zipball_url"]


def DownLoadLastRelease(version, zipurl):
    path = r'F:'
    file_name = version + r'.zip'
    dest_dir = os.path.join(path, file_name)
    #urllib.urlretrieve(zipurl, path + "/" + version + ".zip")
    f = urllib2.urlopen(zipurl)
    data = f.read()
    with open(path+"/"+version+".zip", "wb") as code:
        code.write(data)
    return path+"/"+version+".zip"


ves, zipUrl = GetLastRelease("https://api.github.com/repos/coolpy/coolpyV/releases/latest")
print ves, zipUrl
print DownLoadLastRelease(ves, zipUrl)
