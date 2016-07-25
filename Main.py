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
    path = r'/Users/bileskou'
    file_name = version + r'.zip'
    dest_dir = os.path.join(path, file_name)
    urllib.urlretrieve(zipurl, path + "/" + version + ".zip")
    return "ok"


ves, zipUrl = GetLastRelease("https://api.github.com/repos/coolpy/coolpyV/releases/latest")
print ves, zipUrl
print DownLoadLastRelease(ves, zipUrl)
