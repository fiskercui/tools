import os

root = "..\\res"


class item:
	def __init__(self, name, value):
		self.name = name
		self.value = value

inverseList = []
def getSubDir(dir):
	for i in os.listdir(dir):
		subDir = os.path.join(dir,i)
		if not os.path.isfile(subDir):
			print subDir
			path =  dir[3:] +'\\'
			print i

			print len(inverseList)
			inverseList.append(item(path, i))
			getSubDir(subDir)


# itemObj = item("111", "22")
# print itemObj.name
getSubDir(root)
print(inverseList[229].value)

print(inverseList[230].value)


reverseList = inverseList[::-1]


print(reverseList[0].value)
print(reverseList[1].value)



s = "set curpath=%~dp0files\\\n"
s = s + "rd /s /q %curpath%\\src\\version\n"

s = s + "echo off\n"

s = s + "SET Obj_Length=%d\n"%(len(reverseList) +1)

itemIndex =  0
for itemObj in reverseList:
	print itemIndex 
	print itemObj.name 
	print itemObj.value
	s = s + "SET Obj[%d].Name=%s\nSET Obj[%d].Value=%s\n"%(itemIndex, itemObj.name, itemIndex, itemObj.value)
	itemIndex = itemIndex + 1


srcItem = item(".\\", "src")
s = s + "SET Obj[%d].Name=%s\nSET Obj[%d].Value=%s\n"%(itemIndex, srcItem.name, itemIndex, srcItem.value)

s = s + """set Obj_Index=0\n  	
:LoopStart\n
IF %Obj_Index% EQU %Obj_Length% GOTO :EOF\n\
  
set Obj_Current.Name=0\n
set Obj_Current.Value=0\n
  
FOR /F "usebackq delims==. tokens=1-3" %%I IN (`SET Obj[%Obj_Index%]`) DO ( 
  SET Obj_Current.%%J=%%K
)	\n
  
ECHO Name = %Obj_Current.Name%  \n
ECHO Value = %Obj_Current.Value% \n
ECHO .                         \n

cd %curpath%\n
\"D:\\Program Files\\WinZip\\WZZIP.exe\" %Obj_Current.Value%.pak %Obj_Current.Value% -r -P -ex -k -yt010101012007 \n

cd %curpath%\n
echo "delcurpath"%curpath%%Obj_Current.Name%%Obj_Current.Value%\n
rd /s /q %curpath%%Obj_Current.Name%%Obj_Current.Value%\n

SET /A Obj_Index=%Obj_Index% + 1\n
  
GOTO LoopStart\n
"""
print s


file_object = open('runzip_all.bat', 'w')
file_object.write(s)
file_object.close()