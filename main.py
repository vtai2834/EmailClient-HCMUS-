# java -jar test-mail-server-1.0.jar -s 2225 -p 3335 -m ./
import socket
import os
import base64
import time
import threading

from POP3EmailClient import chucNang_2
from ReadJSON import docJson
from SMTPEmailClient import send_mail

# Prepare account email:
name, user, password, mailserver, smtp, pop3, autoload, project, important, work, spam = docJson()

list_TO = []
list_CC = []
list_BCC = []
list_File = []

list_sender = []
list_subject = []

subject = None
content = None
initializeClient = False
stop_fetching = False

FORMAT = "utf8"
SERVER_PORT_SMTP = int(smtp)
SERVER_PORT_POP3 = int(pop3)
MAX_SIZE = 1024 * 3

def fetch_emails(username, password):
    
    list_sender = []
    list_subject = []
    # Create socket called clientSocket and establish a TCP connection with mailserver
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    clientSocket.connect((mailserver, SERVER_PORT_POP3))

    # nhận thông báo từ mail server:
    response = clientSocket.recv(1024).decode()

    # gửi lệnh USER để xác thực:
    clientSocket.send(b'USER ' + user.encode(FORMAT) + b'\r\n')
    response = clientSocket.recv(1024).decode()

    # gửi lệnh pass để xác thực:
    clientSocket.send(b'PASS ' + password.encode(FORMAT) + b'\r\n')
    response = clientSocket.recv(1024).decode()

    # gửi lệnh STAT -> lấy số byte có trong mail:
    clientSocket.send('STAT\r\n'.encode(FORMAT))
    response = clientSocket.recv(1024).decode()

    # gửi lệnh LIST để lấy danh sách email
    clientSocket.send('LIST\r\n'.encode(FORMAT))
    response = clientSocket.recv(1024).decode()

    # gửi lệnh UIDL
    clientSocket.send('UIDL\r\n'.encode(FORMAT))
    response = clientSocket.recv(1024).decode()

    num_Email = response.count('.msg')
    # gửi lệnh RETR để lấy nội dung email theo số thứ tự
    for i in range(1, num_Email + 1):
        clientSocket.send(('RETR ' + str(i) + '\r\n').encode(FORMAT))
        response = b''  # Sử dụng bytes để nắm bắt dữ liệu nhận được

        while True:
            part = clientSocket.recv(1024)
            response += part
            if b'\r\n.\r\n' in part:
                break
        response = response.decode()

        # Vì sử dụng 1 lệnh response = clientSocket.recv(1024).decode() -> không thể lấy hết được dữ liệu 1 lần trên đường truyền -> dùng vòng while để lấy đủ dữ liệu -> bỏ vào file
        # Di chuyển các email được gửi từ địa chỉ ahihi@testing.com và ahuu@testing.com vào thư mục Project
        from_start_idx = response.find('From:') + len('From:')
        from_end_idx = response.find('Subject:')
        list_sender.append(response[from_start_idx : (from_end_idx - len('\r\n'))])

        subject_start_idx = response.find('Subject:') + len('Subject:')
        subject_end_idx = response.find('Content')
        list_subject.append(response[subject_start_idx : (subject_end_idx - len('\r\n'))])



        # Xu ly loc mail:
        if (project.count(list_sender[i-1]) != 0):
            cnt = len(os.listdir('Project'))
            with open('Project/Mail' + str(cnt + 1) + '.txt', "w") as attachment_file: # xb : kiểm tra nếu chưa có file đó thì tạo ra file mới tự động, còn có rồi thì kh thực hiện
                attachment_file.write(response + 'chuadoc') # tai mail ve folder luon mac dinh la chua doc
        elif (important.count(list_subject[i-1]) != 0):
            cnt = len(os.listdir('Important'))
            with open('Important/Mail' + str(cnt + 1) + '.txt', "w") as attachment_file:
                attachment_file.write(response + 'chuadoc')
        elif any(response.find(i) != -1 for i in work):
            cnt = len(os.listdir('Work'))
            with open('Work/Mail' + str(cnt + 1) + '.txt', "w") as attachment_file:
                attachment_file.write(response + 'chuadoc')
        elif (spam.count(list_subject[i-1]) != 0):
            cnt = len(os.listdir('Spam'))
            with open('Spam/Mail' + str(cnt + 1) + '.txt', "w") as attachment_file:
                attachment_file.write(response + 'chuadoc')
        else:
            cnt = len(os.listdir('Inbox'))
            with open('Inbox/Mail' + str(cnt + 1) + '.txt', "w") as attachment_file:
                attachment_file.write(response + 'chuadoc')

    # Gửi lệnh DELE để đánh dấu email đã tải
    clientSocket.send(b'DELE 1\r\n')

    # Send QUIT command and get server response.
    clientSocket.send(b'QUIT\r\n')
    recv_quit = clientSocket.recv(1024).decode()

def auto_fetch_emails():
    while not stop_fetching:
        fetch_emails(user, password)
        time.sleep(10)

# Start the auto-fetching thread
fetch_thread = threading.Thread(target=auto_fetch_emails)
fetch_thread.start()

while True:
    print("Vui lòng chọn Menu:")
    print("1. Để gửi email")
    print("2. Để xem danh sách các email đã nhận")
    print("3. Thoát\n")
    choice = input("Bạn chọn: ")
    print()

    if choice == "1":
        initializeClient = True
        send_mail(mailserver, SERVER_PORT_SMTP, user, subject, content, list_File, list_TO, list_CC, list_BCC, initializeClient);
    elif choice == "2":
        chucNang_2(SERVER_PORT_POP3)
    elif choice == "3":
        stop_fetching = True;
        break;
    
# Wait for the fetch thread to finish (optional)
fetch_thread.join()
