from data import TOKEN, URL
from bs4 import BeautifulSoup

class Data:
    COOKIES = 0
    QUERY = 1
    FORM = 2
    FILES = 3
    HEADERS = 4


def get_action_and_url(response):
    html = BeautifulSoup(response, 'html.parser')
    url = ""
    action = ""
    if "GET" in response:
        action = "GET"
        url = html.find("code").text
    if "ссылке" in response:
        action = "GET"
        url = html.find("a", href=True)["href"]
    if "POST" in response:
        action = "POST"
        url = html.find("code").text
    if "Загрузите файлы" in response:
        action = "POST"
        url = html.find("code").text

    return action, url

def get_request_data(response):
    cookies = ""
    query = {}
    form = {}
    files = {}
    headers = {}

    html = BeautifulSoup(response, 'html.parser')
    
    priority = {
        response.find("cookie"): Data.COOKIES,
        response.find("параметры запроса"): Data.QUERY,
        response.find("данные формы"): Data.FORM,
        response.find("Загрузите файлы"): Data.FILES,
        response.find("заголовки"): Data.HEADERS,
    }

    data = [i for j, i in sorted(priority.items()) if j != -1]
    tables = html.find_all("table")

    for index in range(len(data)):
        table_dict = parse_table(tables[index])
        
        if data[index] == Data.COOKIES:
            cookie_parts = [f"{k}={v}" for k, v in table_dict.items()]
            cookies = ";".join(cookie_parts)
        elif data[index] == Data.QUERY:
            query = table_dict
        elif data[index] == Data.FORM:
            form = table_dict
        elif data[index] == Data.FILES:
            for k, v in table_dict.items():
                files[k] = v.encode("utf-8")
        elif data[index] == Data.HEADERS:
            headers = table_dict

    action, url = get_action_and_url(response)

    if cookies:
        headers["Cookie"] = f"user={TOKEN};{cookies}"
    else:
        headers["Cookie"] = f"user={TOKEN}"

    return {
        "action": action,
        "url": url,
        "query": query,
        "form": form,
        "files": files,
        "headers": headers,
    }
    


def parse_table(table):
    result = {}
    values = [tag.text for tag in table.find_all("code")]
    
    for i in range(0, len(values), 2):
        result[values[i]] = values[i + 1]
    return result