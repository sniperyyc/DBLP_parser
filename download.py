import requests
import re
import os
import time

session = requests.Session()

headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
           "Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1",
           "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:80.0) Gecko/20100101 Firefox/80.0",
           "Referer": "https://dblp.org/search?q=NDSS", "Connection": "close",
           "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
           "Accept-Encoding": "gzip, deflate"}
cookies = {"dblp-search-mode": "c", "dblp-dismiss-new-feature-2019-08-19": "3"}

lib = {
    # "NDSS": "ndss",
    # "CCS": "ccs",
    # "S&P": "sp",
    # "Usenix_Security": "uss",
    # "DSN": "dsn",
    # "Raid": "raid",
    "IMC": "imc",
    "SIGCOMM": "sigcomm",
    "NSDI": "nsdi"
}


def get_all_bibtex(url):
    bibtexs = []
    res = session.get(url, headers=headers, cookies=cookies)
    data = res.content.decode('utf-8') 
    assert res.status_code == 200
    bibtex_urls = re.compile(r'https://dblp\.org/rec/conf/[a-zA-Z0-9]{1,10}/[a-zA-Z0-9]{1,30}\.html\?view=bibtex').findall(data)
    # print(bibtex_urls)     # print(len(bibtex_urls))     
    bibtex_urls = list(set(bibtex_urls))
    for l in bibtex_urls:
        bibtex = get_one_bibtex(l)
        bibtexs.append(bibtex)
        print("[+] get one succ! {}".format(len(bibtexs)))
        time.sleep(0.1)
    bibtexs = list(set(bibtexs))
    return bibtexs


def get_one_bibtex(url):
    res = session.get(url, headers=headers, cookies=cookies)
    data = res.content.decode('utf-8')
    assert res.status_code == 200
    try:
        bibtex = re.compile(r'@[in]*proceedings{.*}', re.S).findall(data)[0]
        print(bibtex)         
        return bibtex
    except Exception as e:
        print(e)
        print(data)
    return '{}:error!'.format(url)

def check_exist(output):
    file_path = 'bibtex/{}'.format(output)
    if os.path.exists(file_path):
        return True
    return False

def main():
    # year = 2020     # key = 'NDSS'     # name = lib[key]     
    year_start = 2005
    year_end = 2023
    for year in range(year_start, year_end):
        for key in lib:
            name = lib[key]
            output = "{key}_{year}.bibtex".format(key=key, year=year)
            if check_exist(output):
                print("[-] {} {} bibtex exists! Continue...".format(key, year))
                # continue             
                print("[+] Try to get {} {} !".format(key, year))
            url = "https://dblp.org/db/conf/{name}/{name}{year}.html".format(name=name, year=year)
            results = get_all_bibtex(url)
            tmp = '\n'.join(results)
            print("[+] Get all bibtex: {} {} Succ!".format(key, year))
            with open('bibtex/{}'.format(output), 'w') as f:
                f.write(tmp)


if __name__ == '__main__':
    main()