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
    path = r'/Users/bileskou/Downloads'
    file_name = version + r'.zip'
    dest_dir = os.path.join(path, file_name)
    urllib.urlretrieve(zipurl, path + "/" + version + ".zip")
    return "file download finish"


ves, zipUrl = GetLastRelease("https://api.github.com/repos/coolpy/coolpyV/releases/latest")
print ves, zipUrl
print DownLoadLastRelease(ves, zipUrl)

val = os.system("unzip " + r'/Users/bileskou/Downloads/' + ves + ".zip")
print val

val = os.system("ls |grep \"coolpy\"")
print val
