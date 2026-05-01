import requests, time, sys
FILES = [".env",".git/config","robots.txt"]
XSS_P = ["<script>alert(1)</script>"]
SQL_P = ["' OR 1=1--", "' OR '1'='1"]
SQL_ERROR = ['mysql', 'sqlite', 'syntax error', 'ORA-']
def scan_files(url):
    arry = []
    for file in FILES:
        try:
            r = requests.get(f"{url}/{file}", timeout = 5)
            if r.status_code == 200 and len(r.text) > 50:
                arry.append(f"{url}/{file}")
                print(f"[+] Найден файл {url}/{file}")
        except Exception:
            pass
        time.sleep(0.5)
    return arry
def scan_xss(url):
    arry = []
    for xss in XSS_P:
        try:
            r = requests.get(f"{url}?q={xss}", timeout = 5)
            if xss in r.text:
                arry.append(f"{url}?q={xss}")
                print(f"[!] Возможный XSS: {url}?q={xss}")
        except Exception:
            pass
        time.sleep(0.5)
    return arry
def scan_sql(url):
    arry = []
    for sql in SQL_P:
        try:
            r = requests.get(f"{url}?id={sql}", timeout = 5)
            r_text = r.text.lower()
            sql_d = False
            for SQL_ERR in SQL_ERROR:
                if SQL_ERR in r_text:
                    sql_d = True
                    break
            if sql_d:
                arry.append(f"{url}?id={sql}")
                print(f"[!] Возможный SQLi: {url}?id={sql}")
        except Exception:
            pass
        time.sleep(0.5)
    return arry
if __name__ == '__main__':
    target = str(input("URL: "))
    if not target.startswith("http"):
        print("URL должен начинатся с http или https")
        sys.exit()
    print(f"Проверка {target}")
    files = scan_files(target)
    xss = scan_xss(target)
    sql = scan_sql(target)
    print("\n=== ИТОГИ ===")
    print(f"Открытые файлы: {len(files)}")
    print(f"Возможный XSS: {len(xss)}")
    print(f"Возможный SQLi: {len(sql)}")
    
