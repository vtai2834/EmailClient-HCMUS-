import json

def readJson():
    with open('config.json', 'r') as file:
        content = file.read()
    
    # print(content)
    
    name_Start = content.find("Username\": \"") + len("Username\": \"")
    name_End = content.find(" <")
    name = content[name_Start : name_End]

    user_Start = name_End + len(" <")
    user_End = content.find(">")
    user = content[user_Start : user_End]
    
    pass_Start = content.find("Password\": \"") + len("Password\": \"")
    pass_End = content.find("\",", pass_Start)
    password = content[pass_Start : pass_End]
    
    mailserver_Start = content.find("MailServer\": \"") + len("MailServer\": \"")
    mailserver_End = content.find("\",", mailserver_Start)
    mailserver = content[mailserver_Start : mailserver_End]
    
    smtp_Start = content.find("SMTP\": ") + len("SMTP\": ")
    smtp_End = content.find("," , smtp_Start)
    smtp = content[smtp_Start : smtp_End]
    
    pop3_Start = content.find("POP3\": ") + len("POP3\": ")
    pop3_End = content.find("," , pop3_Start)
    pop3 = content[pop3_Start : pop3_End]
    
    autoload_Start = content.find("Autoload\": ") + len("Autoload\": ")
    autoload_End = content.find("\n", autoload_Start)
    autoload = content[autoload_Start : autoload_End]
    
    project_Start = content.find("From\": [\"") + len("From\": [\"")
    project_End = content.find("\"],", project_Start)
    projectTMP = content[project_Start : project_End]
    project = projectTMP.split('\", \"')
    
    
    important_Start = content.find("Subject\": [\"") + len("Subject\": [\"")
    important_End = content.find("\"],", important_Start)
    importantTMP = content[important_Start : important_End]
    important = importantTMP.split('\", \"')
    
    work_Start = content.find("Content\": [\"") + len("Content\": [\"")
    work_End = content.find("\"],", work_Start)
    workTMP = content[work_Start : work_End]
    work = workTMP.split('\", \"')
    
    spam_Start = content.find("Spam\": [\"") + len("Spam\": [\"")
    spam_End = content.find("\"],", spam_Start)
    spamTMP = content[spam_Start : spam_End]
    spam = spamTMP.split('\", \"')
    
    # print(name)
    # print(user)
    # print(password)
    # print(mailserver)
    # print(smtp)
    # print(pop3)
    # print(autoload)
    # print(project)
    # print(important)
    # print(work)
    # print(spam)
    
    return name, user, password, mailserver, smtp, pop3, autoload, project, important, work, spam