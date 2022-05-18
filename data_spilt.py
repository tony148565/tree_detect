import os, shutil, random
import pathlib


#path = input()

def spilt_test(ori_path, path, label):
    files = os.listdir(path)
    filenumber = len(files)
    #data = []
    rate = 0.2
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
    rate = 0.1
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
    
    files = os.listdir(path)
    count = 0
    for file in files:
        shutil.move(path + file, ori_path + 'train_set/' + label + '/' + file)
        count+=1
    
    
    return
    
def get_path(ori_path):
    getpaths =  os.listdir(ori_path)
    print(getpaths)
    for path in getpaths:
        if path != 'test_set' and path != 'train_set' and path != 'validation_set': 
            spilt_test(ori_path, ori_path + path + '/', path)

def setup(path):
    if not os.path.exists(path + 'train_set'):
        os.mkdir(path + 'train_set')
    if not os.path.exists(path + 'test_set'):
        os.mkdir(path + 'test_set')
    if not os.path.exists(path + 'validation_set'):
        os.mkdir(path + 'validation_set') 

if __name__ == '__main__':
    path = "C:/Users/user/Desktop/影像辨識/4band_256_test/"
    setup(path)
    #spilt_test(path)
    get_path(path)