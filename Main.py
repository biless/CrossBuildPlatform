#!/usr/bin/python
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import urllib
import urllib2
import zipfile

root_path = os.getcwd()
root_bin_path = root_path + "/bin/"
system_name = platform.system()
machine = platform.machine()
rice_name = "rice"
if system_name == "Windows":
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
    if err != "":
        print "exec ok"
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
    return file_path, ves


def go_build(os_name, out_file_path):
    if os_name == "windows":
        out_file_path += ".exe"
    shell_info, err_msg = shell_exec(go_path + " build -ldflags=\"-s -w\" -o " + out_file_path + " main.go")
    if err_msg != "":
        packs = re.findall("cannot find package \"(.*)\"", err_msg)
        for pack in packs:
            shell_exec(go_path + " get " + pack)
        shell_exec(go_path + " build -ldflags=\"-s -w\" -o " + out_file_path + " main.go")
    print "build success " + out_file_path
    return


def set_os_arch(repo, ves, os_system):
    os.environ["GOOS"] = os_system["os_name"]
    os.environ["GOARCH"] = os_system["os_arch"]
    os.environ["GOARM"] = os_system["arm"]
    out_file_path = "%s/bin/%s/%s/" % (root_path, os_system["os_name"], os_system["os_arch"])
    out_file_name = "%s_%s_%s_%s" % (repo, os_system["os_real_name"], os_system["os_arch"], ves)
    return out_file_path, out_file_name


def zip_dir(dir_name, zip_file_name):
    full_dir_name = os.path.abspath(dir_name)
    full_zip_file_name = os.path.abspath(zip_file_name)
    print "Start to zip %s to %s ..." % (full_dir_name, full_zip_file_name)
    if not os.path.exists(full_dir_name):
        print "Dir %s is not exist, check your dir" % full_dir_name
        return
    if os.path.isdir(full_zip_file_name):
        tmp_base_name = os.path.basename(dir_name)
        full_zip_file_name = os.path.normpath(os.path.join(full_zip_file_name, tmp_base_name))
    if os.path.isfile(full_dir_name):
        print "%s is not a dir, check your dir" % full_dir_name
        return
    zip_temp = zipfile.ZipFile(full_zip_file_name, "w", zipfile.ZIP_DEFLATED)
    for root, dir_list, files in os.walk(dir_name):
        for filename in files:
            zip_temp.write(os.path.join(root, filename))
    zip_temp.close()
    print "Zip folder succeed!"


def build_zip(os_system, out_file_path, out_file_name):
    if os.path.exists(out_file_path):
        shutil.rmtree(out_file_path)
    go_build(os_system["os_name"], out_file_path + out_file_name)
    for path in os_system["copy_paths"]:
        shutil.copytree(path, out_file_path + path)
    zip_dir(out_file_path, root_bin_path + out_file_name + ".zip")
    return


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


def get_go():
    file_directory, file_path = get_go_compress()
    print file_directory, " File Path:", file_path
    ext_path = un_zip(file_path, file_directory)
    print ext_path
    go_path_temp = ext_path + "bin/go"
    print os.environ["PATH"]
    print shell_exec(go_path_temp + " env")
    return go_path_temp


def build_and_zip(repo, ves, os_system):
    out_file_path, out_file_name = set_os_arch(repo, ves, os_system)
    build_zip(os_system, out_file_path, out_file_name)


def cross_build(repo, ves, os_list):
    print ves
    for os_system in os_list:
        build_and_zip(repo=repo, ves=ves, os_system=os_system)
    return


def start(owner, repo, os_list):
    os.chdir(root_path)
    repo_file, ves = get_file_path(owner, repo)
    os.chdir(repo_file)
    set_environ(repo_file)
    cross_build(repo, ves, os_list)
    return


# go_path = get_go()
if __name__ == '__main__':
    # os_temp = [{"arm": "", "os_name": "windows", "os_real_name": "Windows", "os_arch": "amd64"},
    #            {"arm": "", "os_name": "windows", "os_real_name": "Windows", "os_arch": "386"},
    #            {"arm": "", "os_name": "linux", "os_real_name": "Linux", "os_arch": "amd64"},
    #            {"arm": "", "os_name": "linux", "os_real_name": "Linux", "os_arch": "386"},
    #            {"arm": "", "os_name": "darwin", "os_real_name": "Mac", "os_arch": "amd64"},
    #            {"arm": "8", "os_name": "linux", "os_real_name": "Arm8", "os_arch": "arm64"},
    #            {"arm": "7", "os_name": "linux", "os_real_name": "Arm7", "os_arch": "arm"},
    #            {"arm": "6", "os_name": "linux", "os_real_name": "Arm6", "os_arch": "arm"}]
    os_temp = json.load(file("config.json"))
    print os_temp
    start("jacoblai", "Coolpy5Sub", os_temp)
