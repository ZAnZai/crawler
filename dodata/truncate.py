#!/usr/bin/env python2.7
#coding=utf-8
#the raw copy from stackoverflow
#author@alingse
#2016.08.1

from __future__ import with_statement

import argparse
import os

def bigger(x,y):
    if x > y:
        return x
    raise Exception("the input must bigger than "+str(y))

#unsinged int
uint = lambda x:bigger(int(x),-1)
#positive integers
pint = lambda x:bigger(int(x),0)

def truncate_tail(file,number,size=10240,nothalf=False,test=False):
    with open(file,'r+b') as f:
        #seek END
        f.seek(0, os.SEEK_END)
        end = f.tell()
        _end = end
        _number = number

        #only patch the last line
        last = True
        while end >0 and number > -1:
            if end < size:
                size = end

            #seek and read data block
            f.seek(-1*size, os.SEEK_CUR)
            data = f.read(size)
        
            #seek back after every time read -- read把指针移走了了
            end = end - size
            f.seek(-1*size, os.SEEK_CUR)
            
            lines = data.split('\n')
            #'wwww\nsfds\nss\nwww' --> ['wwww','sfds','ss','www']
            #通常lines最后一个半行应该算到上一次读的那一行里面,所以应该去掉
            #但是文件末尾这一个半行也算做一行,因此这里有一个patch
            if last is False:
                lines.pop()
            else:
                #last line is half line
                if nothalf and data[-1] != '\n':
                    print('last line if half line ! (not end with \'\n\' )')
                    return 2

                if data[-1] == '\n':
                    lines.pop()
                last = False

            count = len(lines)
            if number > count:
                number = number - count
            else:
                for i in range(number):
                    lines.pop()
                number = number - number

            if number == 0 and lines != []:
                back_data = '\n'.join(lines)+'\n'
                back_size = len(back_data)
                end = end + back_size
                f.seek(back_size, os.SEEK_CUR)
                number = -1

        if end == 0 and number >= 0:
            print("No change: requested removal would leave empty file: {} bytes,{} lines".format(_end,_number - number))
            return 3
        if end > 0 and number == -1:
            if test:                
                print("will Remove {} lines && {} bytes from end of file".format(_number,_end - end))
            else:
                f.truncate()
                print("Removed {} lines && {} bytes from end of file".format(_number,_end - end))
            return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='the file to truncate')
    parser.add_argument('number',type=uint,help='line number to truncate')
    parser.add_argument('-s','--size',type = pint,default=10240,help='read buffer size in byte')
    parser.add_argument('--nothalf',default=False,action='store_true',help='check the last line is half line')
    parser.add_argument('--test',action='store_true',help='just test and will not truncate it(help you find the right size)')
    args = parser.parse_args()
        
    file = args.file
    number = args.number
    size = args.size
    nothalf = args.nothalf
    test = args.test
    if test:
        print('It\'s just a test')
    truncate_tail(file,number,size=size,nothalf=nothalf,test=test)
