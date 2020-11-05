from PIL import Image
import matplotlib.pyplot as plt
import os

path = 'dataset_to_sirius1'
target_shape = (400, 400)

def getname(string): #возвращает строку до чисел: "Alisher_1313Black" => "Alisher_"
    res = ""
    for i in string:
        if '0' <= i <= '9':
            return res
        res += i
    return res

def combine_pictures(im_array):
    def get_concat_h(images):
        n = len(images)
        width = images[0].width
        height = images[0].height
        dst = Image.new('L', (width * n, height))
        for i in range(n):
            dst.paste(images[i], (width * i, 0))
        return dst

    def get_concat_v(images):
        n = len(images)
        width = images[0].width
        height = images[0].height
        dst = Image.new('L', (width, height * n))
        for i in range(n):
            dst.paste(images[i], (0, height * i))
        return dst

    def closest_square(num):
        res = 1
        while res*res < num:
            res += 1
        return res

    n = closest_square(len(im_array))
    h_im = []
    for i in range(n-1):
        h_im += [get_concat_h(im_array[i*n : i*n+n])]
        #h_im[i].show()

    last_h_im = im_array[n*(n-1) : ]
    if last_h_im != []:
        h_im += [get_concat_h(last_h_im)]

    return get_concat_v(h_im)

listdir = os.listdir(path=path)

#тут будет хранится УНИКАЛЬНЫЙ список названий классов
#называется эта штука 'dictionary'
uniquelist = {}
for i in listdir:
    key = getname(i)
    if uniquelist.get(key) == None:
        uniquelist[key] = [i]
    else:
        uniquelist[key] += [i]

number_of_classes = len(uniquelist)
print("Number of classes = ", number_of_classes, ":")

keys = list(uniquelist.keys()) #названия классов
print(keys, "\n")
nameofclass = "retina_" #сюда пишем название класса, который хотим вывести

#эта страшная штука -- массив, кт содержит все картинки данного класса
#в нашем случае это "retina_"
images = [Image.open(path + '/' + i).convert('L').resize(target_shape) for i in uniquelist[nameofclass]]

# images = []
# for i in uniquelist[nameofclass]:
#     im = Image.open(path + '/' + i)
#     im = im.convert('L')
#     im = im.resize(target_shape)
#     images += [im]

combine_pictures(images).show()

#bar_plot
#Гистограмма
x = range(number_of_classes)
plt.bar(x, [len(uniquelist[i]) for i in keys])
plt.xticks(x, keys)
plt.show()