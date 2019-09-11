from datetime import datetime, timezone
from urllib.request import urlopen
from json import loads

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

if __name__ == '__main__':
    print(get_file_modification_dtaware("turulomio","xulpymoney","products.xlsx"))
