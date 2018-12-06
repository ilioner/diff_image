# -*- coding: utf-8 -*-

from PIL import Image
from os import listdir
import os
import shutil
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

def picPostfix():  # 相册后缀的集合
    postFix = set()
    postFix.update(['bmp', 'jpg', 'png', 'tiff', 'gif', 'pcx', 'tga', 'exif',
                    'fpx', 'svg', 'psd', 'cdr', 'pcd', 'dxf', 'ufo', 'eps', 'JPG', 'raw', 'jpeg'])
    return postFix


def getDiff(width, high, image):  # 将要裁剪成w*h的image照片
    diff = []
    im = image.resize((width, high))
    imgray = im.convert('L')  # 转换为灰度图片 便于处理
    pixels = list(imgray.getdata())  # 得到像素数据 灰度0-255

    for row in range(high):  # 逐一与它左边的像素点进行比较
        rowStart = row * width  # 起始位置行号
        for index in range(width - 1):
            leftIndex = rowStart + index
            rightIndex = leftIndex + 1  # 左右位置号
            diff.append(pixels[leftIndex] > pixels[rightIndex])

    return diff  # *得到差异值序列 这里可以转换为hash码*


def getHamming(diff=[], diff2=[]):  # 暴力计算两点间汉明距离
    hamming_distance = 0
    for i in range(len(diff)):
        if diff[i] != diff2[i]:
            hamming_distance += 1

    return hamming_distance

def startTask(path):
    width = 32
    high = 32  # 压缩后的大小
    dirName = path  # 相册路径
    allDiff = []
    postFix = picPostfix()  # 图片后缀的集合

    tempPath = makeTempDir(path+"/temp")
    dirList = listdir(dirName)
    cnt = 0
    for i in dirList:
        cnt += 1
        # print
        # cnt  # 可以不打印 表示处理的文件计数
        if str(i).split('.')[-1] in postFix:  # 判断后缀是不是照片格式
            print(i)
            im = Image.open(r'%s/%s' % (dirName, i))
            diff = getDiff(width, high, im)
            allDiff.append((str(i), diff))

    same_file_arr = []

    for i in range(len(allDiff)):
        for j in range(i + 1, len(allDiff)):
            if i != j:
                ans = getHamming(allDiff[i][1], allDiff[j][1])
                if ans <= 5:  # 判别的汉明距离，自己根据实际情况设置
                    print(allDiff[i][0], "与", allDiff[j][0], "相似度极高！")
                    same_file_arr.append(allDiff[j][0])
                    # print("准备将相似度高的文件移动至temp文件夹====>%s"%allDiff[j][0])
                    # shutil.move(dirName+"/"+allDiff[j][0], tempPath+"/"+allDiff[j][0])
                    # print(allDiff[j][0]+"已经被移动")
    for sub in same_file_arr:
        if os.path.exists(dirName+"/"+sub):
            print("准备将相似度高的文件移动至temp文件夹====>%s"%sub)
            shutil.move(dirName+"/"+sub, tempPath+"/"+sub)
            print(sub+"已经被移动")


def makeTempDir(path):

    folder = os.path.exists(path)
    print(folder)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("---  new folder...  ---")
        print("---  OK  ---")
        return path
    return path

if __name__ == '__main__':
    # if len(sys.argv)==0:
    #     print("=============请输入要查重的路径重新运行==========")
    # else:
    #     path = sys.argv[0]
    path="";
    startTask(path)
        # startTask(path)