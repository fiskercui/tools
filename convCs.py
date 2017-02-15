#!/usr/bin/python

import xml.sax
import sys
import os
import chardet

from xml.dom.minidom import parse
import xml.dom.minidom


def get_charset(s):
	return chardet.detect(s)['encoding']

def init_resource_root():
	resource_root = None
	fileName = "./xml/resource-utf-8.xml"
	file_xml = open(fileName,"r").read()
	charset = get_charset(file_xml)
	file_xml = file_xml.decode(charset).encode("utf-8")
	DOMTree = xml.dom.minidom.parseString(file_xml)
	resource_root = DOMTree.documentElement
	return resource_root


def initConst(resource_root):
	itemList = resource_root.getElementsByTagName("macro")

	content = "class macros \n{\n" 
	for item in itemList:
		print("name:" + item.getAttribute("name"))
		print("value:" + item.getAttribute("value"))
		content = content + "public const int " + item.getAttribute("name") + " = " + item.getAttribute("value") + ";\n";
 	
 	content = content + "\n}\n"

 	content = content +  "public class TableHeadInfo {} \n public class AttributeInfo {}\n"
	file_object = open('./property/const.cs', 'w')
	file_object.write(content)
	file_object.close()




def getResourceRootInfo(root, propertyName):
	tableProperties = root.getElementsByTagName("struct")
	for table in tableProperties:
		# print("table:" + table.getAttribute("name"))
		if propertyName == table.getAttribute("name"):
			return table



def init_convert_root():
	fileName = "./convlist-utf-8.xml"
	file_xml = open(fileName,"r").read()
	charset = get_charset(file_xml)
	file_xml = file_xml.decode(charset).encode("utf-8")
	DOMTree = xml.dom.minidom.parseString(file_xml)
	resource_root = DOMTree.documentElement
	return resource_root



if ( __name__ == "__main__"):
	root = 	init_resource_root()
	print(type(root))
	initConst(root)

	convert_root = init_convert_root()
	conver_tree_root = convert_root.getElementsByTagName("ConvTree")
	for tree_root in conver_tree_root:
		conver_comm_node = tree_root.getElementsByTagName("CommNode")
		for comm_node in conver_comm_node:
			resNodes = comm_node.getElementsByTagName("ResNode")
			for node in resNodes:
				print("node:" + node.getAttribute("Meta"))

				propertyInfo = getResourceRootInfo(root, node.getAttribute("Meta"))
				s = "using System.Collections.Generic; \n public class "  + node.getAttribute("Meta") + "Property" + "\n{\n"
				s = s + "\tpublic TableHeadInfo TResHeadAll;\n"
				s = s + "\tpublic List<" + node.getAttribute("Meta") + "Object" + "> "  + node.getAttribute("Meta") + "{ get; set;}\n}\n";



				s = s + "public class " + node.getAttribute("Meta") + "Object" +  "{\n";
				s = s + "\t public AttributeInfo @attributes;\n"

				for entry in propertyInfo.getElementsByTagName("entry"):
					print("entryName:" + entry.getAttribute("name") + " type:" + entry.getAttribute("type") )
					if entry.getAttribute("type")  == "int":
						if entry.getAttribute("name") == "default":
							s = s + "\t public int _" + entry.getAttribute("name") +  " { get; set;}\n";
						else:
							s = s + "\t public int " + entry.getAttribute("name") + "{ get; set;}\n";
					elif entry.getAttribute("type") == "string":
						if entry.getAttribute("name") == "default":
							s = s + "\t public string _" + entry.getAttribute("name") + "{ get; set;}\n";
						else:
							s = s + "\t public string " + entry.getAttribute("name") + "{ get; set;}\n";

				s = s+"}\n"
				file_object = open('./property/' + node.getAttribute("Meta") + 'Property.cs', 'w')
				file_object.write(s)
				file_object.close()
	# root = 	init_resource_root()
	# itemList = root.getElementsByTagName("macro")
	# for item in itemList:
	# 	print("name:" + item.getAttribute("name"))
	# 	print("value:" + item.getAttribute("value"))
	# 	# print(type(item))


	# propertyInfo = getResourceRootInfo(root, "CardProp")
	# for entry in propertyInfo.getElementsByTagName("entry"):
	# 	print("entryName:" + entry.getAttribute("name"))

	# 	print("type:" + entry.getAttribute("type"))