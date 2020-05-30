# -*- coding:utf-8 -*-
import sqlite3


#-------------------------------ci------------------------------------------------------------#

def ci_poem_opendb():
    conn = sqlite3.connect("poem_date.db")
    cur = conn.execute("""create table if not exists ci_info(id integer PRIMARY KEY autoincrement,poemName varchar(30),author varchar(30),content text)""")
    return cur,conn

#根据诗句模糊查找诗整体信息
def ci_poem_selectParagraphs(paragraphs):
        hel = ci_poem_opendb()
        cur = hel[1].cursor()
        cur.execute("select * from ci_info where content like '%%%s%%'" %paragraphs)
        res = cur.fetchall()
        return res
        cur.close()
        

#根据诗句模糊查找诗整体信息
def ci_poem_selectParagraphs(strs):
        hel = ci_poem_opendb()
        cur = hel[1].cursor()
        cur.execute("select * from ci_info where poemName like '%%%s%%' or author like '%%%s%%' or content like '%%%s%%'" %(strs,strs,strs))
        res = cur.fetchall()
        return res
        cur.close()

#-------------------------------tang---------------------------------------------------------------#
def tang_poem_opendb():
    conn = sqlite3.connect("poem_date.db")
    cur = conn.execute("""create table if not exists tang_poem_info(id integer PRIMARY KEY autoincrement,poemName varchar(30),author varchar(30),strains varchar(256),paragraphs varchar(256))""")
    return cur,conn
        
#根据诗句模糊查找诗整体信息
def tang_poem_selectParagraphs(paragraphs):
        hel = tang_poem_opendb()
        cur = hel[1].cursor()
        cur.execute("select * from tang_poem_info where paragraphs like '%%%s%%'" %paragraphs)
        res = cur.fetchall()
        return res
        cur.close()
        
#根据诗句模糊查找诗整体信息
def tang_poem_selectParagraphss(strs):
        hel = tang_poem_opendb()
        cur = hel[1].cursor()
        cur.execute("select * from tang_poem_info where poemName like '%%%s%%' or author like '%%%s%%' or paragraphs like '%%%s%%'" %(strs,strs,strs))
        res = cur.fetchall()
        return res
        cur.close()

#------------------------------------song----------------------------------------------------------#

def song_poem_opendb():
    conn = sqlite3.connect("poem_date.db")
    cur = conn.execute("""create table if not exists song_poem_info(id integer PRIMARY KEY autoincrement,poemName varchar(30),author varchar(30),strains varchar(256),paragraphs varchar(256))""")
    return cur,conn
        
#根据诗句模糊查找诗整体信息
def song_poem_selectParagraphs(paragraphs):
        hel = song_poem_opendb()
        cur = hel[1].cursor()
        cur.execute("select * from song_poem_info where paragraphs like '%%%s%%'" %paragraphs)
        res = cur.fetchall()
        return res
        cur.close()

#根据诗句模糊查找诗整体信息
def song_poem_selectParagraphss(strs):
        hel = song_poem_opendb()
        cur = hel[1].cursor()
        cur.execute("select * from song_poem_info where poemName like '%%%s%%' or author like '%%%s%%' or paragraphs like '%%%s%%'" %(strs,strs,strs))
        res = cur.fetchall()
        return res
        cur.close()