import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
import cv2

import blob
import os
import random

plotting = False

textures = os.path.join('blob_generation', 'textures')
bgs = os.path.join('blob_generation', 'backgrounds')
generated = os.path.join('blob_generation', 'generated')

texture_paths = list(map(lambda texture: os.path.join(textures, texture), os.listdir(textures)))
random.shuffle(texture_paths)
bg_paths = list(map(lambda bg: os.path.join(bgs, bg), os.listdir(bgs)))
random.shuffle(bg_paths)

if len(texture_paths) > len(bg_paths): texture_paths = texture_paths[0:len(bg_paths)]
if len(bg_paths) > len(texture_paths): bg_paths = bg_paths[0:len(texture_paths)]

pair_list = list(zip(bg_paths, texture_paths))


def to_txt(filepath, rectangles, img_shape):
    f = open(filepath + '.txt', 'w')
    for r in rectangles:
        x = r[0]/img_shape[1]
        y = r[1]/img_shape[0]
        w = r[2]/img_shape[1]
        h = r[3]/img_shape[0]
        f.write("0 {0:.6f} {1:.6f} {2:.6f} {3:.6f}\n".format(x,y,w,h))


for i, pair in enumerate(pair_list):

    counter = str(i+1).zfill(4)
    blob_no = random.randint(1,9)
    if blob_no > 4: blob_no = 1

    if i < 10: blob_no = 1

    texture = mpimg.imread(pair[1])
    if texture.shape[0] > 1000 or texture.shape[1] > 1500:
        texture = cv2.resize(texture, (640,480))
    bg = mpimg.imread(pair[0])

    # print(pair[1])
    # print(texture.shape)

    print("Progress: {0}/{1}".format(i+1, len(pair_list)))

    width = bg.shape[1]
    height = bg.shape[0]

    rectangles={"1":list(), "2": list(), "3":list()}

    filenames = ["generated_sample_" + counter + "_" + str(x) for x in range(1,4)]
    filepaths = list(map(lambda name: os.path.join(generated, name), filenames))

    new_img=[bg,bg,bg]

    for k in range(blob_no):
        for l in range(3):
            if l == 0:
                b = blob.Blob([height, width])
            else:
                b = b.genarete_rotated()
            texture_b, blob_pos = blob.blob_texture(texture,b, pos= None if l == 0 else blob_pos)
            new_img[l], rectangle, pos = blob.join_blob(new_img[l], texture_b, b, prev_pos=None if l == 0 else pos)
            if isinstance(rectangle, list): rectangles[str(l+1)].append(rectangle)
        texture = mpimg.imread(pair_list[random.randint(-i, 0)][1])
        if texture.shape[0] > 1000 or texture.shape[1] > 1500:
            texture = cv2.resize(texture, (640, 480))

    for l in range(3):
        mpimg.imsave(filepaths[l] + '.jpg', new_img[l])
        to_txt(filepaths[l], rectangles[str(l+1)], new_img[l].shape)

    fig = plt.figure()
    for l in range(3):
        ax = fig.add_subplot(3, 1, l+1)
        ax.imshow(new_img[l])
        for rectangle in rectangles[str(l+1)]:
            r = patches.Rectangle((rectangle[0] - rectangle[2] // 2, rectangle[1] - rectangle[3] // 2), rectangle[2],
                                  rectangle[3], linewidth=1, edgecolor='r', facecolor='none')
            ax.add_patch(r)

    fig.savefig(filepaths[0][:-1]+'verif.jpg')
    plt.close(fig)

if plotting:
    plt.show()