# -*- coding: utf-8 -*-
import pwd
#заводим счетчики
erroruser = []
errorpass = []
#получаем базу данных паролей
passwd_db = pwd.getpwall()
try:
    #проверяем каждое имя пользователя и пароль на валидность
    for entry in passwd_db:
        username = entry[0]
        password = entry [1]
        if len(username) < 6:
            erroruser.append(username)
        if len(password) < 8:
            errorpass.append(username)
    #выводим результаты на экран
    print "Следующие пользователи имеют имена менее чем из 6 символов:"
    for item in erroruser:
        print item
    print "\nСледующие пользователи имеют пароли менее чем из 8 символов:"
    for item in errorpass:
        print item
except:
    print "Возникла проблема при выполнении программы!"
