import os, sys
import re

# sys.argv[1] : project.pbxproj path
# sys.argv[2] : meituan_login_enable
# update meituan_login_enable in project.pbxproj. this meituan_login_enable is define.

file_path = sys.argv[1]
meituan_login_enable = int(sys.argv[2])
pro_file = open(file_path,"r+")

# read file conten to instance
file_content = ''
for line in pro_file:
	file_content = file_content + line

# find builds uuid
builds = []
start_point = file_content.find('/* Begin XCConfigurationList section */')
end_point = len(file_content)
sub_str = file_content[start_point : end_point]
start_point = sub_str.find('/* Build configuration list for PBXNativeTarget "demo" */ ')
end_point = len(sub_str)
sub_str = sub_str[start_point : end_point]
start_point = sub_str.find('buildConfigurations')
end_point = len(sub_str)
sub_str = sub_str[start_point : end_point]
start_point = sub_str.find('(') + 2
end_point = sub_str.find(')')
sub_str = sub_str[start_point : end_point]
start_point = 0
end_point = sub_str.rfind('*/') + 2
sub_str = sub_str[start_point : end_point]
split_subs = sub_str.split('\n')
for item in split_subs:
	item = re.sub(r'\t','',item)
	item = item[0 : item.find(' ')]
	builds.append(item)

if meituan_login_enable >= 1:
	#add MEITUAN_LOGIN_ENABLE=1 to config
	for item in builds:
		start_point = file_content.find(item)
		end_point = len(file_content)
		sub_str = file_content[start_point : end_point]
		start_point = sub_str.find('buildSettings')
		end_point = sub_str.find('};') + 2
		sub_str = sub_str[start_point : end_point]
		start_point = sub_str.find('GCC_PREPROCESSOR_DEFINITIONS')
		if start_point >= 0:
			end_point = len(sub_str)
			sub_str = sub_str[start_point : end_point]
			file_point = file_content.find(sub_str)
			tstr = sub_str[sub_str.find('\t') : sub_str.find('\"')]
			start_point = sub_str.find('(')
			end_point = sub_str.find(');')
			sub_str = sub_str[start_point : end_point]
			start_point = sub_str.find('MEITUAN_LOGIN_ENABLE')
			file_point = file_point + len("GCC_PREPROCESSOR_DEFINITIONS = (\n") + len(tstr)
			if start_point < 0:
				file_sub1 = file_content[0 : file_point]
				file_sub2 = file_content[file_point :len(file_content)]
				file_content = file_sub1 + "\"MEITUAN_LOGIN_ENABLE=1\",\n" + tstr + file_sub2
		else :
			file_point = file_content.find(sub_str)
			len1 = sub_str.find('\n') + 1
			file_point = file_point + len1
			sub_str = sub_str[len1 : sub_str.find(';')]
			tstr = sub_str[0 : sub_str.rfind('\t') + 1]
			file_point = file_point + len(tstr)
			file_sub1 = file_content[0 : file_point]
			file_sub2 = file_content[file_point :len(file_content)]
			file_content = file_sub1 + 'GCC_PREPROCESSOR_DEFINITIONS = (\n' + tstr + '\t' + "\"$(inherited)\",\n" + tstr + '\t' + "\"COCOAPODS=1\",\n" + tstr + '\t' + "\"MEITUAN_LOGIN_ENABLE=1\",\n" + tstr + ");\n" + tstr + file_sub2 
else:
	#delect MEITUAN_LOGIN_ENABLE in builds
	for x in xrange(1,len(builds) + 1):
		start_point = file_content.find('MEITUAN_LOGIN_ENABLE')
		if start_point >= 0:
			file_sub1 = file_content[0 : start_point]
			file_sub2 = file_content[start_point : len(file_content)]
			file_sub1 = file_sub1[0 : file_sub1.rfind('\n') + 1]
			file_sub2 = file_sub2[file_sub2.find('\n') + 1 : len(file_sub2)]
			file_content = file_sub1 + file_sub2

# fresh	project.pbxproj 
try:
	pro_file.seek(0)
	pro_file.truncate()
	pro_file.write(file_content)
	pro_file.close()
except Exception, e:
	print e
	pro_file.close()
