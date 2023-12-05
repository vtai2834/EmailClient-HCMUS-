import socket
import os
import base64

FORMAT = "utf8"
MAX_SIZE = 1024 * 3

#send TO and CC and BCC:
def send_TO_CC_BCC(attachment_path, clientSocket, user, list_TO, list_CC, list_BCC, subject, content, to, cc, bcc):
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
        print('250 reply not received from server.')

    list = []
    for i in list_TO:
        check_have = False
        for j in list:
            if i == j:
                check_have = True
        if not check_have:
            list.append(i)
    
    for i in list_CC:
        check_have = False
        for j in list:
            if i == j:
                check_have = True
        if not check_have:
            list.append(i)

    for i in list_BCC:
        check_have = False
        for j in list:
            if i == j:
                check_have = True
        if not check_have:
            list.append(i)
    
    for i in list:
        send = 'RCPT TO:<' + i + '>\r\n';
        clientSocket.send(send.encode(FORMAT));
        recv = clientSocket.recv(1024).decode();
    
    send = 'DATA\r\n';
    clientSocket.send(send.encode(FORMAT));
    recv = clientSocket.recv(1024).decode();
    if (recv[:3] != '354'):
        print('354 reply not received from server');

    clientSocket.send(b'To: ' + to.encode(FORMAT) + b'\r\n')
    clientSocket.send(b'Cc: ' + cc.encode(FORMAT) + b'\r\n')
    clientSocket.send(b'From: ' + user.encode(FORMAT) + b'\r\n');
    clientSocket.send(b'Subject: ' + subject.encode(FORMAT) + b'\r\n');
    clientSocket.send(b'Content-Type: multipart/mixed; boundary="boundary"\r\n\r\n')

    # Gửi phần text của email
    clientSocket.send(b'--boundary\r\n')
    clientSocket.send(b'Content-Type: text/plain; charset=UTF-8; format=flowed\r\n\r\n')
    clientSocket.send(content.encode(FORMAT) + b'\r\n')

    # Đọc nội dung của file.txt và mã hóa base64
    if (attachment_path):
        send_File(attachment_path, clientSocket)

    # Kết thúc email
    clientSocket.send(b'--boundary--\r\n.\r\n')

    recv = clientSocket.recv(1024).decode()

    # Send QUIT command and get server response.
    clientSocket.send(b'QUIT\r\n')
    recv_quit = clientSocket.recv(1024).decode()
#send CC and BCC:
def send_CC_BCC(attachment_path, clientSocket, user, list_CC, list_BCC, subject, content, cc, bcc):
    # Send HELO command and print server response.
    heloCommand = 'EHLO [127.0.0.1]\r\n'
    clientSocket.send(heloCommand.encode(FORMAT))
    recv1 = clientSocket.recv(1024).decode()

    if recv1[:3] != '250':
        print('250 reply not received from server.')

    # Send MAIL FROM command and print server response.
    send = 'MAIL FROM:<' + user + '>\r\n'
    clientSocket.send(send.encode(FORMAT))
    recv = clientSocket.recv(1024).decode()

    if (recv[:3] != '250'):
        print('250 reply not received from server.')

    for i in list_CC:
        send = 'RCPT TO:<' + i + '>\r\n';
        clientSocket.send(send.encode(FORMAT));
        recv = clientSocket.recv(1024).decode();
    for i in list_BCC:
        check = 0
        for j in list_CC:
            if (i == j):
                check = 1
                break
        if check == 0:
            send = 'RCPT TO:<' + i + '>\r\n'
            clientSocket.send(send.encode(FORMAT))
            recv = clientSocket.recv(1024).decode()
    
    send = 'DATA\r\n';
    clientSocket.send(send.encode(FORMAT));
    recv = clientSocket.recv(1024).decode();
    if (recv[:3] != '354'):
        print('354 reply not received from server');

    clientSocket.send(b'To: ' + cc.encode(FORMAT) + b'\r\n')
    clientSocket.send(b'From: ' + user.encode(FORMAT) + b'\r\n');
    clientSocket.send(b'Subject: ' + subject.encode(FORMAT) + b'\r\n');
    clientSocket.send(b'Content-Type: multipart/mixed; boundary="boundary"\r\n\r\n')

    # Gửi phần text của email
    clientSocket.send(b'--boundary\r\n')
    clientSocket.send(b'Content-Type: text/plain;charset=UTF-8; format=flowed\r\n\r\n')
    clientSocket.send(content.encode(FORMAT) + b'\r\n')

    # Đọc nội dung của file.txt và mã hóa base64
    if (attachment_path):
        send_File(attachment_path, clientSocket)

    # Kết thúc email
    clientSocket.send(b'--boundary--\r\n.\r\n')

    recv = clientSocket.recv(1024).decode()

    # Send QUIT command and get server response.
    clientSocket.send(b'QUIT\r\n')
    recv_quit = clientSocket.recv(1024).decode()
#send TO and BCC:
def send_TO_BCC(attachment_path, clientSocket, user, list_TO, list_BCC, subject, content, to, bcc):
    # Send HELO command and print server response.
    heloCommand = 'EHLO [127.0.0.1]\r\n'
    clientSocket.send(heloCommand.encode(FORMAT))
    recv1 = clientSocket.recv(1024).decode()

    if recv1[:3] != '250':
        print('250 reply not received from server.')

    # Send MAIL FROM command and print server response.
    send = 'MAIL FROM:<' + user + '>\r\n'
    clientSocket.send(send.encode(FORMAT))
    recv = clientSocket.recv(1024).decode()

    if (recv[:3] != '250'):
        print('250 reply not received from server.')

    for i in list_TO:
        send = 'RCPT TO:<' + i + '>\r\n';
        clientSocket.send(send.encode(FORMAT));
        recv = clientSocket.recv(1024).decode();
    for i in list_BCC:
        check = 0
        for j in list_TO:
            if (i == j):
                check = 1
                break
        if check == 0:
            send = 'RCPT TO:<' + i + '>\r\n'
            clientSocket.send(send.encode(FORMAT))
            recv = clientSocket.recv(1024).decode()
    
    send = 'DATA\r\n';
    clientSocket.send(send.encode(FORMAT));
    recv = clientSocket.recv(1024).decode();
    if (recv[:3] != '354'):
        print('354 reply not received from server');

    clientSocket.send(b'To: ' + to.encode(FORMAT) + b'\r\n')
    clientSocket.send(b'From: ' + user.encode(FORMAT) + b'\r\n');
    clientSocket.send(b'Subject: ' + subject.encode(FORMAT) + b'\r\n');
    clientSocket.send(b'Content-Type: multipart/mixed; boundary="boundary"\r\n\r\n')

    # Gửi phần text của email
    clientSocket.send(b'--boundary\r\n')
    clientSocket.send(b'Content-Type: text/plain; charset=UTF-8; format=flowed\r\n\r\n')
    clientSocket.send(content.encode(FORMAT) + b'\r\n')

    # Đọc nội dung của file.txt và mã hóa base64
    if (attachment_path):
        send_File(attachment_path, clientSocket)

    # Kết thúc email
    clientSocket.send(b'--boundary--\r\n.\r\n')

    recv = clientSocket.recv(1024).decode()

    # Send QUIT command and get server response.
    clientSocket.send(b'QUIT\r\n')
    recv_quit = clientSocket.recv(1024).decode()

#send TO and CC:
def send_TO_CC(attachment_path, clientSocket, user, list_TO, list_CC, subject, content, to, cc):
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
        print('250 reply not received from server.')

    for i in list_TO:
        send = 'RCPT TO:<' + i + '>\r\n';
        clientSocket.send(send.encode(FORMAT));
        recv = clientSocket.recv(1024).decode();
    for i in list_CC:
        check = 0
        for j in list_TO:
            if (i == j):
                check = 1
                break
        if check == 0:
            send = 'RCPT TO:<' + i + '>\r\n'
            clientSocket.send(send.encode(FORMAT))
            recv = clientSocket.recv(1024).decode()
    
    send = 'DATA\r\n';
    clientSocket.send(send.encode(FORMAT));
    recv = clientSocket.recv(1024).decode();
    if (recv[:3] != '354'):
        print('354 reply not received from server');

    clientSocket.send(b'To: ' + to.encode(FORMAT) + b'\r\n')
    clientSocket.send(b'Cc: ' + cc.encode(FORMAT) + b'\r\n')
    clientSocket.send(b'From: ' + user.encode(FORMAT) + b'\r\n');
    clientSocket.send(b'Subject: ' + subject.encode(FORMAT) + b'\r\n');
    clientSocket.send(b'Content-Type: multipart/mixed; boundary="boundary"\r\n\r\n')

    # Gửi phần text của email
    clientSocket.send(b'--boundary\r\n')
    clientSocket.send(b'Content-Type: text/plain;charset=UTF-8; format=flowed\r\n\r\n')
    clientSocket.send(content.encode(FORMAT) + b'\r\n')

    # Đọc nội dung của file.txt và mã hóa base64
    if (attachment_path):
        send_File(attachment_path, clientSocket)

    # Kết thúc email
    clientSocket.send(b'--boundary--\r\n.\r\n')

    recv = clientSocket.recv(1024).decode()

    # Send QUIT command and get server response.
    clientSocket.send(b'QUIT\r\n')
    recv_quit = clientSocket.recv(1024).decode()

# Send TO
def send_TO(attachment_path, clientSocket, user, list_TO, subject, content):
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
        clientSocket.send(b'To: ' + i.encode(FORMAT) + b'\r\n');
    clientSocket.send(b'From: ' + user.encode(FORMAT) + b'\r\n');
    clientSocket.send(b'Subject: ' + subject.encode(FORMAT) + b'\r\n');
    clientSocket.send(b'Content-Type: multipart/mixed; boundary="boundary"\r\n\r\n')

    # Gửi phần text của email
    clientSocket.send(b'--boundary\r\n')
    clientSocket.send(b'Content-Type: text/plain; charset=UTF-8; format=flowed\r\n\r\n')
    clientSocket.send(content.encode(FORMAT) + b'\r\n')

    # Đọc nội dung của file.txt và mã hóa base64
    if (attachment_path):
        send_File(attachment_path, clientSocket)

    # Kết thúc email
    clientSocket.send(b'--boundary--\r\n.\r\n')

    recv = clientSocket.recv(1024).decode()

    # Send QUIT command and get server response.
    clientSocket.send(b'QUIT\r\n')
    recv_quit = clientSocket.recv(1024).decode()
    
# Send CC
def send_CC(attachment_path, clientSocket, user, list_CC, subject, content):
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
        clientSocket.send(b'CC: ' + i.encode(FORMAT) + b'\r\n');
    clientSocket.send(b'From: ' + user.encode(FORMAT) + b'\r\n');
    clientSocket.send(b'Subject: ' + subject.encode(FORMAT) + b'\r\n');
    clientSocket.send(b'Content-Type: multipart/mixed; boundary="boundary"\r\n\r\n')

    # Gửi phần text của email
    clientSocket.send(b'--boundary\r\n')
    clientSocket.send(b'Content-Type: text/plain; charset=UTF-8; format=flowed\r\n\r\n')
    clientSocket.send(content.encode(FORMAT) + b'\r\n')

    # Đọc nội dung của file.txt và mã hóa base64
    if (attachment_path):
        send_File(attachment_path, clientSocket)

    # Kết thúc email
    clientSocket.send(b'--boundary--\r\n.\r\n')
    recv = clientSocket.recv(1024).decode()

    # Send QUIT command and get server response.
    clientSocket.send(b'QUIT\r\n')
    recv_quit = clientSocket.recv(1024).decode()
    
# Send BCC
def send_BCC(attachment_path, clientSocket, user, list_BCC, subject, content):
    # Send HELO command and print server response.
    heloCommand = 'EHLO [127.0.0.1]\r\n'
    clientSocket.send(heloCommand.encode(FORMAT))
    recv1 = clientSocket.recv(1024).decode()

    if recv1[:3] != '250':
        print('250 reply not received from server.')

    # Send MAIL FROM command and print server response.
    send = 'MAIL FROM:<' + user + '>\r\n'
    clientSocket.send(send.encode(FORMAT))
    recv = clientSocket.recv(1024).decode()

    if (recv[:3] != '250'):
        print('250 reply not received from server.');
    for i in list_BCC:
        send = 'RCPT TO:<' + i + '>\r\n';
        clientSocket.send(send.encode(FORMAT));
        recv = clientSocket.recv(1024).decode();

    send = 'DATA\r\n';
    clientSocket.send(send.encode(FORMAT));
    recv = clientSocket.recv(1024).decode();

    if (recv[:3] != '354'):
        print('354 reply not received from server');

    # Data mail: 
    clientSocket.send(b'To: ' + 'undisclosed-recipients: ;'.encode(FORMAT) + b'\r\n');
    clientSocket.send(b'From: ' + user.encode(FORMAT) + b'\r\n');
    clientSocket.send(b'Subject: ' + subject.encode(FORMAT) + b'\r\n');
    clientSocket.send(b'Content-Type: multipart/mixed; boundary="boundary"\r\n\r\n')

    # Gửi phần text của email
    clientSocket.send(b'--boundary\r\n')
    clientSocket.send(b'Content-Type: text/plain; charset=UTF-8; format=flowed\r\n\r\n')
    clientSocket.send(content.encode(FORMAT) + b'\r\n')

    # Đọc nội dung của file.txt và mã hóa base64
    if (attachment_path):
        send_File(attachment_path, clientSocket)

    # Kết thúc email
    clientSocket.send(b'--boundary--\r\n.\r\n')
    recv = clientSocket.recv(1024).decode()

    # Send QUIT command and get server response.
    clientSocket.send(b'QUIT\r\n')
    recv_quit = clientSocket.recv(1024).decode()

# Send File
def send_File(attachment_path_list, clientSocket):
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
            clientSocket.send(f'Content-Type: application/octet-stream; name="{attachment_name}"\r\n'.encode(FORMAT))
            clientSocket.send(f'Content-Disposition: attachment; filename="{attachment_name}"\r\n'.encode(FORMAT))
            clientSocket.send(f'Content-Transfer-Encoding: base64\r\n\r\n'.encode(FORMAT))

            # Chia nhỏ dữ liệu đính kèm thành các dòng nhỏ hơn
            chunk_size = 76  # Độ dài tối đa của mỗi dòng
            for i in range(0, len(encoded_attachment), chunk_size):
                clientSocket.send(encoded_attachment[i:i+chunk_size].encode(FORMAT) + b'\r\n')

        elif (last_three_char == 'pdf'):
            # Gửi phần đính kèm *.pdf của email
            clientSocket.send(b'--boundary\r\n')
            clientSocket.send(f'Content-Type: application/pdf; name="{attachment_name}"\r\n'.encode(FORMAT));
            clientSocket.send(f'Content-Disposition: attachment; filename="{attachment_name}"\r\n'.encode(FORMAT))
            clientSocket.send(f'Content-Transfer-Encoding: base64\r\n\r\n'.encode(FORMAT))

            # Chia nhỏ dữ liệu đính kèm thành các dòng nhỏ hơn
            chunk_size = 76  # Độ dài tối đa của mỗi dòng
            for i in range(0, len(encoded_attachment), chunk_size):
                clientSocket.send(encoded_attachment[i:i+chunk_size].encode(FORMAT) + b'\r\n')

        elif (last_three_char == 'ocx'):
            #gửi phần đính kèm *.doc của email
            clientSocket.send(b'--boundary\r\n')
            clientSocket.send(f'Content-Type: application/msword; name="{attachment_name}"\r\n'.encode(FORMAT))
            clientSocket.send(f'Content-Disposition: attachment; filename="{attachment_name}"\r\n'.encode(FORMAT))
            clientSocket.send(f'Content-Transfer-Encoding: base64\r\n\r\n'.encode(FORMAT))

            # clientSocket.send(encoded_attachment.encode(FORMAT) + b'\r\n')

            # Chia nhỏ dữ liệu đính kèm thành các dòng nhỏ hơn
            chunk_size = 76  # Độ dài tối đa của mỗi dòng
            for i in range(0, len(encoded_attachment), chunk_size):
                clientSocket.send(encoded_attachment[i:i+chunk_size].encode(FORMAT) + b'\r\n')

        elif (last_three_char == 'jpg'):
            #gửi phần đính kèm *.jpg của email
            clientSocket.send(b'--boundary\r\n')
            clientSocket.send(f'Content-Type: image/jpeg; name="{attachment_name}"\r\n'.encode(FORMAT))
            clientSocket.send(f'Content-Disposition: attachment; filename="{attachment_name}"\r\n'.encode(FORMAT))
            clientSocket.send(f'Content-Transfer-Encoding: base64\r\n\r\n'.encode(FORMAT))

            # Chia nhỏ dữ liệu đính kèm thành các dòng nhỏ hơn
            chunk_size = 76  # Độ dài tối đa của mỗi dòng
            for i in range(0, len(encoded_attachment), chunk_size):
                clientSocket.send(encoded_attachment[i:i+chunk_size].encode(FORMAT) + b'\r\n')

        elif (last_three_char == 'zip'):
            #gửi phần đính kèm *.zip của email:
            clientSocket.send(b'--boundary\r\n')
            clientSocket.send(f'Content-Type: application/zip; name="{attachment_name}"\r\n'.encode(FORMAT))
            clientSocket.send(f'Content-Disposition: attachment; filename="{attachment_name}"\r\n'.encode(FORMAT))
            clientSocket.send(f'Content-Transfer-Encoding: base64\r\n\r\n'.encode(FORMAT))

            # Chia nhỏ dữ liệu đính kèm thành các dòng nhỏ hơn
            chunk_size = 76  # Độ dài tối đa của mỗi dòng
            for i in range(0, len(encoded_attachment), chunk_size):
                clientSocket.send(encoded_attachment[i:i+chunk_size].encode(FORMAT) + b'\r\n')

def send_mail(mailserver, SERVER_PORT_SMTP, user, subject, content, list_File, list_TO, list_CC, list_BCC, initializeClient):
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


    if (to and cc):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((mailserver, SERVER_PORT_SMTP))

        recv = clientSocket.recv(1024).decode()
        print(recv)
        if recv[:3] != '220':
            print('\n 220 reply not received from server.')
        send_TO_CC(list_File, clientSocket, user, list_TO, list_CC, subject, content, to, cc)
    elif (to and bcc):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((mailserver, SERVER_PORT_SMTP))

        recv = clientSocket.recv(1024).decode()
        print(recv)
        if recv[:3] != '220':
            print('\n 220 reply not received from server.')
        send_TO_BCC(list_File, clientSocket, user, list_TO, list_BCC, subject, content, to, bcc)
    elif (cc and bcc):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((mailserver, SERVER_PORT_SMTP))

        recv = clientSocket.recv(1024).decode()
        print(recv)
        if recv[:3] != '220':
            print('\n 220 reply not received from server.')
        send_CC_BCC(list_File, clientSocket, user, list_CC, list_BCC, subject, content, cc, bcc)
    elif (to and cc and bcc):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((mailserver, SERVER_PORT_SMTP))

        recv = clientSocket.recv(1024).decode()
        print(recv)
        if recv[:3] != '220':
            print('\n 220 reply not received from server.')
        send_TO_CC_BCC(list_File, clientSocket, user, list_TO, list_CC, list_BCC, subject, content, to, cc, bcc)
    elif to:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((mailserver, SERVER_PORT_SMTP))

        recv = clientSocket.recv(1024).decode()
        print(recv)
        if recv[:3] != '220':
            print('\n 220 reply not received from server.')
        send_TO(list_File, clientSocket, user, list_TO, subject, content)
    elif cc:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        clientSocket.connect((mailserver, SERVER_PORT_SMTP))
        
        recv = clientSocket.recv(1024).decode()
        print(recv)
        if recv[:3] != '220':
            print('\n 220 reply not received from server.')
        send_CC(list_File, clientSocket, user, list_CC, subject, content)
    elif bcc:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        clientSocket.connect((mailserver, SERVER_PORT_SMTP))
        for i in range(len(list_BCC)):
            recv = clientSocket.recv(1024).decode()
            print(recv)
            if recv[:3] != '220':
                print('\n 220 reply not received from server.')
            send_BCC(list_File, clientSocket, user, list_BCC, subject, content)
    # Đóng socket
    if initializeClient:
        clientSocket.close()