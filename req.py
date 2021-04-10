import requests
import config


def login(phone, passw):
    s = requests.session()
    try:
        r = s.post('https://cst-russia.ru/my/login.php', data={'phone': phone, 'pass': passw}, timeout=30)
        print(s.cookies['PHPSESSID'])
        return s
    except requests.exceptions.RequestException as e:
        print(e)
        return 0
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
        return 0
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
        return 0
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
        return 0


def smsStat(date_from, date_to, child_id):
    s = login(config.cst_phone, config.cst_pass)
    if s != 0:
        try:
            r_stat = s.post('https://cst-russia.ru/my/index.php?mod=smsstat',
                            data={'date_from': date_from, 'date_to': date_to, 'childrenids[]': child_id}, timeout=30)
            resp_body = r_stat.text
            return resp_body
        except requests.exceptions.RequestException as e:
            print(e)
            return 0
