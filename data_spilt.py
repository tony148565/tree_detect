import os, shutil, random
import pathlib
import math
import argparse
import stat

#path = input()

def spilt_test(ori_path, path, label, lists_rate):
    files = os.listdir(path)
    filenumber = len(files)
    #data = []
    rate = lists_rate[1]
    picknumber = int(filenumber*rate)
    sample = random.sample(files,picknumber)
    print(len(sample))
    folder_name =['test_set']
    count = 0
    try:
        os.mkdir(ori_path + 'test_set/' + label)
    except FileExistsError:
        print("folder exist")
    try:
        os.mkdir(ori_path + 'train_set/' + label)
    except FileExistsError:
        print("folder exist")
    for name in sample:
        shutil.move(path + name, ori_path + 'test_set/' + label + '/' + name)
        count+=1
    
    files = os.listdir(path)
    rate = lists_rate[2]
    vpicknumber = int(filenumber*rate)
    vsample = random.sample(files,vpicknumber)
    print(len(vsample))
    try:
        os.mkdir(ori_path + 'validation_set/' + label)
    except FileExistsError:
        print("folder exist")
    count = 0
    for file in vsample:
        shutil.move(path + file, ori_path + 'validation_set/' + label + '/' + file)
        count+=1
    
    if lists_rate[2] + lists_rate[1] + lists_rate[0] != 1:
        files = os.listdir(path)
        rate = lists_rate[0]
        vpicknumber = int(filenumber*rate+1)
        vsample = random.sample(files,vpicknumber)
        print(len(vsample))
        try:
            os.mkdir(ori_path + 'train_set/' + label)
        except FileExistsError:
            print("folder exist")
        count = 0
        for file in vsample:
            shutil.move(path + file, ori_path + 'train_set/' + label + '/' + file)
            count+=1
    else:
        files = os.listdir(path)
        count = 0
        for file in files:
            shutil.move(path + file, ori_path + 'train_set/' + label + '/' + file)
            count+=1
    
    
    return

def not_zero(num):
    j=0
    while True:
        ans = round(num, j)
        #print(ans)
        if ans == 0:
            j+=1
        else:
            break
    return ans

def balance(ori_path, paths):
    lists_count = []
    lists_rate = []
    i = 0
    max_type = -1
    sec_type = -1
    for path in paths:
        files = os.listdir(ori_path + path + '/')
        filenumber = len(files)
        lists_count.append(filenumber)
        list_rate = [0.7, 0.2, 0.1] # train test validation
        lists_rate.append(list_rate)
        #print(lists_count)
        if max_type == -1:
            print('max')
            print(i)
            max_type = i
            i+=1
            continue
        elif lists_count[max_type] < lists_count[i]:
            max_type = i
        
        if sec_type == -1 and max_type != -1:
            print('sec')
            print(i)
            sec_type = i
        elif lists_count[sec_type] < lists_count[i]:
            if lists_count[sec_type] > lists_count[max_type]:
                sec_type = max_type
                max_type = i
            else:
                sec_type = i
        i+=1
    
    rate = not_zero(lists_count[sec_type]/lists_count[max_type])
    print('rate:')
    print(rate)
    lists_rate[max_type][0] = not_zero(lists_rate[max_type][0] * rate)
    lists_rate[max_type][1] = not_zero(lists_rate[max_type][1] * rate)
    lists_rate[max_type][2] = not_zero(lists_rate[max_type][2] * rate)
    if lists_rate[max_type][0] == 1:
        lists_rate[max_type][0] = lists_rate[max_type][0] - lists_rate[max_type][1] - lists_rate[max_type][2]
    print(lists_rate)
    #print('################################################')
    return lists_rate
    
    
    

def get_path(ori_path, lists_rate):
    getpaths =  os.listdir(ori_path)
    print(getpaths)
    #files = os.listdir(path)
    #balance(ori_path, getpaths)
    i = 0
    for path in getpaths:
        if path != 'test_set' and path != 'train_set' and path != 'validation_set': 
            spilt_test(ori_path, ori_path + path + '/', path, lists_rate[i])
            i += 1

def del_folder(path):
    path = path.replace('/', '\\')
    folders = os.listdir(path)
    for folder in folders:
        if folder != 'test_set' and folder != 'train_set' and folder != 'validation_set':
            print('del' + path + folder)
            if not os.access(path + folder, os.W_OK):
                os.chmod(path + folder, stat.S_IWRITE) # above PermissionError
            shutil.rmtree(path + folder)
            #os.remove(path + folder)


def setup(path):
    if not os.path.exists(path + 'train_set'):
        os.mkdir(path + 'train_set')
    if not os.path.exists(path + 'test_set'):
        os.mkdir(path + 'test_set')
    if not os.path.exists(path + 'validation_set'):
        os.mkdir(path + 'validation_set') 

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="輸入資料夾路徑")
    args = parser.parse_args()
    path = args.path
    #print(path)
    if not path.endswith('/'):
        path = path + '/'
    ############################################################
    files = os.listdir(path)
    lists_rate = balance(path, files)
    setup(path)
    #spilt_test(path)
    get_path(path, lists_rate)
    ############################################################
    del_folder(path)
    print('complete!!')