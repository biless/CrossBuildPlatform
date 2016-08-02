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
go_path = "go"


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
    info = child.stdout.read().decode("gb2312")
    err = child.stderr.read().decode("gb2312")
    print "exec ok"
    # print "info message:\n", info
    # print "error message:\n", err
    return info, err


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


def go_build(file_path, out_file_path):
    shell_info, err_msg = shell_exec(go_path + " build -o " + out_file_path + " main.go")
    if err_msg != "":
        packs = re.findall("cannot find package \"(.*)\"", err_msg)
        for pack in packs:
            shell_exec(go_path + " get " + pack)
        shell_exec(go_path + " build -o " + out_file_name + " main.go")
    print "build success " + file_path + out_file_name
    return file_path


def set_os_arch(owner, repo, os_name, arch):
    os.environ["GOOS"] = os_name
    os.environ["GOARCH"] = arch
    out_file_path = root_path + "/bin/" + os_name + "/" + owner + "_" + repo + "_" + os_name + "_" + arch
    if os_name == "windows":
        out_file_path += ".exe"
    return out_file_path


def cross_build(owner, repo, repo_file):
    out_file_path = set_os_arch(owner, repo, "windows", "amd64")
    go_build(repo_file, out_file_path)
    return


def start(owner, repo, is_rice):
    rice_path = ""
    if is_rice:
        set_environ(root_path)
        shell_exec(go_path + " get github.com/GeertJohan/go.rice/rice")
        rice_path = root_path + "/bin/" + rice_name
    os.chdir(root_path)
    repo_file = get_file_path(owner, repo)
    if is_rice:
        os.chdir(repo_file)
        shell_exec(rice_path + " embed-go")
    os.chdir(repo_file)
    set_environ(repo_file)
    cross_build(owner, repo, repo_file)
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


def get_go_compress():
    go_version = get_go_version()
    print "go version is ", go_version
    go_compress_name = get_go_compress_name(go_version)
    print "go compress name is ", go_compress_name
    file_directory, file_path = download_file("http://www.golangtc.com/static/go/" + go_version + "/" + go_compress_name
                                              , go_compress_name)
    return file_directory, file_path


def get_go():
    # file_directory, file_path = get_go_compress()
    file_directory = "F:\CrossBuildPlatform/"
    file_path = "F:\CrossBuildPlatform\go1.6.3.windows-amd64.zip"
    print file_directory, " File Path:", file_path
    ext_path = un_zip(file_path, file_directory)
    print ext_path
    go_path_temp = ext_path + "bin/go"
    print os.environ["PATH"]
    print shell_exec(go_path_temp + " env")
    return go_path_temp


# go_path = get_go()

print "hello world"

start("jacoblai", "Coolpy5Sub", True)