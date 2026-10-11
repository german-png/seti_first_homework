import socket

def send_socket_request(s: socket, method: str = "GET", path: str = "/", 
                       headers: list = None, body: list = None, 
                       host: str = "hw1.alexbers.com", timeout: int = 10) -> str:
    if headers is None:
        header = []
    if body is None:
        body = []

    body_string = "\r\n".join(body)
    body_length_bytes = len(body_string.encode("utf-8"))

    request = f"{method} {path} HTTP/1.1\r\n"

    required_headers = [
        f"Host: {host}",
        f"Content-Length: {body_length_bytes}",
        "Connection: keep-alive",
    ]

    final_headers = required_headers + headers
    headers_string = "\r\n".join(final_headers)

    if body:
        full_request = f"{request}{headers_string}\r\n\r\n{body_string}\r\n\r\n"
    else:
        full_request = f"{request}{headers_string}\r\n\r\n"

    decode_request = full_request.encode("utf-8")

    # print("-----REQUEST------------------------------")
    # print(decode_request)
    # print("------------------------------------------")
    # for i in decode_request.split(b"\r\n"):
    #     print(i)
 
    s.settimeout(timeout)
    s.sendall(decode_request)

    response = b""
    while b"\r\n\r\n" not in response:
        response += s.recv(1024)
        # print(response)

    resp_headers, resp_body = response.split(b"\r\n\r\n", 1)

    response_content_length = 0
    for i in resp_headers.split(b"\r\n"):
        if b"Content-Length" in i:
            response_content_length = int(i.split(b" ")[1])
            break
    # print(f"responce content length: {response_content_length}")
    # print("------------------------------------------")

    while len(resp_body) < response_content_length:
        resp_body += s.recv(1024)

    return (resp_headers + b"\r\n\r\n" + resp_body).decode("utf-8", errors="ignore")