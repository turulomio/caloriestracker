## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README

from pkg_resources import resource_filename
from os import path, listdir
from logging import info, debug

## Returns the path searching in a pkg_resource model and a url. Due to PYinstaller packager doesn't supportpkg_resource
## filename is differet if we are in LInux, Windows --onefile or Windows --onedir
## @param module String
## @param url String
## @return string with the filename
def package_filename(module, url):
    for filename in [
        resource_filename(module, url), #Used in pypi and Linux
        url, #Used in pyinstaller --onedir, becaouse pkg_resources is not supported
        resource_filename(module,"../{}".format(url)), #Used in pyinstaller --onefile, becaouse pkg_resources is not supported
    ]:
        if filename!=None and path.exists(filename):
            info("Package filename '{}' found".format(filename)) #When debugging in windows, change logging for printt
            return filename
    debug("Not found {} in module {}".format(url, module))

def package_listdir(module, url):
    for dirname in [
            resource_filename(module, url), #Used in pypi and Linux
            url, #Used in pyinstaller --onedir, becaouse pkg_resources is not supported
            resource_filename(module,"../{}".format(url)), #Used in pyinstaller --onefile, becaouse pkg_resources is not supported
        ]:
        if dirname!=None and path.isdir(dirname):
            return listdir(dirname)
