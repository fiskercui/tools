#coding=utf-8
#2015.12.14 windows版本
#查找所有空格名字 或者 空格  # -*- coding: utf-8 -*-
#想要去除的空格的话，可以使用 replace(" ","")
#取得当前路径，所有 直接双击，或者cmd 当前目录下再执行python脚本
#检查空格 和中文 
import os,sys
import xml.sax
import sys
import os
import chardet
import re
import codecs
import json
from xml.dom.minidom import parse
import xml.dom.minidom
reload(sys)
sys.setdefaultencoding('utf8') 
try: 
    import xml.etree.cElementTree as ET 
except ImportError: 
    import xml.etree.ElementTree as ET 


RootDir = os.getcwd() + "\cocosstudio\csd"

zhPattern = re.compile(u'[\u4e00-\u9fa5]+')

fileChineseDict = []


#统计中文
def start(rootDir):
    for f in os.listdir(rootDir):
        sourceF = os.path.join(rootDir,f)
        if os.path.isfile(sourceF):
            a, b = os.path.splitext(f) #去除扩展名
            checkDir(sourceF)
            # print("checkDir")
        if os.path.isdir(sourceF):
            # checkName(f)
            start(sourceF)
            # print("sourceF")
    print("end")
#文件数组
def file_extension(path): 
  return os.path.splitext(path)[1] 



def replaceSpace(uniString):
    print("replaceSpace type:%s"%(type(uniString)))

    spaceString = u"&#xA;"
    resUniString = u""
    index = 0
    lastIndex = 0
    for ch in uniString:
        # print "heheheh",type(ch)
        # print index , ord(ch),
        if ord(ch) == 10:
            print("ord is 10")
            # resUniString = uniString[lastIndex:index]
            resUniString = resUniString+uniString[lastIndex:index]
            # resUniStringList.append(resUniString)
            resUniString = resUniString + spaceString
            lastIndex = index+1
        index = index+1
    resUniString = resUniString + uniString[lastIndex:]
    print resUniString
    return resUniString


def revertSpace(uniString):
    index = uniString.find("&#xA;")
    uniString = uniString.replace("&#xA;", chr(0xa))
    return uniString


def enumChildren(childrenNode, parentName):
    global fileChineseDict
    # print("enumChildren",childrenNode)
    for child in childrenNode:
        # print("hehehehe",(child.attrib)["Name"])
        nodeName = None
        if parentName != None:
            nodeName = parentName + "/" + (child.attrib)["Name"]
        else:
            nodeName = (child.attrib)["Name"]
        if child.attrib.has_key("LabelText"):
            match = zhPattern.search( (child.attrib)["LabelText"]) 
            if match:
                print nodeName

                labelText = (child.attrib)["LabelText"]

                # print(len(labelText))
                # print len(labelText.encode('utf-8'))
                # print labelText.encode('utf-8')
                replaceSpace(labelText)
                # for ch in labelText:
                #     code = ord(ch)
                #     print "%x"%(code),
                # print("------------")
                # f = codecs.open(RootDir+"/" + (child.attrib)["Name"]+".xml","w+","utf-8")
                # f = open(RootDir+"/" + (child.attrib)["Name"]+".xml","w+")
                # f.write(labelText)
                # f.close()

                # charset = chardet.detect(labelText)['encoding']                
                # charset = chardet.detect(u"%s"(labelText))['encoding']


                # labelText = labelText.decode(charset).encode('ascii', 'ignore')
                # print labelText
                dictitem = {"node":nodeName, "text": replaceSpace(labelText)}
                fileChineseDict.append(dictitem)

        for nodeData in child.findall('Children'):
            enumChildren(nodeData,nodeName)    

def checkDir(fileName):
    global fileChineseDict

    # print("file_extension", file_extension(fileName))

    if file_extension(fileName) == ".csd":
        # print("checkDir", fileName)
        try: 
            # file_xml = open(fileName,"r").read()
            # charset = chardet.detect(file_xml)['encoding']
            # print charset
            # file_xml = file_xml.decode(charset).encode("utf-8")
            tree = ET.parse(fileName)     #打开xml文档 
            root = tree.getroot()         #获得root节点  
        except Exception, e: 
            print "Error:cannot parse file:." + fileName
            return

        for child in root:
            # print("tag GameFile root")
            if child.tag == "Content":
                # print("tag content")
                for subConent in child:
                    # print("tag content")
                    for subsubContent in subConent:
                        for child in subsubContent:
                            # print("child", child.tag)
                            if child.tag == "Children":
                                enumChildren(child, None)
        if len(fileChineseDict) != 0:
            fileName = fileName[len(RootDir)+1:]
            fileDictItem = {"files":fileName ,"nodeDict":fileChineseDict}
            Chinese.append(fileDictItem)
            fileChineseDict = []

    # if file_extension(fileName) == ".csd":
    #     file_xml = open(fileName,"r").read()
    #     charset = chardet.detect(file_xml)['encoding']
    #     file_xml = file_xml.decode(charset).encode("utf-8")
    #     DOMTree = xml.dom.minidom.parseString(file_xml)
    #     resource_root = DOMTree.documentElement
    #     # print(resource_root)
    #     gamefile_root = resource_root.getElementsByTagName("Content")
    #     # print(gamefile_root)
    #     for content_root in gamefile_root:
    #         content_content_root = content_root.getElementsByTagName("Content")
    #         for a_content_content_root in content_content_root:
    #             objectDataNodes = a_content_content_root.getElementsByTagName("ObjectData")
    #             for objectDataObject in objectDataNodes:                    
    #                 # print("()()()(",objectDataObject.getAttribute("Name"),objectDataObject.getAttribute("ActionTag"))
    #                 # print("**********8", a_content_content_root.nodeName, objectDataObject.nodeName)
    #                 enumChildren(objectDataObject.getElementsByTagName("Children"), objectDataObject.getAttribute("Name"),fileName)

    # #
    # fHandle = open(f)             # 返回一个文件对象  
    # content = ""
    # line = fHandle.readline()             # 调用文件的 readline()方法  
    # while line:  
    #     line = fHandle.readline()  
    #     content = content + line
    # print(f)
    # old_charset =  chardet.detect(content)['encoding']
    # print("checkName:" + f + "\t code:" + old_charset)
    # ff = content.decode(old_charset)
    # match = zhPattern.search(ff) #匹配中文
    # if match:
    #     # print (ff)
    #     print("***********************************8")
    #     Chinese.append(f)
    # for i in f:
    #        if i.isspace(): #检查空格
    #            # print f
    #            name.append(f)


def parseLanguageXml():
    # global LanguageNode
    try: 
        tree = ET.parse(RootDir+"/language_csd.xml")     #打开xml文档 
        root = tree.getroot()         #获得root节点  
    except Exception, e: 
        print "Error:cannot parse file:.xml" 
        sys.exit(1) 
    for child in root.findall("file"):
        print "============"+child.tag 
        print child.attrib["files"]
        print type(child)
    # print LanguageNode

#输出到txt
def writeXml():

    # f.write("\nChinese :\n")
    # for i in range(0, len(Chinese)):
    #     f.write("\"" + Chinese[i] + "\"\n")  
    # print("write end")
    # print(Chinese)
    # cs = json.dumps(Chinese, indent =4)
    # f.write("[\n")
    # for i in range(0, len(Chinese)):
    #     f.write("\t{\n")
    #     f.write("\t\t\"files\":\"" + Chinese[i]["files"] + "\",\n")  
    #     f.write("\t\t\"nodeDict\":\t[\n")
    #     for j in range(0, len(Chinese[i]["nodeDict"])):
    #         f.write("\t\t\t{\n")  
    #         f.write("\t\t\t\t\"node\":\"" + Chinese[i]["nodeDict"][j]["node"] + "\",\n")  
    #         f.write("\t\t\t\t\"text\":\"" + Chinese[i]["nodeDict"][j]["text"] + "\"\n")  
    #         f.write("\t\t\t},\n")  

    #     f.write("\t\t],\n")
    #     f.write("\t},\n")
    # f.write("]\n")
    # f.write(cs)

    dom = None
    tree = None
    if not os.path.exists(RootDir+"/language_csd.xml"):
        impl = xml.dom.minidom.getDOMImplementation()
        dom = impl.createDocument(None, 'GameFile', None)
        root = dom.documentElement  

        # root = ET.Element("GameFile")
        # tree = ET.ElementTree(root)
    else:
        try: 
            # dom = xml.dom.minidom.parse(RootDir+"/language_csd.xml")
            # root = dom.documentElement  
            tree = ET.parse(RootDir+"/language_csd.xml")     #打开xml文档 
            root = tree.getroot()         #获得root节点  
        except Exception, e: 
            print "Error:cannot parse file:. language_csd"
            sys.exit(1)

    def indent(elem, level=0):
            i = "\n" + level*"  "
            if len(elem):
                    if not elem.text or not elem.text.strip():
                            elem.text = i + "  "
                    if not elem.tail or not elem.tail.strip():
                            elem.tail = i
                    for elem in elem:
                            indent(elem, level+1)
                    if not elem.tail or not elem.tail.strip():
                            elem.tail = i
            else:
                    if level and (not elem.tail or not elem.tail.strip()):
                            elem.tail = i
    def getFileNodeOrCreate(fileName):
        for child in root.getiterator("file"):
            if child.attrib["files"] == fileName:
                return child
        fileE = ET.SubElement(root, "file")
        fileE.attrib["files"] = fileName
        fileE.tail = "\n"
        fileE.text = "\n\t"
        # indent(fileE, 1)
            # if child.getAttribute("files") == fileName:
            #     return child        
        # fileE = dom.createElement('file')
        # fileE.setAttribute("files", fileName)
        # root.appendChild(fileE)
        return fileE

    def getNodeByFileE(fileElement, nodeName):
        for child in fileElement.getiterator("Node"):
            # if child.getAttribute("NodeName") == nodeName:
            #     return child
            if child.attrib["NodeName"] == nodeName:
                return child

        print ("creat node ")
        # nodeE = dom.createElement('Node')
        # nodeE.setAttribute("NodeName", Chinese[i]["nodeDict"][j]["node"])
        # fileElement.appendChild(nodeE)
        nodeE = ET.SubElement(fileElement, 'Node') 
        nodeE.attrib["NodeName"] = nodeName
        nodeE.tail = "\n\t"

        # indent(nodeE, 2)

        return nodeE



    print ("len Chinese", len(Chinese))
    for i in range(0, len(Chinese)):
        print("=============",Chinese[i]["files"])
        fileE = getFileNodeOrCreate(Chinese[i]["files"])


        # fileE = dom.createElement('file')
        # fileE.setAttribute("files", Chinese[i]["files"])
        # root.appendChild(fileE)
        for j in range(0, len(Chinese[i]["nodeDict"])):
            nodeE = getNodeByFileE(fileE, Chinese[i]["nodeDict"][j]["node"])
            # nodeE.setAttribute("LabelText", Chinese[i]["nodeDict"][j]["text"])
            nodeE.attrib["LabelText"] = Chinese[i]["nodeDict"][j]["text"]

            # nodeE = getNodeByFileE(fileE, Chinese[i]["nodeDict"][j]["node"])


    # f = codecs.open(RootDir+"/language_csd.xml","w+","utf-8")
    # dom.writexml(f, addindent='  ',encoding='utf-8')
    # f.close()

    # xmls =  xml.dom.minidom.parseString(
    #             ET.tostring(
    #               tree.getroot(),
    #               'utf-8')).toprettyxml(encoding = "utf-8")


    # f = codecs.open(RootDir+"/language_csd.xml","w+","utf-8")
    # f.write( xmls)
    # f.close()

    tree.write(RootDir+"/language_csd.xml", encoding="UTF-8",xml_declaration=True)
# 
def readLangXml():
    fileName = RootDir+"/language_csd.xml"
    file_xml = open(fileName,"r").read()
    charset = chardet.detect(file_xml)['encoding']
    file_xml = file_xml.decode(charset).encode("utf-8")
    DOMTree = xml.dom.minidom.parseString(file_xml)

    resource_root = DOMTree.documentElement
    # print(resource_root)
    gamefile_root = resource_root.getElementsByTagName("file")
    print gamefile_root
    for gameFile_Object in gamefile_root:
        print("filesName"+gameFile_Object.getAttribute("files"))
        nodeElements = gameFile_Object.getElementsByTagName("Node")
        for node in nodeElements:
            print("node name:" + node.getAttribute("NodeName") + "LabelText:" + node.getAttribute("LabelText"))


def outputJson():
    fileName = RootDir+"/language_csd.xml"
    file_xml = open(fileName,"r").read()
    charset = chardet.detect(file_xml)['encoding']
    file_xml = file_xml.decode(charset).encode("utf-8")
    DOMTree = xml.dom.minidom.parseString(file_xml)
    resource_root = DOMTree.documentElement

    outputDict = {}
    # print(resource_root)
    gamefile_root = resource_root.getElementsByTagName("file")
    print gamefile_root
    for gameFile_Object in gamefile_root:
        print("filesName"+gameFile_Object.getAttribute("files"))
        nodeElements = gameFile_Object.getElementsByTagName("Node")
        for node in nodeElements:
            outputDict[node.getAttribute("LabelText")] = 1

    fileName = RootDir+"/language_csd.lua"
    # for index,app_id in enumerate(outputDict):
    #     print index, app_id
    # f = codecs.open(RootDir+"/language_csd.lua","w+","utf-8")
    # f.write("local languageStr = {\n")

    # for (k,v) in outputDict.items():
    #     # print v
    #     f.write("[\"" + k + "\"] = \"\",\n")

    # f.write("\n}\n")
    # f.write("return languageStr\n")
    f = codecs.open(RootDir+"/language_csd.json","w+","utf-8")
    f.write("{\n")
    writeIndex = 0
    for (k,v) in outputDict.items():
        writeIndex = writeIndex + 1
        if writeIndex == len(outputDict):
            f.write("\"" + k  + "\"" + ":\"\"" )
        else:
            f.write("\"" + k  + "\"" + ":\"\",\n" )
    f.write("\n}\n")


LanguageJson ={}

def changeNodeChild(Children, parentName, fileName, depth):
    global LanguageJson
    # print("parentName", parentName)
    # print("fileName", fileName)
    # if len(Children) >0:
    #     print("lenChildren", len(Children))
    index = 0
    # print("startIndex:%d"%(index))
    # print("depth:%d lenChildren:%d"%(depth, len(Children)))

    gap = ""
    for x in xrange(0,depth):
        gap = gap + "    "
        # print("heheheh:%d"%(x))
        # print(gap + "depth")
        # print("%sdepth gap"%(gap))

    for child in Children:
        index = index + 1
        # print("childtype", type(child))
        print("*****8")
        print(child.nodeValue)
        print(child.nodeType)
        print(child.nodeName)

        # AbstractNodes = child.getElementsByTagName("AbstractNodeData")
        # # print("%sstartIndex:%d %d"%(gap, index, len(AbstractNodes)))

        # subIndex = 0
        # for bstractNode in AbstractNodes:
        #     # print("%ssubIndex:%d"%(gap, subIndex))
        #     subIndex = subIndex + 1
        #     match = zhPattern.search(bstractNode.getAttribute("LabelText")) 
        #     nodeName = parentName + "/" + bstractNode.getAttribute("Name")    
        #     print("%snodeName:%s"%( gap, nodeName) )
        #     if match:
        #         # dictitem = {"node":nodeName, "text":bstractNode.getAttribute("LabelText")}
        #         # print("LabelText", bstractNode.getAttribute("LabelText"))
        #         # print("hehe1")
        #         # print(LanguageJson)
        #         # print("hehe2")
        #         # print(LanguageJson[bstractNode.getAttribute("LabelText")])
        #         if LanguageJson.has_key(bstractNode.getAttribute("LabelText")):
        #             # print("OKOKOKOKOKO", nodeName)
        #             pass
        #         # pass
        #         # fileChineseDict.append(dictitem)
        #     # print("type", type(bstractNode.getElementsByTagName("Children")))
        #     # changeNodeChild(bstractNode.getElementsByTagName("Children"), nodeName,fileName,depth+1)


unique_id  = 1
def walkData(root_node, level, result_list):  
    global unique_id  
    temp_list =[unique_id, level, root_node.tag, root_node.attrib]  
    result_list.append(temp_list)  
    unique_id += 1  
      
    #遍历每个子节点  
    children_node = root_node.getchildren()  
    if len(children_node) == 0:  

        return  
    for child in children_node:  
        walkData(child, level + 1, result_list)  
    return  

def changeNodeChildren(childrenNode, parentName, LangNodeDict):
    # print("changeChildrenNode")
    for child in childrenNode:
        nodeName = None
        if parentName != None:
            nodeName = parentName + "/" + (child.attrib)["Name"]
        else:
            nodeName = (child.attrib)["Name"]
        print nodeName



        # print ("*******---------")
        if LangNodeDict.has_key(nodeName):
            if child.attrib.has_key("LabelText"):
                labelText = (child.attrib)["LabelText"]
                # for ch in labelText:
                #     code = ord(ch)
                #     print "%x"%(code),
                # print 
                # for ch in labelText.encode("string_escape"):
                #     code = ord(ch)
                #     print code
                # print (chardet.detect((child.attrib)["LabelText"])["encoding"])

                # labelText = (child.attrib)["LabelText"]
                # labalSpaceText =  replaceSpace(labelText)
                # match = zhPattern.search( labalSpaceText) 
                # if match:

                originName = LangNodeDict[nodeName]
                # print("match ok:%s"%(nodeName))
                if LanguageJson.has_key(originName):
                    print("——————————————————————————————————————")

                    # for ch in LanguageJson[originName]:
                    #     print ord(ch)

                    restring = revertSpace(LanguageJson[originName])
                    print((LanguageJson[originName]).encode("utf-8"))
                    (child.attrib)["LabelText"] = restring
                    print((child.attrib)["LabelText"] )

        for nodeData in child.findall('Children'):
            changeNodeChildren(nodeData,nodeName,LangNodeDict)

def changeLangeuage(fileName, langJson):
    global fileChineseDict

    print("fileName", fileName)

    subFileName = fileName[len(RootDir)+1:]
    if not LanguageNode.has_key(subFileName):
        return 
    print("changeLangeuage", fileName)
    # print("file_extension", file_extension(fileName))
    if file_extension(fileName) == ".csd":
        try: 
            tree = ET.parse(fileName)     #打开xml文档 
            root = tree.getroot()         #获得root节点  
        except Exception, e: 
            print "Error:cannot parse file:." + fileName
            sys.exit(1) 


        for child in root:
            # print("iter root")
            if child.tag == "Content":
                # print("tag content")
                for subConent in child:
                    # print("tag content")
                    for subsubContent in subConent:
                        for child in subsubContent:
                            # print("child", child.tag)
                            if child.tag == "Children":
                                changeNodeChildren(child, None, LanguageNode[subFileName])
                      
        tree.write(fileName, encoding="UTF-8",xml_declaration=False)
                        # print subsubContent.tag
        # result_list = [] 
        # level = 1
        # walkData(root, level, result_list)
        # for x in result_list:  
        #     print x  
        # pass


def parseLanguageNode():
    global LanguageNode
    try: 
        tree = ET.parse(RootDir+"/language_csd.xml")     #打开xml文档 
        root = tree.getroot()         #获得root节点  
    except Exception, e: 
        print "Error:cannot parse file:." + fileName
        sys.exit(1) 
    for child in root:
        # print (child.attrib)["files"]
        fileName = (child.attrib)["files"]
        # print fileName
        LanguageNode[fileName] = {}

        for sub in child:
            # print sub.attrib["LabelText"]
            # print sub.attrib["NodeName"]
            LanguageNode[fileName][sub.attrib["NodeName"]] = sub.attrib["LabelText"]

    # print LanguageNode


def writeLanguageCsd(rootDir, langJson):
    f=file(langJson)
    global LanguageJson
    LanguageJson=json.load(f)
    # print(LanguageJson)
    f.close()
    # dumpLangjson()

    for f in os.listdir(rootDir):
        sourceF = os.path.join(rootDir,f)
        if os.path.isfile(sourceF):
            changeLangeuage(sourceF, langJson)
        if os.path.isdir(sourceF):
            writeLanguageCsd(sourceF,langJson)


def dumpLangjson():
    for(k,v) in LanguageJson.items():
        print k,v 

if __name__=="__main__":
    name = []
    Chinese = []

    LanguageJson = {}
    LanguageNode = {}

    print(RootDir)

    # csd生成 node -chinese 文件
    # start(RootDir)
    # writeXml()

    #输出json文件
    # outputJson()

    #改写csd文件
    parseLanguageNode()
    writeLanguageCsd(RootDir, RootDir+"/language_csd.json")