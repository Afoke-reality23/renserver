# import socket
# import json
# import os

# server=socket.socket()
# ip="0.0.0.0"
# port=int(os.getenv("PORT",1998))
# server.bind((ip,port))
# server.listen()
# print("server is listening for connection")
# cors_headers=(
#         "HTTP/1.1 200 OK\r\n"
#         "Access-Control-Allow-Origin:*\r\n"
#         "Access-Control-Allow-Headers:Content-Type\r\n"
#         "Access-Control-Allow-Methods:GET,POST,OPTIONS\r\n"
#         "Content-Type:application/json\r\n"
#         "\r\n"
#         )
# print('i am here now 1')
# preflight_headers=(
#        "HTTP/1.1 204 No Content\r\n"                              
#        "Access-Control-Allow-Origin:*\r\n"
#        "Access-Control-Allow-Methods:GET,POST,OPTIONS\r\n"
#        "Access-Control-Allow-Headers:Content-Type\r\n"
#        "Content-Type:application/json\r\n"
#        "\r\n"
#        )

# print('i am here now 2')

# def handle_client():
#     print('i am here now 3')
#     while True:
#         conn,addr=server.accept()
#         print('i am here now 4')
#         data=conn.recv(1024).decode()
#         print('i am here now 5')
#         # print(data)
#         if data.startswith("OPTIONS"):
#             conn.send(preflight_headers.encode("utf-8"))
#             conn.close()
#             continue
#         print('i am here now ')
#         if "\r\n\r\n" in data:
#             print('true')
#             header,body=data.split("\r\n\r\n",1)
#             print(f"body message==>{body}")
#         msg='yes i recieved your message this is my response hope you can text got over to you'
#         rsp=json.dumps(msg)
#         full_msg=cors_headers + rsp
#         conn.send(full_msg.encode('utf-8'))
#         conn.close()


# handle_client()



import socket
import json
import os
import threading

server = socket.socket()
ip = "0.0.0.0"
port = int(os.getenv("PORT", 1998))
server.bind((ip, port))
server.listen()
print("Server is listening for connections")

cors_headers = (
    "HTTP/1.1 200 OK\r\n"
    "Access-Control-Allow-Origin: *\r\n"
    "Access-Control-Allow-Headers: Content-Type\r\n"
    "Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n"
    "Content-Type: application/json\r\n"
    "\r\n"
)

preflight_headers = (
    "HTTP/1.1 204 No Content\r\n"
    "Access-Control-Allow-Origin: *\r\n"
    "Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n"
    "Access-Control-Allow-Headers: Content-Type\r\n"
    "Content-Type: application/json\r\n"
    "\r\n"
)


def handle_client(conn, addr):
    try:
        data = conn.recv(1024).decode()
        if not data:
            conn.close()
            return

        if data.startswith("OPTIONS"):
            conn.send(preflight_headers.encode("utf-8"))
            conn.close()
            return

        if "\r\n\r\n" in data:
            _, body = data.split("\r\n\r\n", 1)
            print(f"Body message ==> {body}")

        msg = "yes, I received your message. This is my response."
        rsp = json.dumps(msg)
        full_msg = cors_headers + rsp
        conn.send(full_msg.encode("utf-8"))

    except Exception as e:
        print(f"Error handling client: {e}")

    finally:
        conn.close()


while True:
    conn, addr = server.accept()
    threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
