from data import TOKEN, URL
import requests
import parser_http 
import bs4


def main():
    response = requests.get(URL, headers={"Cookie": f"user={TOKEN}"}).text

    while True:
        for i in response.split("\n"):
            if "Шаг" in i:
                print(i.strip())

        request_data = parser_http.get_request_data(response)

        response = requests.request(request_data["action"],
                                    f"{URL}{request_data['url']}",
                                    params=request_data["query"],
                                    headers=request_data["headers"],
                                    data=request_data["form"],
                                    files=request_data["files"],
                                    ).text

        if "Поздравляем" in response:
            break

    html = bs4.BeautifulSoup(response, "html.parser")
    print(html.find("code").text)


if __name__ == "__main__":
    main()