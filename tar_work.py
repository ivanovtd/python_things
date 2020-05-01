# -*- coding: utf-8 -*-
import tarfile, sys
try:
    #открываем tar-файл
    tar = tarfile.open(sys.argv[1], "r:tar")
    #выводим меню и сохраняем выбор
    selection = raw_input("Введите\n\
    1 чтобы извлечь файл\n\
    2 чтобы вывести информацию о файле в архиве\n\
    3 чтобы показать все файлы в архиве\n\n")
    #выполняем действия, основанные на выборе
    if selection == "1":
        filename = raw_input("введите имя файла для извлечения:  ")
        tar.extract(filename)
    elif selection == "2":
        filename = raw_input("введите имя файла для просмотра:  ")
        for tarinfo in tar:
            if tarinfo.name == filename:
                print "\n\
                Имя файла:\t\t", tarinfo.name, "\n\
                Размер:\t\t", tarinfo.size, "байт\n"
    elif selection == "3":
        print tar.list(verbose=True)
except:
    print "При выполнении программы возникла проблема!"
