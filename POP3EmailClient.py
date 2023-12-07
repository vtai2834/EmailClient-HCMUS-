import socket
import os
import base64
from ReadJSON import readJson

name, user, password, mailserver, smtp, pop3, autoload, project, important, work, spam = readJson()


FORMAT = "utf8";
SERVER_PORT_POP3 = int(pop3)
MAX_SIZE = 1024*3

#chuadoc
def check_Readed(data):
    if data[-7:] == 'chuadoc': return 1
    return 0

def Read_Mail(folder):
    list_data = []
    list_from = []
    list_sub = []

    for i in range(len(os.listdir(folder))):
        with open(folder + '/Mail' + str(i + 1) + '.txt', 'r') as attachment_file:
            attachment_data = attachment_file.read()
        data = attachment_data
        list_data.append(data)

        from_start_idx = data.find('From: ') + len('From: ')
        from_end_idx = data.find('Subject: ')
        list_from.append(data[from_start_idx : (from_end_idx - len('\r\n'))])

        subject_start_idx = data.find('Subject: ') + len('Subject: ')
        if (data.find('MIME-Version: 1.0') != -1):
            if (data.find('This is a multi-part message in MIME format.') != -1):
                subject_end_idx = data.find('This is a multi-part message in MIME format.') - len('\r\n\r\n')
            else:
                subject_end_idx = data.find('Content', subject_start_idx) - len('\r\n')
        else:
            subject_end_idx = data.find('Content', subject_start_idx) - len('\r\n')
        list_sub.append(data[subject_start_idx : subject_end_idx])

    while True:
        os.system("cls")
        print("Đây là danh sách email:")
        for i in range (len(list_data)):
            if (check_Readed(list_data[i]) == 1):
                print(str(i+1) + '. (chưa đọc)' +  ' <' + list_from[i] + '>, <' + list_sub[i] + '>')
            else:
                print(str(i+1) + '. <' + list_from[i] + '>, <' + list_sub[i] + '>')
    

        check = input('\nBạn muốn đọc Email thứ mấy (hoặc nhấn enter để thoát ra ngoài, hoặc nhấn 0 để xem lại danh sách email): ')
        if (not check):
            os.system("cls")
            return
        if(int(check) <= len(list_data)):
            if (check != '0'):
                check = int(check)
                print('Nội dung email của email thứ ' + str(check) + ': ')
                # lấy nội dung email:
                # print(list_data[0])
                data_idx = 0
                data_idx_end = 0

                if list_data[check-1].find('MIME-Version: 1.0') != -1: #gui = thunderbird
                    data_idx = list_data[check-1].find('Content-Transfer-Encoding: 7bit') + len('Content-Transfer-Encoding: 7bit\r\n\r\n')
                    if (list_data[check-1].find('Content-Transfer-Encoding: base64') == -1): # khong co file đính kèm
                        data_idx_end = list_data[check-1].find('\r\n.\r\n')
                    else: # không có file đính kèm
                        data_idx_end = list_data[check -1].find('--------------', data_idx) - len('\r\n')
                else: #gui mail = python roi lay ve
                    data_idx = list_data[check-1].find('Content-Type: text/plain; charset=UTF-8; format=flowed') + len('Content-Type: text/plain; charset=UTF-8; format=flowed\r\n\r\n')
                    if (list_data[check-1].find('Content-Transfer-Encoding: base64') != -1): # có file đính kèm
                        data_idx_end = list_data[check -1].find('--boundary', data_idx);
                    else: # không có file đính kèm
                        data_idx_end = list_data[check -1].find('--boundary--', data_idx)

                data_res = list_data[check -1][data_idx : data_idx_end]
                print(data_res)

                
                if (list_data[check-1].find('Content-Transfer-Encoding: base64') == -1): 
                    if (check_Readed(list_data[check -1]) == 1):
                        with open(folder + '/Mail' + str(check) + '.txt', "w") as attachment_file: # wb : mở file, xóa nd cũ, ghi nd mới
                            attachment_file.write(list_data[check-1].replace('chuadoc', 'dadoc'))
                    return; # kh có attachment file
            

                char = input('Trong email này có attached file, bạn có muốn save không : ')
                if (char == 'có' or char == 'co'):
                    path = input('Cho biết đường dẫn bạn muốn lưu (nhập thêm kí tự \ vào cuối): ')

                    # xác định nếu có file đính kèm và lấy thong tin file:
                    pos = data_idx_end
                    i = 0
                    num_file = list_data[check -1].count('Content-Transfer-Encoding: base64')
                    attachment_start = -1
                    while (list_data[check -1].find('Content-Transfer-Encoding: base64', pos) != -1):
                        attachment_start = list_data[check -1].find('Content-Transfer-Encoding: base64', pos)

                        if attachment_start != -1: # có file
                            i += 1
                            idx_start = attachment_start + len('Content-Transfer-Encoding: base64\r\n\r\n'); # cho \r\n\r\n
                            idx_end = 0

                            if (list_data[check-1].find('MIME-Version: 1.0') != -1): # mail do thunderbird gui
                                idx_end = list_data[check-1].find('--------------', idx_start);
                            else:
                                if (i != num_file):
                                    idx_end = list_data[check -1].find('--boundary', idx_start)
                                else:
                                    idx_end = list_data[check -1].find('--boundary--')
                            
                            res = list_data[check -1][idx_start : idx_end]

                            #tên file đính kèm:
                            attachment_file = ''
                            if (list_data[check -1].find('Content-Type: application/octet-stream', pos, idx_end) != -1 or list_data[check -1].find('Content-Type: text/plain', pos, idx_end) != -1):
                                attachment_file = 'download.txt'
                            elif (list_data[check -1].find('Content-Type: application/pdf', pos, idx_end) != -1):
                                attachment_file = 'download.pdf'
                            elif(list_data[check -1].find('Content-Type: application/msword', pos, idx_end) != -1 or list_data[check-1].find('Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document') != -1):
                                attachment_file = 'download.docx'
                            elif (list_data[check -1].find('Content-Type: image/jpeg', pos, idx_end) != -1):
                                attachment_file = 'download.jpg'
                            elif (list_data[check -1].find('Content-Type: application/zip', pos, idx_end) != -1 or list_data[check-1].find('Content-Type: application/x-zip-compressed') != -1):
                                attachment_file = 'download.zip'

                            # print(attachment_file)
                            # kiểm tra -> tạo file -> ghi dữ liệu vào:
                            if not os.path.exists(path + attachment_file):
                                with open(attachment_file, "xb") as attachment_file: # xb : kiểm tra nếu chưa có file đó thì tạo ra file mới tự động, còn có rồi thì kh thực hiện
                                    attachment_file.write(base64.b64decode(res))
                            else:
                                print('file alredy exist')
                            pos = idx_end
            elif (check == '0'):
                continue
            # đổi lại mail này thành mail đã đọc:
            if (check_Readed(list_data[check -1]) == 1):
                with open(folder + '/Mail' + str(check) + '.txt', "w") as attachment_file: # wb : mở file, xóa nd cũ, ghi nd mới
                    attachment_file.write(list_data[check-1].replace('chuadoc', 'dadoc'))

def receive_mail(SERVER_PORT_POP3):
    list_sender = []
    list_subject = []
    # Create socket called clientSocket and establish a TCP connection with mailserver
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    clientSocket.connect((mailserver, SERVER_PORT_POP3))

    # nhận thông báo từ mail server:
    response = clientSocket.recv(1024).decode();

    # gửi lệnh USER để xác thực:
    clientSocket.send(b'USER ' + user.encode(FORMAT) + b'\r\n')
    response = clientSocket.recv(1024).decode()

    # gửi lệnh pass để xác thực:
    clientSocket.send(b'PASS ' + password.encode(FORMAT) + b'\r\n')
    response = clientSocket.recv(1024).decode()

    # gửi lệnh STAT -> lấy số byte có trong mail:
    clientSocket.send('STAT\r\n'.encode(FORMAT))
    response = clientSocket.recv(1024).decode();

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
        #Di chuyển các email được gửi từ địa chỉ ahihi@testing.com và ahuu@testing.com vào thư mục Project
        from_start_idx = response.find('From:') + len('From:')
        from_end_idx = response.find('Subject:')
        list_sender.append(response[from_start_idx : (from_end_idx - len('\r\n'))])


        subject_start_idx = response.find('Subject: ') + len('Subject: ')
        if (response.find('MIME-Version: 1.0') != -1):
            if (response.find('This is a multi-part message in MIME format.') != -1):
                subject_end_idx = response.find('This is a multi-part message in MIME format.') - len('\r\n\r\n')
            else:
                subject_end_idx = response.find('Content', subject_start_idx) - len('\r\n')
        else:
            subject_end_idx = response.find('Content', subject_start_idx) - len('\r\n')
        list_subject.append(response[subject_start_idx : subject_end_idx])

        
        # Xu ly loc mail:
        if (project.count(list_sender[i-1]) != 0):
            cnt = len(os.listdir('Project'))
            with open('Project/Mail' + str(cnt + 1) + '.txt', "w") as attachment_file: # xb : kiểm tra nếu chưa có file đó thì tạo ra file mới tự động, còn có rồi thì kh thực hiện
                attachment_file.write(response + 'chuadoc') # tai mail ve folder luon mac dinh la chua doc
        elif any(j in list_subject[i-1] for j in important):
            cnt = len(os.listdir('Important'))
            with open('Important/Mail' + str(cnt + 1) + '.txt', "w") as attachment_file:
                attachment_file.write(response + 'chuadoc')
        elif any(response.find(i) != -1 for i in work):
            cnt = len(os.listdir('Work'))
            with open('Work/Mail' + str(cnt + 1) + '.txt', "w") as attachment_file:
                attachment_file.write(response + 'chuadoc')
        elif (any(j in list_subject[i-1] for j in spam) or any(response.find(i) != -1 for i in spam)):
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

    clientSocket.close()

    while (1):
        print('Đây là danh sách các folder trong mailbox của bạn: ')
        print('1. Inbox')
        print('2. Project')
        print('3. Important')
        print('4. Work')
        print('5. Spam')
        choose = input('Bạn muốn xem email trong folder nào (Nhấn enter để thoát ra ngoài): ')

        if (not choose):
            break
        elif choose == '1':
            Read_Mail('Inbox')
        elif choose == '2':
            Read_Mail('Project')
        elif choose == '3':
            Read_Mail('Important')
        elif choose == '4':
            Read_Mail('Work')
        elif choose == '5':
            Read_Mail('Spam')