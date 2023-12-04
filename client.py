import socket

HOST = "192.168.1.6";
SERVER_PORT = 55000;
FORMAT = "utf8";

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
print("CLIENT SIDE");

try:
    client.connect((HOST, SERVER_PORT));
    print("CONNECT COMPLETE");
    print("Client address:", client.getsockname());

    msg = None;
    while (msg != "q"):
        msg = input("Client: ");
        client.sendall(msg.encode(FORMAT));
        msg = client.recv(1024).decode();
        print("Server:", msg);
except:
    print("Error");


print("End");
client.close();

input()