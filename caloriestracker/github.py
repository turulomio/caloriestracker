## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README


from datetime import datetime, timezone
from urllib.request import urlopen
from json import loads
from os import system, path, chdir, getcwd

## Get Github file modification datetime
## https://api.github.com/repos/turulomio/xulpymoney/commits?path=products.xlsx
## @return datetime or None if can't find it
def get_file_modification_dtaware(user,project,path):
    try:
        url="https://api.github.com/repos/{}/{}/commits?path={}".format(user,project,path)
        print(url)
        bytes_j = urlopen(url).read()
        j=loads(bytes_j.decode('UTF-8'))
        dtnaive= datetime.strptime(j[0]['commit']['author']['date'], "%Y-%m-%dT%H:%M:%SZ")
        return dtnaive.replace(tzinfo=timezone.utc)
    except:
        None

## Downloads file to a destiny directory
def download_from_github(user,repository,path_filename, destiny_directory):
    destiny_path='{}/{}'.format(destiny_directory,path.basename(path_filename))
    download_from_github_to_path(user, repository, path_filename, destiny_path)

## Downloads file to a new file path
def download_from_github_to_path(user,repository,path_filename, destiny_path):
    response = urlopen("https://raw.githubusercontent.com/{}/{}/master/{}".format(user,repository, path_filename), timeout = 5)
    content = response.read()
    f = open(destiny_path, 'wb' )
    f.write( content )
    f.close()
    print("Updating {} from https://github.com/turulomio/reusingcode/{}".format(destiny_path,path_filename))


if __name__ == '__main__':
    print(get_file_modification_dtaware("turulomio","xulpymoney","products.xlsx"))
    download_from_github("turulomio", "xulpymoney", "products.xlsx", "./")
    download_from_github_to_path("turulomio", "xulpymoney", "products.xlsx", "productas.xlsx")
