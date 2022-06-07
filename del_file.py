import os, shutil, random
import argparse

def rand_del_file(path, rate):
    files = os.listdir(path)
    filenumber = len(files)
    #rate = 0.88
    picknumber = int(filenumber*rate)
    sample = random.sample(files,picknumber)
    for file in sample:
        os.remove(path + '/' + file)

def find_smaller_folder(path):
    folders = os.listdir(path)
    rate_list = []
    path_list = []
    min = -1
    for folder in folders:
        files = len(os.listdir(path + folder))
        rate_list.append(files)
        path_list.append(path + folder)
        print(folder)
        if min == -1:
            min = files
        elif files < min:
            min = files
        
    #print(min)
    for i in range(0, len(rate_list)):
        rate_list[i] = 1 - (min / rate_list[i]) 
    #print(rate_list)
    return path_list, rate_list
    
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="輸入資料夾路徑")
    args = parser.parse_args()
    path = args.path
    if not path.endswith('/'):
        path = path + '/'
    path_list, rate_list = find_smaller_folder(path)
    
    print(path_list)
    print(rate_list)
    
    for p, r in zip(path_list, rate_list):
        rand_del_file(p, r)
    print('hello python')
    

if __name__ == '__main__':
    main()