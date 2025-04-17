# coding:utf-8
import json
import os
import sys
import os.path as osp
from PIL import Image
from tqdm import tqdm
from deeplab import DeeplabV3

Image.MAX_IMAGE_PIXELS = None


def cut(im, x, dirsavepath):
    a = im.size[0]
    b = im.size[1]
    imc = im.copy()
    imc = imc.convert('RGB')
    regionx = []
    e, f = 512, 512
    regionx = [0 for x in range(0, a//e+2)]
    for n in range(b//f):
        for i in range(a//e):
            box = (e*i, f*n, e*(i+1), f*(n+1))
            regionx[i] = imc.crop(box)
            x = x+1

            regionx[i].save(dirsavepath+'\\{}.jpg'.format(x))

        regionx[a//e+1] = imc.crop((a-e, f*n, a, f*(n+1)))

        x = x+1
        regionx[a//e+1].save(dirsavepath+'\\{}.jpg'.format(x))

    for i in range(a//e):
        box = (e*i, b-f, e*(i+1), b)
        regionx[i] = imc.crop(box)
        x = x+1
        regionx[i].save(dirsavepath+'\\{}.jpg'.format(x))

    regionx[a//e] = imc.crop((a-e, b-f, a, b))
    x = x+1
    regionx[a//e].save(dirsavepath+'\\{}.jpg'.format(x))
    return x


def paste(dirsavepath, resultpath, a, b, x, p, xsum, name):

    e, f = 512, 512

    to_image = Image.new('RGB', (a, b))
    oo = xsum-x

    for n in range(b//f):
        for i in range(a//e):
            oo += 1
            k = Image.open(dirsavepath+"\\{}.jpg".format(oo))
            box = (e*i, f*n, e*(i+1), f*(n+1))
            to_image.paste(k, box)
        oo += 1
        k = Image.open(dirsavepath+"\\{}.jpg".format(oo))
        box = (a-e, f*n, a, f*(n+1))
        to_image.paste(k, box)
    for i in range(a//e):
        oo += 1
        k = Image.open(dirsavepath+"\\{}.jpg".format(oo))
        box = (e*i, b-f, e*(i+1), b)
        to_image.paste(k, box)
    oo += 1
    k = Image.open(dirsavepath+"\\{}.jpg".format(oo))
    box = (a-e, b-f, a, b)
    to_image.paste(k, box)
    to_image.save(resultpath+"/{}".format(name))


def predict(directory, dirsave):
    deeplab = DeeplabV3()

    dir_origin_path = directory
    dir_save_path = dirsave

    img_names = os.listdir(dir_origin_path)
    for img_name in tqdm(img_names):
        if img_name.lower().endswith(('.bmp', '.dib', '.png', '.jpg', '.jpeg',
                                      '.pbm', '.pgm', '.ppm', '.tif', '.tiff')
                                     ):
            image_path = os.path.join(dir_origin_path, img_name)
            image = Image.open(image_path)
            r_image = deeplab.detect_image(image)
            if not os.path.exists(dir_save_path):
                os.makedirs(dir_save_path)
            r_image.save(os.path.join(dir_save_path, img_name))


def execute(data_path, out_dir, name, sr=243.4):
    x = 0
    xlist = []
    sizelist = []
    xsumlist = []
    lodgingnum = 0
    # black = 0
    green = 0
    image_list = [data_path+name]

    directory = '{}cutlist'.format(data_path)
    dirsave = '{}prelist'.format(data_path)
    result = out_dir + name.split(".")[0]

    os.makedirs(directory, exist_ok=True)
    os.makedirs(dirsave, exist_ok=True)
    os.makedirs(result, exist_ok=True)

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}: {e}")
    for filename in os.listdir(dirsave):
        file_path = os.path.join(dirsave, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}: {e}")
    for filename in os.listdir(result):
        file_path = os.path.join(result, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}: {e}")

    for filename in image_list:
        if filename.endswith('.jpg') or filename.endswith('.png'):

            with Image.open(filename) as im:
                a, b = im.size[0], im.size[1]
                sizelist.append((a, b))
                x = cut(im, x, directory)
                xsumlist.append(x)
                try:
                    eachx = x-xlist[-1]
                    xlist.append(eachx)
                except IndexError:
                    xlist.append(x)

    predict(directory, dirsave)

    for i in range(len(xlist)):
        a, b = sizelist[i][0], sizelist[i][1]
        # size = a* b
        # sizesum += size
        paste(dirsave, result, a, b, xlist[i], i, xsumlist[i], name)

    extensions = (".jpg", ".jpeg", ".png")

    image_paths = [osp.join(result, f) for f in os.listdir(result) if f.
                   endswith(extensions)]

    print('预测结束,开始计算')
    for image_path in image_paths:
        with Image.open(image_path) as im:
            width, height = im.size
            pixels = im.load()
            for x in range(width):
                for y in range(height):
                    pixel = pixels[x, y]  # 直接使用像素访问对象，而不是调用getpixel方法
                    r, g, b = pixel  # 一次性解包RGB值，避免多次索引

                    # 将条件判断合并为一个表达式，减少判断的次数
                    if (r > 240 and g < 50 and b < 50) or (r < 50 and g > 240
                                                           and b < 50):
                        if r > 240 and g < 50 and b < 50:
                            lodgingnum += 1
                        else:
                            green += 1

    res_dict = dict()
    res_dict['area'] = round(lodgingnum*float(sr)*0.000001, 2)
    res_dict['mu'] = round(lodgingnum*float(sr)*0.000001*0.0015, 2)
    res_dict['ratio'] = round((lodgingnum/(green+lodgingnum))*100, 2)
    print("倒伏面积大约为:"+str(res_dict['area'])+'平方米\n'+str(res_dict['mu'])+'亩')
    print("倒伏比例:"+str(res_dict['ratio'])+"%")
    with open(out_dir + name.split(".")[0] + '/data.json', 'w', encoding='utf-8') as f:  
        json.dump(res_dict, f, ensure_ascii=False, indent=4)



# if __name__ == '__main__':
#     data_path = str(sys.argv[1])
#     out_dir = (sys.argv[2])
#     name = (sys.argv[3])
#     sr = float(sys.argv[4])
#     execute(data_path, out_dir, name, sr)
