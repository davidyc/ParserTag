from tkinter import * #графическая библеотека
from tkinter import messagebox
import requests #работы с сайтами
import re #регулярные вырожениия
import pyodbc #библеотека подключения а бд

# строчка подключения 
connectstring = 'DRIVER={SQL Server};SERVER=COMPUTER\SQLEXPRESS;DATABASE=CountTags;Trusted_Connection=yes;'

'''Подключения к БД'''
def ConnectToDataBase():
    cnxn = pyodbc.connect(connectstring)
    return cnxn

'''Добавление к записей бд
url - адресс сайта 
dic - словарь с тегами и их кол-вом
'''
def AddData(url, dic):
    cursor = ConnectToDataBase()     
    cursor.execute("insert into SaitNameTable(saitname) values('{0}')".format(url))
    coutnSait = cursor.execute("select MAX(id) from SaitNameTable").fetchone() 
    cursor.commit()       

    for item in dic:
         cursor.execute("insert into TagsNameAndCount(saitnameID,tag,counttags) values('{0}','{1}',{2})"
         .format(coutnSait[0], item[0], item[1]))
         cursor.commit()   
    
'''Поиск тего на страницы
text - код веб старницы
return - возращает множество с тагами'''
def SearchTeg(text):
     res = re.findall(r"<\w+", text)
     newres = set(res)    
     return newres

'''Обрабатывает страницу разбирает по тегам изаписывает их в базу
text - код веб страницы 
url - адрес сайта'''
def CountDiv(text, url): 
    listOfTags = SearchTeg(text)
    dic = []
    for item in listOfTags:
          res = re.findall(item, text)
          count = res.count(item)
          dic.append((item[1:], count))
    AddData(url, dic) 

'''Вызов функции обратного выхова
url - адрес сайта'''
def callback(url):
	r = requests.get(url)
	CountDiv(r.text, url)
     #messagebox.showinfo("Процесс закончен", "Операция запись в базу закончиена")



# блок вызова графических интерфейсов 
root = Tk()
root.title("Web tags  count")
l = Label(root, text="url")
textbox = Entry(width=80)
btn = Button(root, text="OK", height=2, width=15, command=lambda: callback(textbox.get()))

l.grid(row=0, column=0)
textbox.grid(row=0, column=1)
btn.grid(row=0, column=2)

root.mainloop()