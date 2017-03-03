# coding=utf-8
# 2015.12.14 windows版本
# 查找所有空格名字 或者 空格  # -*- coding: utf-8 -*-
# 想要去除的空格的话，可以使用 replace(" ","")
# 取得当前路径，所有 直接双击，或者cmd 当前目录下再执行python脚本
# 检查空格 和中文
import os
import sys
import os.path
import re
import sys
import os
import chardet
import codecs
import shutil

t = codecs.lookup("utf-8" )
print t
RootDir = os.getcwd() + "\src"
print RootDir
OutputDic = RootDir.replace("\src","\copy_src")
# os.makedirs(OutputDic)
if os.path.exists(OutputDic):
    print "remove file:"+OutputDic
    shutil.rmtree(OutputDic)

outputFile = os.getcwd()+"/res"+"/lang_yuenan.json"
if os.path.exists(outputFile):
    print "remove file:"+outputFile
    os.remove(outputFile)

yinPattern = re.compile('\"([^\"]*)\"')
zhPattern = re.compile(u'[\u4e00-\u9fa5]+')

g_match = []
encodeList = []

def start(rootDir):
    for f in os.listdir(rootDir):
        sourceF = os.path.join(rootDir, f)
        copyF = sourceF.replace("\src","\copy_src")
        curFilePath = os.path.dirname(sourceF)
        # 创建目录
        copyFilePath = curFilePath.replace("\src","\copy_src")
        if os.path.exists(copyFilePath) == False:
            # print "==create dir:"+copyFilePath
            os.mkdir(copyFilePath)
        if os.path.isfile(sourceF):
            a, b = os.path.splitext(f)  # 去除扩展名
            checkName(sourceF,copyF)
            print "==do:"+sourceF
        if os.path.isdir(sourceF):
            # checkName(f)
            start(sourceF)
    # print "g_match"
    # print g_match


# 文件数组
def checkName(f,copyF):
    fHandle = open(f,"r")             # 返回一个文件对象
    copyFile = open(copyF, "w+")
    line = fHandle.readline()             # 调用文件的 readline()方法
    copyFile.write(line)
    lineCount = 1
    while line:
        line = fHandle.readline()
        l_match = []
        lineCount = lineCount + 1
        old_charset = chardet.detect(line)['encoding']
        if old_charset != None:
            ff = line.decode(old_charset)
            if old_charset not in encodeList:
                encodeList.append(old_charset)
            # print "===old_charset:"+old_charset
            if (old_charset.find("ISO-8859-2") >= 0 or old_charset.find("windows-1252") >= 0) and ff.find("print") < 0:
                # print("copy1 line:"+str(lineCount))
                ff = line.decode('utf-8');
                # print ff
            if ff.find("print") < 0 and ff.find("--") < 0:
                yinmatch = yinPattern.findall(ff)
                if yinmatch:
                    for yinObj in yinmatch:
                        match = zhPattern.findall(yinObj)
                        matchStr = "".join(match)
                        for obj in match:
                            if yinObj not in l_match:
                                l_match.append(yinObj)
                                sourceStr = "\""+yinObj+"\""
                                replaceStr = "GET_LANGUAGE_STR(\""+yinObj+"\")"
                                if ff.find(replaceStr) < 0:
                                    ff = ff.replace(sourceStr, replaceStr)
                            if yinObj not in g_match:
                                g_match.append(yinObj)
                

                # print("copy1 line:"+str(lineCount))
                # print chardet.detect(line)
                copyFile.write(ff.encode("utf-8"))
            else:
                # print("copy2 line:"+str(lineCount))
                copyFile.write(line)
        else:
            # print("copy4 line:"+str(lineCount))
            copyFile.write(line)
    copyFile.close()


# 输出到txt
def outputJson():
    # f = open(RootDir+"/checkReslut.json", "w+")
    f = codecs.open(os.getcwd()+"/res"+"/lang_yuenan.json", "w+", "utf-8")
    f.write("{"+"\n")
    print len(g_match)
    for i in range(0, len(g_match)):
        if i<(len(g_match) - 1):
            f.write('"'+g_match[i] + '"'+':"",' + "\n")
        else:
            f.write('"'+g_match[i] + '"'+':""' + "\n")
    f.write("}")
    print("write end")
    f.close()

if __name__ == "__main__":
    name = []
    g_match = []
    start(RootDir)
    print("startWrite")
    outputJson()
    print encodeList
