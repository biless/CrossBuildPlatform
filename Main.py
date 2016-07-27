import commands
import json
import os
import re
import urllib
import urllib2

import subprocess
import zipfile


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

# ves, zipUrl = GetLastRelease("https://api.github.com/repos/jacoblai/Coolpy5Sub/releases/latest")
# print ves, zipUrl
# zippath = DownLoadLastRelease(ves, zipUrl)
# print zippath

zippath = "F:/5.0.1.0.zip"

os.chdir("F:/")
r = zipfile.is_zipfile(zippath)
first_dic = False
filename = ""
if r:
    fz = zipfile.ZipFile(zippath, 'r')
    for file in fz.namelist():
        if not first_dic:
            filename = file
            first_dic = True
        fz.extract(file, "/")
else:
    print('This file is not zip file')

print 'zip finish'

print filename


# for parent,dirnames,_ in os.walk("F:/"):
#     for dirname in dirnames:
#         print "parent is:" + parent
#         print "dirname is" + dirname

os.environ["GOPATH"]="F:/"+filename
#print os.environ["GOPATH"]
os.chdir("F:/"+filename)
#print os.getcwd()
#os.system("go build main.go")
#cmd = os.popen("go env")
#ss = cmd.read().decode('GB2312')
#print ss



#for i in cmd:
    #print i
#ss = cmd.readline().decode('GB2312')
child = subprocess.Popen('go build main.go',shell=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
returncode = child.poll()
info = child.stdout.read().decode('gb2312')
print "message:",info
res = re.findall("cannot find package \"(.*)\"", info)
print res


for pack in res:
    child = subprocess.Popen('go get ' + pack,shell=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    returncode = child.poll()
    info = child.stdout.read().decode('gb2312')


#print (a)
#res = re.findall("\w", cmd)
#print res
#cmd = os.system("go build -o win32.exe main.go")
#print cmd
