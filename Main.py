import json
import os
import platform
import re
import subprocess
import urllib
import urllib2
import zipfile

import sys

import time

root_path = os.getcwd()
system_name = platform.system()
machine = platform.machine()
out_file_name = system_name + "_" + machine
rice_name = "rice"
if system_name == "Windows":
    out_file_name += ".exe"
    rice_name += ".exe"


def get_last_release(http_address):
    http_stream = urllib2.urlopen(http_address)
    res = http_stream.read()
    res_json = json.loads(res)
    print res_json["tag_name"], res_json["zipball_url"]
    return res_json["tag_name"], res_json["zipball_url"]


def downLoad_last_release(version, zip_url):
    path = root_path
    file_name = version + r'.zip'
    f = urllib2.urlopen(zip_url)
    data = f.read()
    with open(path + "/" + file_name, "wb") as code:
        code.write(data)
    print path + "/" + file_name + " Finish"
    return path, path + "/" + file_name


def un_zip(zip_path, ext_path):
    r = zipfile.is_zipfile(zip_path)
    first_dic = False
    filename = ""
    if r:
        fz = zipfile.ZipFile(zip_path, 'r')
        for file in fz.namelist():
            if not first_dic:
                filename = file
                first_dic = True
            fz.extract(file, ext_path)
    else:
        print('This file is not zip file')
        return ""
    print filename + 'zip finish'
    return ext_path + filename


def shell_exec(cmd):
    print "exec " + cmd
    child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    info = child.stdout.read()
    #err = child.stderr.read()
    print "message:", info
    return info


def set_environ(file_path):
    os.chdir(file_path)
    os.environ["GOPATH"] = file_path
    # os.environ["path"] = os.environ["path"] + ";" + rice_path
    print os.getcwd()
    return


def get_file_path(owner, repo):
    ves, zip_url = get_last_release("https://api.github.com/repos/" + owner + "/" + repo + "/releases/latest")
    path, zip_path = downLoad_last_release(ves, zip_url)
    file_path = un_zip(zip_path, path + "/")
    return file_path


def go_build(file_path):
    shell_info = shell_exec("go build -o " + out_file_name + " main.go")
    if shell_info != "":
        packs = re.findall("cannot find package \"(.*)\"", shell_info)
        for pack in packs:
            shell_exec("go get " + pack)
        shell_exec("go build -o " + out_file_name + " main.go")
    print "build success " + file_path + out_file_name
    return file_path


def start(owner, repo, is_rice):
    rice_path = ""
    if is_rice:
        set_environ(root_path)
        shell_exec("go get github.com/GeertJohan/go.rice/rice")
        rice_path = root_path + "/bin/" + rice_name
    os.chdir(root_path)
    repo_file = get_file_path(owner, repo)
    if is_rice:
        os.chdir(repo_file)
        shell_exec(rice_path + " embed-go")
    os.chdir(repo_file)
    set_environ(repo_file)
    repo_path = go_build(repo_file)
    return



def view_bar(num=1, sum=100, bar_word="#"):
    rate = float(num) / float(sum)
    rate_num = int(rate * 100)
    print '\r%d%% :' %(rate_num),
    for i in range(0, num):
        os.write(1, bar_word)
    sys.stdout.flush()

# print "finish"
# for i in range(0, 100):
#     time.sleep(0.1)
#     view_bar(i, 100)
#
# print "finish"
# for i in range(0, 100):
#     time.sleep(0.1)
#     view_bar(i, 100)


r = urllib2.urlopen("http://www.golangtc.com/download")
res1 = r.read()
ban = re.findall("<a class=\"accordion-toggle\".*?>[\r\n \t]*([\d.]*?)[\r\n \t]*</a>", res1)
print ban[0]
bit = "386"
if machine == "AMD64":
    bit = "amd64"
lower_system_name = system_name.lower()
zip_name = "go"+ ban[0] +"." + lower_system_name + "-" + bit
if system_name == "Windows":
    zip_name += ".zip"
else:
    zip_name += ".tar.gz"


def report(count, blockSize, totalSize):
    percent = count * blockSize * 100 / float(totalSize)
    sys.stdout.write("\r%f%%" % percent + ' complete')
    sys.stdout.flush()

# sys.stdout.write('\rFetching ' + "haha" + '...\n')
#
# url = "http://www.golangtc.com/static/go/" + ban[0] + "/" + zip_name
#
# file_name = url.split('/')[-1]
# u = urllib2.urlopen(url)
# f = open(file_name, 'wb')
# meta = u.info()
# file_size = int(meta.getheaders("Content-Length")[0])
# print "Downloading: %s Bytes: %s" % (file_name, file_size)
#
# file_size_dl = 0
# block_sz = 8192
# while True:
#     buffer = u.read(block_sz)
#     if not buffer:
#         break
#
#     file_size_dl += len(buffer)
#     f.write(buffer)
#     status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
#     status = status + chr(8) * (len(status) + 1)
#     print status
#
# f.close()


sys.stdout.write('\rFetching ' + "haha" + '...\n')
local = os.path.join(os.getcwd(),zip_name)
urllib.urlretrieve("http://www.golangtc.com/static/go/" + ban[0] + "/" + zip_name, local, reporthook=report)
sys.stdout.write("\rDownload complete, saved as %s" % (zip_name) + '\n\n')
sys.stdout.flush()

print "hello world"
# downLoad_last_release(zip_name,"http://www.golangtc.com/static/go/" + ban[0] + "/" + zip_name)

# start("jacoblai", "Coolpy5Sub", True)

# get_last_release_zip("jacoblai", "Coolpy5Sub")

# for parent,dirnames,_ in os.walk("F:/"):
#     for dirname in dirnames:
#         print "parent is:" + parent
#         print "dirname is" + dirname

# os.environ["GOPATH"] = "F:/" + filename
# print os.environ["GOPATH"]
# os.chdir("F:/" + filename)
# print os.getcwd()

# res = re.findall("cannot find package \"(.*)\"", info)
# print res

# for pack in res:
#     child = subprocess.Popen('go get ' + pack, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#     info = child.stdout.read().decode('gb2312')
