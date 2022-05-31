import multi_channel
from osgeo import gdal
from affine import Affine
import os

def raster_center(raster):
    width, height = raster.RasterXSize, raster.RasterYSize
    xmed = width/2
    ymed = height/2
    return (xmed, ymed)

def rotate_gt(affine_matrix, angle, pivot=None):
    affine_src = Affine.from_gdal(*affine_matrix)
    affine_dst = affine_src * affine_src.rotation(angle, pivot)
    return affine_dst.to_gdal()


def tif_rotate(path, num):
    #path = '000000573.tif' # 檔名
    name = path.replace('.tif','')
    #print(name)
    rotate = 360//num
    #print(rotate)
    if num == 1:
        return '0'
    r = 0
    for i in range(num-1):
        img = gdal.Open(path)
        driver = gdal.GetDriverByName("GTiff")
        dataset_dst = driver.CreateCopy(str(name) + '_' + str(i) + '.tif', img, strict=0)
        gt_affine = img.GetGeoTransform()
        center = raster_center(img)
        r = r + rotate
        print(r)
        dataset_dst.SetGeoTransform(rotate_gt(gt_affine, r, center))
        lzw_compress(path)
    return 'complete'

def test2():
    path = 'SP27GTIF.tif'
    name = path.replace('.tif','')
    img = gdal.Open(path, 1)
    driver = gdal.GetDriverByName("GTiff")
    dataset_dst = driver.CreateCopy(str(name) + '_.tif', img, strict=0)
    GeoTransform = dataset_dst.GetGeoTransform()
    GeoTransform = list(GeoTransform)
    GeoTransform[2] = 90.0
    GeoTransform[-2] = 90.0
    GeoTransform = tuple(GeoTransform)
    #tif_driver = gdal.GetDriverByName('GTiff')    
    #out_ds = tif_driver.Create('test01.tif', im_width,im_height, 3, band1.DataType)
    dataset_dst.SetGeoTransform(GeoTransform)
    del dataset_dst
    #lzw_compress()

def load_folder(path):
    folders = os.listdir(path)
    print(folders) # label name 
    num_files = [] # how mant file in this folder
    for folder in folders:
        #print(folder)
        num_files.append(len(os.listdir(path + '/' + folder)))
    #print(num_files) #debug
    count = []
    for i in num_files:
        count.append(max(num_files)//i)
    #print(count)
    j=0
    
    for folder in folders:
        #print(folder)
        files = os.listdir(path + '/' + folder)
        for file in files:
            state = tif_rotate(path + '/' + folder + '/' + file, count[j])
            print(state)
        j = j + 1
    
def lzw_compress(data):
    rasterfile = rasterio.open(data)
    rasterdata2 = rasterfile.read()
    profile = rasterfile.profile
    
    profile.update(compress='lzw')
    with rasterio.open(data, mode='w', **profile) as dst:
        dst.write(rasterdata2)

def main():
    load_folder('./8band_256_8bit')
    #tif_rotate('SP27GTIF.tif', 2)
    #test2()
    



if __name__ == '__main__':
    main()