#coding=utf-8
#2015.12.14 windows版本
#查找所有空格名字 或者 空格  # -*- coding: utf-8 -*-
#想要去除的空格的话，可以使用 replace(" ","")
#取得当前路径，所有 直接双击，或者cmd 当前目录下再执行python脚本
#检查空格 和中文 
import os,sys
import os.path
import re
import sys
import os
import chardet

RootDir = os.getcwd() + "\cocosstudio\csd"
print RootDir
print "123"
zhPattern = re.compile(u'[\u4e00-\u9fa5]+')

def start(rootDir):
    for f in os.listdir(rootDir):
        sourceF = os.path.join(rootDir,f)
        if os.path.isfile(sourceF):
            a, b = os.path.splitext(f) #去除扩展名
            checkName(sourceF)
        if os.path.isdir(sourceF):
            # checkName(f)
            start(sourceF)

#文件数组
"""
注意这地方的编码格式。windows文件名字的编码格式为gbk
"""
def checkName(f):
    #
    fHandle = open(f)             # 返回一个文件对象  
    content = ""
    line = fHandle.readline()             # 调用文件的 readline()方法  
    while line:  
        line = fHandle.readline()  
        content = content + line
    print(f)
    old_charset =  chardet.detect(content)['encoding']
    print("checkName:" + f + "\t code:" + old_charset)
    ff = content.decode(old_charset)
    # ff = f.decode('gbk')
    # print(ff)
    match = zhPattern.search(ff) #匹配中文
    if match:
        # print (ff)
        print("***********************************8")
        Chinese.append(f)
    for i in f:
           if i.isspace(): #检查空格
               # print f
               name.append(f)

#输出到txt
def wirte():
    f = open(RootDir+"/checkReslut.txt", "w+")
    f.write("space :\n")
    print("start write name")
    for i in range(0, len(name)):
        f.write(name[i] + "\n")

    print("start write Chinese")
    f.write("\nChinese :\n")
    for i in range(0, len(Chinese)):
        f.write(Chinese[i] + "\n")  

    print("write end")
    f.close()

if __name__=="__main__":
    name = []
    Chinese = []
    start(RootDir)
    print("startWrite")
    wirte()

