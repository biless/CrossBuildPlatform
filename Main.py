import json
import os
import platform
import re
import subprocess
import sys
import urllib
import urllib2
import zipfile

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


def process(count, block_size, total_size):
    percent = count * block_size * 100 / float(total_size)
    sys.stdout.write("\r%f%%" % percent + ' complete')
    sys.stdout.flush()


def download_file(file_url, file_name, file_directory=os.getcwd()):
    sys.stdout.write('\rStart Download <' + file_name + '>...\n')
    local = os.path.join(file_directory, file_name)
    urllib.urlretrieve(file_url, local, reporthook=process)
    sys.stdout.write("\rDownload complete, saved as %s" % file_name + '\n\n')
    sys.stdout.flush()
    return file_directory, local


def un_zip(zip_path, ext_path):
    r = zipfile.is_zipfile(zip_path)
    first_dic = False
    filename = ""
    if r:
        fz = zipfile.ZipFile(zip_path, 'r')
        for name in fz.namelist():
            if not first_dic:
                filename = name
                first_dic = True
            fz.extract(name, ext_path)
    else:
        print('This file is not zip file')
        return ""
    print filename + 'zip finish'
    return ext_path + filename


def shell_exec(cmd):
    print "exec " + cmd
    child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    info = child.stdout.read()
    err = child.stderr.read()
    print "message:", info, err
    return info, err

print os.environ["PATH"]


def set_environ(file_path):
    os.chdir(file_path)
    os.environ["GOPATH"] = file_path
    print os.getcwd()
    return


def get_file_path(owner, repo):
    ves, zip_url = get_last_release("https://api.github.com/repos/" + owner + "/" + repo + "/releases/latest")
    path, zip_path = download_file(zip_url, ves + ".zip")
    file_path = un_zip(zip_path, path + "/")
    return file_path


def go_build(file_path):
    shell_info, err_msg = shell_exec("go build -o " + out_file_name + " main.go")
    if err_msg != "":
        packs = re.findall("cannot find package \"(.*)\"", err_msg)
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
    return


def get_go_version():
    html = urllib.urlopen("http://www.golangtc.com/download").read()
    versions = re.findall("<a class=\"accordion-toggle\".*?>[\r\n \t]*([\d.]*?)[\r\n \t]*</a>", html)
    return versions[0]


def get_go_compress_name(go_version):
    bit = "386"
    if machine == "AMD64" or machine == "x86_64":
        bit = "amd64"
    lower_system_name = system_name.lower()
    zip_name = "go" + go_version + "." + lower_system_name + "-" + bit
    if system_name == "Windows":
        zip_name += ".zip"
    else:
        zip_name += ".tar.gz"
    return zip_name

version = get_go_version()
print version
print get_go_compress_name(version)

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

print "hello world"
# downLoad_last_release(zip_name,"http://www.golangtc.com/static/go/" + ban[0] + "/" + zip_name)

start("jacoblai", "Coolpy5Sub", True)

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
