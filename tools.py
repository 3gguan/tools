#coding=utf-8
import os
import re


content_filter_list = r'create *or *replace *trigger.*?/|create *trigger.*?/'

file_filter_list = r'.*\.sql'
file_filter_handle = None

#通过正则表达式获取需要的内容块
def get_contents(file_full_name):
    f = open(file_full_name, 'r')
    s = f.read()
    rec = re.compile(content_filter_list, re.I|re.S)
    return rec.findall(s)

#输出内容到文件中
def write_contents(file_full_name, list):
    if len(list) > 0:
        f = open(file_full_name, 'w')
        s = ''
        for tmp in list:
            s += tmp
            s += '\n\n'
        f.write(s)

#提取文件中内容并写入另一个文件
def get_contents_to_file(file_list):
    for file in file_list:
        base_name = os.path.basename(file)
        contents = get_contents(file)
        write_contents('filter_' + base_name, contents)

#使用ffmpeg批量提取视频中的音频
def video_to_audio(file_list):
    for file in file_list:
        base_name = os.path.basename(file).split('.')[0]
        cmd = 'ffmpeg -i \"' + file + '\" -vn -acodec copy \"' + base_name + '.m4a\"'
        ret = os.system(cmd)
        if ret != 0:
            print(file)


#文件名过滤器初始化
def file_filter_init():
    if len(file_filter_list) > 0:
        return re.compile(file_filter_list)
    else:
        return None

#文件名是否匹配
def file_match(file_full_name):
    if file_filter_handle is not None:
        if file_filter_handle.match(file_full_name) is not None:
            return True
        else:
            return False
    else:
        return True

#递归获取匹配的文件名，结果带路径
def get_files_recursion(dirname):
    file_list = []
    files = os.listdir(dirname)
    for file in files:
        file_full_name = os.path.join(dirname, file)
        if os.path.isdir(file_full_name):
            sub_files = get_files_recursion(file_full_name)
            if len(sub_files) > 0:
                file_list.extend(sub_files)
        elif os.path.isfile(file_full_name):
            if file_match(file_full_name):
                file_list.append(file_full_name)

    return file_list


#获取文件名
file_filter_handle = file_filter_init()
files = get_files_recursion('.')
print(len(files))

#ffmpeg提取音频
#video_to_audio(files)

#匹配文件内容并写入另一个文件
#get_contents_to_file(files)



