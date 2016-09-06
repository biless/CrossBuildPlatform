#!/usr/bin/python
import os
import re
import subprocess
import sys
import urllib
import platform
import zipfile

root_path = sys.path[0]
root_bin_path = root_path + "/bin/"
system_name = platform.system()
machine = platform.machine()
root_zip_path = root_bin_path
repo_version = "0.0.0.0"
go_root = ""


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


def get_go_version():
    html = urllib.urlopen("http://www.golangtc.com/download").read()
    versions = re.findall("<a class=\"accordion-toggle\".*?>[\r\n \t]*([\d.]*?)[\r\n \t]*</a>", html)
    return versions[0].encode('utf-8')


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


def get_go_compress():
    go_version = get_go_version()
    print "go version is ", go_version
    go_compress_name = get_go_compress_name(go_version)
    print "go compress name is ", go_compress_name
    file_directory, file_path = \
        download_file("http://www.golangtc.com/static/go/%s/%s" % (go_version, go_compress_name), go_compress_name)
    return file_directory, file_path


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
    info = child.stdout.read().decode("gb2312")
    err = child.stderr.read().decode("gb2312")
    if err != "":
        print "exec ok"
    return info, err


def get_go():
    file_directory, file_path = get_go_compress()
    print file_directory, " File Path:", file_path
    ext_path = un_zip(file_path, file_directory)
    print ext_path
    go_path_temp = ext_path + "bin/go"
    print os.environ["PATH"]
    print shell_exec(go_path_temp + " env")
    return go_path_temp


go_path = get_go()
print go_path