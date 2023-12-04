# java -jar test-mail-server-1.0.jar -s 2225 -p 3335 -m ./
import socket
import os
import base64
import time
import threading

from POP3EmailClient import chucNang_2
from ReadJSON import docJson

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

FORMAT = "utf8"
SERVER_PORT_SMTP = int(smtp)
SERVER_PORT_POP3 = int(pop3)
MAX_SIZE = 1024 * 3



# Send TO
def send_TO(attachment_path):
    # Send HELO command and print server response.
    heloCommand = 'EHLO [127.0.0.1]\r\n'
    clientSocket.send(heloCommand.encode(FORMAT))
    recv1 = clientSocket.recv(1024).decode()

    if recv1[:3] != '250':
        print('250 reply not received from server.')

    # Send MAIL FROM command and print server response.
    send = 'MAIL FROM:<' + user + '>\r\n';
    clientSocket.send(send.encode(FORMAT));
    recv = clientSocket.recv(1024).decode();

    if (recv[:3] != '250'):
        print('250 reply not received from server.');
        
    for i in list_TO:
        send = 'RCPT TO:<' + i + '>\r\n';
        clientSocket.send(send.encode(FORMAT));
        recv = clientSocket.recv(1024).decode();
    
    send = 'DATA\r\n';
    clientSocket.send(send.encode(FORMAT));
    recv = clientSocket.recv(1024).decode();

    if (recv[:3] != '354'):
        print('354 reply not received from server');

    #goi du lieu mail: 
    for i in list_TO:
        clientSocket.send(b'To:' + i.encode(FORMAT) + b'\r\n');
    clientSocket.send(b'From:' + user.encode(FORMAT) + b'\r\n');
    clientSocket.send(b'Subject:' + subject.encode(FORMAT) + b'\r\n');
    clientSocket.send(b'Content-Type:multipart/mixed; boundary="boundary"\r\n\r\n')

    # Gửi phần text của email
    clientSocket.send(b'--boundary\r\n')
    clientSocket.send(b'Content-Type:text/plain;charset=UTF-8;format=flowed\r\n\r\n')
    clientSocket.send(content.encode(FORMAT) + b'\r\n')

    # Đọc nội dung của file.txt và mã hóa base64
    if (attachment_path):
        send_File(attachment_path)

    # Kết thúc email
    clientSocket.send(b'--boundary--\r\n.\r\n')

    recv = clientSocket.recv(1024).decode()

    # Send QUIT command and get server response.
    clientSocket.send(b'QUIT\r\n')
    recv_quit = clientSocket.recv(1024).decode()
    
# Send CC
def send_CC(attachment_path):
    # Send HELO command and print server response.
    heloCommand = 'EHLO [127.0.0.1]\r\n'
    clientSocket.send(heloCommand.encode(FORMAT))
    recv1 = clientSocket.recv(1024).decode()

    if recv1[:3] != '250':
        print('250 reply not received from server.')

    # Send MAIL FROM command and print server response.
    send = 'MAIL FROM:<' + user + '>\r\n';
    clientSocket.send(send.encode(FORMAT));
    recv = clientSocket.recv(1024).decode();

    if (recv[:3] != '250'):
        print('250 reply not received from server.');
        
    for i in list_CC:
        send = 'RCPT TO:<' + i + '>\r\n';
        clientSocket.send(send.encode(FORMAT));
        recv = clientSocket.recv(1024).decode();
    
    send = 'DATA\r\n';
    clientSocket.send(send.encode(FORMAT));
    recv = clientSocket.recv(1024).decode();

    if (recv[:3] != '354'):
        print('354 reply not received from server');

    # Data mail: 
    for i in list_CC:
        clientSocket.send(b'CC:' + i.encode(FORMAT) + b'\r\n');
    clientSocket.send(b'From:' + user.encode(FORMAT) + b'\r\n');
    clientSocket.send(b'Subject:' + subject.encode(FORMAT) + b'\r\n');
    clientSocket.send(b'Content-Type:multipart/mixed; boundary="boundary"\r\n\r\n')

    # Gửi phần text của email
    clientSocket.send(b'--boundary\r\n')
    clientSocket.send(b'Content-Type:text/plain;charset=UTF-8;format=flowed\r\n\r\n')
    clientSocket.send(content.encode(FORMAT) + b'\r\n')

    # Đọc nội dung của file.txt và mã hóa base64
    if (attachment_path):
        send_File(attachment_path)

    # Kết thúc email
    clientSocket.send(b'--boundary--\r\n.\r\n')
    recv = clientSocket.recv(1024).decode()

    # Send QUIT command and get server response.
    clientSocket.send(b'QUIT\r\n')
    recv_quit = clientSocket.recv(1024).decode()
    
# Send BCC
def send_BCC(bcc, attachment_path):
    # Send HELO command and print server response.
    heloCommand = 'EHLO [127.0.0.1]\r\n'
    clientSocket.send(heloCommand.encode(FORMAT))
    recv1 = clientSocket.recv(1024).decode()

    if recv1[:3] != '250':
        print('250 reply not received from server.')

    # Send MAIL FROM command and print server response.
    send = 'MAIL FROM:<' + user + '>\r\n';
    clientSocket.send(send.encode(FORMAT));
    recv = clientSocket.recv(1024).decode();

    if (recv[:3] != '250'):
        print('250 reply not received from server.');
    send = 'RCPT TO:<' + bcc + '>\r\n';
    clientSocket.send(send.encode(FORMAT));
    recv = clientSocket.recv(1024).decode();

    send = 'DATA\r\n';
    clientSocket.send(send.encode(FORMAT));
    recv = clientSocket.recv(1024).decode();

    if (recv[:3] != '354'):
        print('354 reply not received from server');

    # Data mail: 
    clientSocket.send(b'To:' + bcc.encode(FORMAT) + b'\r\n');
    clientSocket.send(b'From:' + user.encode(FORMAT) + b'\r\n');
    clientSocket.send(b'Subject:' + subject.encode(FORMAT) + b'\r\n');
    clientSocket.send(b'Content-Type:multipart/mixed; boundary="boundary"\r\n\r\n')

    # Gửi phần text của email
    clientSocket.send(b'--boundary\r\n')
    clientSocket.send(b'Content-Type:text/plain;charset=UTF-8;format=flowed\r\n\r\n')
    clientSocket.send(content.encode(FORMAT) + b'\r\n')

    # Đọc nội dung của file.txt và mã hóa base64
    if (attachment_path):
        send_File(attachment_path)

    # Kết thúc email
    clientSocket.send(b'--boundary--\r\n.\r\n')
    recv = clientSocket.recv(1024).decode()

    # Send QUIT command and get server response.
    clientSocket.send(b'QUIT\r\n')
    recv_quit = clientSocket.recv(1024).decode()

# Send File
def send_File(attachment_path_list):
    size = 0
    # Có giới hạn dung lượng file gửi
    for attachment_path in attachment_path_list:
        if os.path.exists(attachment_path):
            size += os.path.getsize(attachment_path)
        else:
            print(f"File not found: {attachment_path}")
    size = size / 1024;
    if (size > MAX_SIZE): return ;

    # gửi file đính kèm
    for attachment_path in attachment_path_list:
        attachment_name = os.path.basename(attachment_path)
        with open(attachment_path, 'rb') as attachment_file:
            attachment_data = attachment_file.read()
        encoded_attachment = base64.b64encode(attachment_data).decode(FORMAT)  # Mã hóa base64

        last_three_char = attachment_name[-3:]
        if (last_three_char == 'txt'):
            # Gửi phần đính kèm *.txt của email
            clientSocket.send(b'--boundary\r\n')
            clientSocket.send(f'Content-Type:application/octet-stream; name="{attachment_name}"\r\n'.encode(FORMAT))
            clientSocket.send(f'Content-Disposition:attachment; filename="{attachment_name}"\r\n'.encode(FORMAT))
            clientSocket.send(f'Content-Transfer-Encoding: base64\r\n\r\n'.encode(FORMAT))

            # Chia nhỏ dữ liệu đính kèm thành các dòng nhỏ hơn
            chunk_size = 76  # Độ dài tối đa của mỗi dòng
            for i in range(0, len(encoded_attachment), chunk_size):
                clientSocket.send(encoded_attachment[i:i+chunk_size].encode(FORMAT) + b'\r\n')

        elif (last_three_char == 'pdf'):
            # Gửi phần đính kèm *.pdf của email
            clientSocket.send(b'--boundary\r\n')
            clientSocket.send(f'Content-Type:application/pdf; name="{attachment_name}"\r\n'.encode(FORMAT));
            clientSocket.send(f'Content-Disposition:attachment; filename="{attachment_name}"\r\n'.encode(FORMAT))
            clientSocket.send(f'Content-Transfer-Encoding: base64\r\n\r\n'.encode(FORMAT))

            # Chia nhỏ dữ liệu đính kèm thành các dòng nhỏ hơn
            chunk_size = 76  # Độ dài tối đa của mỗi dòng
            for i in range(0, len(encoded_attachment), chunk_size):
                clientSocket.send(encoded_attachment[i:i+chunk_size].encode(FORMAT) + b'\r\n')

        elif (last_three_char == 'ocx'):
            #gửi phần đính kèm *.doc của email
            clientSocket.send(b'--boundary\r\n')
            clientSocket.send(f'Content-Type:application/msword; name="{attachment_name}"\r\n'.encode(FORMAT))
            clientSocket.send(f'Content-Disposition:attachment; filename="{attachment_name}"\r\n'.encode(FORMAT))
            clientSocket.send(f'Content-Transfer-Encoding: base64\r\n\r\n'.encode(FORMAT))

            # clientSocket.send(encoded_attachment.encode(FORMAT) + b'\r\n')

            # Chia nhỏ dữ liệu đính kèm thành các dòng nhỏ hơn
            chunk_size = 76  # Độ dài tối đa của mỗi dòng
            for i in range(0, len(encoded_attachment), chunk_size):
                clientSocket.send(encoded_attachment[i:i+chunk_size].encode(FORMAT) + b'\r\n')

        elif (last_three_char == 'jpg'):
            #gửi phần đính kèm *.jpg của email
            clientSocket.send(b'--boundary\r\n')
            clientSocket.send(f'Content-Type:image/jpeg; name="{attachment_name}"\r\n'.encode(FORMAT))
            clientSocket.send(f'Content-Disposition:attachment; filename="{attachment_name}"\r\n'.encode(FORMAT))
            clientSocket.send(f'Content-Transfer-Encoding: base64\r\n\r\n'.encode(FORMAT))

            # Chia nhỏ dữ liệu đính kèm thành các dòng nhỏ hơn
            chunk_size = 76  # Độ dài tối đa của mỗi dòng
            for i in range(0, len(encoded_attachment), chunk_size):
                clientSocket.send(encoded_attachment[i:i+chunk_size].encode(FORMAT) + b'\r\n')

        elif (last_three_char == 'zip'):
            #gửi phần đính kèm *.zip của email:
            clientSocket.send(b'--boundary\r\n')
            clientSocket.send(f'Content-Type:application/zip; name="{attachment_name}"\r\n'.encode(FORMAT))
            clientSocket.send(f'Content-Disposition:attachment; filename="{attachment_name}"\r\n'.encode(FORMAT))
            clientSocket.send(f'Content-Transfer-Encoding: base64\r\n\r\n'.encode(FORMAT))

            # Chia nhỏ dữ liệu đính kèm thành các dòng nhỏ hơn
            chunk_size = 76  # Độ dài tối đa của mỗi dòng
            for i in range(0, len(encoded_attachment), chunk_size):
                clientSocket.send(encoded_attachment[i:i+chunk_size].encode(FORMAT) + b'\r\n')

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

stop_fetching = False

def auto_fetch_emails():
    while not stop_fetching:
        fetch_emails(user, password)
        time.sleep(10)


try:
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
            print("Đây là thông tin soạn email: (nếu không điền vui lòng nhấn enter để bỏ qua)")
            answer = input()

            to = input("To: ")
            if not to:
                print("<enter>\n")
            else:
                list_TO = to.split(', ')
                print()
                
            cc = input("CC: ")
            if not cc:
                print("<enter>\n")
            else:
                list_CC = cc.split(', ')
                print()
                
            bcc = input("BCC: ")
            if not bcc:
                print("<enter>\n")
            else:
                list_BCC = bcc.split(', ')
                print()
            
            subject = input("Subject: ")
            content = input("Content: ")
            
            attachment = int(input("Có gửi kèm file (1. có, 2. không): "))
            if attachment == 1:
                num_File = int(input("Số lượng file muốn gửi: "))
                for i in range(1, num_File + 1):
                    add = input("Cho biết đường dẫn file thứ " + str(i) + ": ")
                    list_File.append(add)
                    
            if to:
                clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                clientSocket.connect((mailserver, SERVER_PORT_SMTP))

                recv = clientSocket.recv(1024).decode()
                print(recv)
                if recv[:3] != '220':
                    print('\n 220 reply not received from server.')
                send_TO(list_File)
            if cc:
                clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
                clientSocket.connect((mailserver, SERVER_PORT_SMTP))
                
                recv = clientSocket.recv(1024).decode()
                print(recv)
                if recv[:3] != '220':
                    print('\n 220 reply not received from server.')
                send_CC(list_File)
            if bcc:
                for i in range(len(list_BCC)):
                    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
                    clientSocket.connect((mailserver, SERVER_PORT_SMTP))
                    
                    recv = clientSocket.recv(1024).decode()
                    print(recv)
                    if recv[:3] != '220':
                        print('\n 220 reply not received from server.')
                    send_BCC(list_BCC[i], list_File)
        elif choice == "2":
            chucNang_2(SERVER_PORT_POP3)
        elif choice == "3":
            stop_fetching = True;
            break;
        
    # Wait for the fetch thread to finish (optional)
    fetch_thread.join()

    # Đóng socket
    if initializeClient:
        clientSocket.close()
except:
    print('Error To Implement')