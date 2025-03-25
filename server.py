import socket
import json
import os

server=socket.socket()
ip=" "
# port=1998
port=int(os.getenv("PORT",8080))
server.bind((ip,port))
print(port)
server.listen()
cors_headers=(
        "HTTP/1.1 200 OK\r\n"
        "Access-Control-Allow-Origin:*\r\n"
        "Access-Control-Allow-Headers:Content-Type\r\n"
        "Access-Control-Allow-Methods:GET,POST,OPTIONS\r\n"
        "Content-Type:application/json\r\n"
        "\r\n"
        )
preflight_headers=(
       "HTTP/1.1 204 No Content\r\n"                              
       "Access-Control-Allow-Origin:*\r\n"
       "Access-Control-Allow-Methods:GET,POST,OPTIONS\r\n"
       "Access-Control-Allow-Headers:Content-Type\r\n"
       "Content-Type:application/json\r\n"
       "\r\n"
       )

def handle_client():
    while True:
        print("server is listening for connection")
        conn,addr=server.accept()
        print('i am here now 4')
        data=conn.recv(1024).decode()
        print('i am here now 5')
        # print(data)
        if data.startswith("OPTIONS"):
            conn.send(preflight_headers.encode("utf-8"))
            conn.close()
            continue
        print('i am here now ')
        if "\r\n\r\n" in data:
            print('true')
            header,body=data.split("\r\n\r\n",1)
            print(f"body message==>{body}")
        msg='yes i recieved your message this is my response hope you can text got over to you'
        rsp=json.dumps(msg)
        full_msg=cors_headers + rsp
        conn.send(full_msg.encode('utf-8'))
        conn.close()


handle_client()

