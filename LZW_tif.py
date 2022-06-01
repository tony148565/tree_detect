import rasterio as rio
import rasterio
import os
import tqdm
import numpy as np
from pathlib import Path

def load_data(path):
    files = Path(path)
    #print(files)
    for file in files.glob('**/*.tif'):
        lzw_method(file)
        #print(file)

def lzw_method(input_path):
    print(input_path)
    rasterdata = rio.open(input_path, 'r')
    datas = rasterdata.read()
    profile = rasterdata.profile
    rasterdata.close()
    #print(type(profile))
    if 'compress' in profile:
        print(profile['compress'])
    else:
    #print(profile[])
        profile.update(compress='lzw')
        with rio.open(input_path, 'w', **profile) as file:
            file.write(datas)
        print('done')

def main():
    print('root_path: ')
    root_path = input()
    #print('hello world!!')
    load_data(root_path)
    print('complete!!')
    #lzw_method('30.tif')


if __name__ == '__main__':
    main()