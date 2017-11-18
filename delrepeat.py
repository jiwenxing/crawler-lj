#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author:Jverson

import json
import time


# remove repeat data in the file
def remove_repeat(fileName):
    
    f1 = open(fileName, "r", encoding='UTF-8')
    print("origin length: %d" % (len(f1.readlines())))
    f1.close

    ids = set()
    f = open(fileName, "r", encoding='UTF-8')
    for line in f.readlines():
        line = line.strip() 
        if not len(line) or line.startswith('#'):
            continue                                   
        info = json.loads(line)
        houseId = info.get("链家编号", "0")
        if houseId not in ids:
            ids.add(info.get("链家编号", "0"))
            writer_to_text(info)
    
    print("uniq length: %d" % (len(ids)))
    print("remove repeat done!")
    f.close()


def writer_to_text(list):  # 储存到text
    with open('lj-uniq-'+time.strftime('%Y-%m-%d',time.localtime(time.time()))+'.txt', 'a', encoding='utf-8')as f:
        f.write(json.dumps(list, ensure_ascii=False) + '\n')
        f.close()

def main():
    remove_repeat("lj-data-2017-11-17.txt")



if __name__ == '__main__':
	main()