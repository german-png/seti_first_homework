from bs4 import BeautifulSoup
from parser_http import for_socket_parser_adapter, get_request_data
from send_request import send_socket_request
from data import TOKEN, URL
from urllib.parse import urlparse
import socket 

def main():
    host = "hw1.alexbers.com"
    
    s = socket.socket()
    s.connect((host, 80))
    
    response = send_socket_request(
        s,
        method="GET",
        path="/",
        headers=[f"Cookie: user={TOKEN}"],
        body=[]
    )

    while True:
        for i in response.split("\n"):
            if "Шаг" in i:
                print(i.strip())

        parsed_data = get_request_data(response)
        request_data = for_socket_parser_adapter(parsed_data)

        response = send_socket_request(
            s,
            method=request_data["method"],
            path=request_data["path"],
            headers=request_data["headers"],
            body=request_data["body"]
        )

        if "Поздравляем" in response:
            break

    print(response)
    

if __name__ == "__main__":
    main()