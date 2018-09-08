import numpy as np
import cv2
import copy


class Blob:
    def __init__(self, img_shape):
        self.relative_size = np.random.uniform(0.3, 0.8)
        self.is_square = np.random.choice([True, False])
        if self.is_square:
            self.shape = (int(self.relative_size * img_shape[0]), int(self.relative_size * img_shape[0]))
        else:
            self.shape = (int(self.relative_size * img_shape[0]), int(self.relative_size * img_shape[1]))

        self.circles_no = np.random.randint(20, high=26)
        self.circles_sizes = np.random.randint(self.shape[0]//18, high=self.shape[0]//6, size=self.circles_no)
        self.circles_x_pos = np.random.randint(self.shape[1]//3, high=2*self.shape[1]//3, size=self.circles_no)
        self.circles_y_pos = np.random.randint(self.shape[0]//3, high=2*self.shape[0]//3, size=self.circles_no)

        self.mask = np.zeros(self.shape, dtype=bool)

        x_dists = np.arange(self.shape[1])
        y_dists = np.arange(self.shape[0])

        for i, r in enumerate(self.circles_sizes):
            x_diffs = x_dists - self.circles_x_pos[i]
            y_diffs = y_dists - self.circles_y_pos[i]

            x_diffs=x_diffs**2
            y_diffs=y_diffs**2

            x_diffs = np.kron(np.ones((self.shape[0], 1)), x_diffs)
            y_diffs = np.transpose(np.kron(np.ones((self.shape[1], 1)), y_diffs))

            dist_matrix = x_diffs + y_diffs

            self.mask = (self.mask + (dist_matrix < r**2)) > 0

        self.mark_mask()

    def mark_mask(self):

        padding = 2

        left = 0
        right = self.shape[1]
        up = 0
        down = self.shape[0]
        prev_col = False
        prev_row = False

        for col in range(self.shape[1]):
            curr_col = False
            for row in range(self.shape[0]):
                if self.mask[row][col]: curr_col = True
            if curr_col and not prev_col: left = col - padding
            if prev_col and not curr_col: right = col + padding
            prev_col = curr_col

        for row in range(self.shape[0]):
            curr_row = False
            for col in range(self.shape[1]):
                if self.mask[row][col]: curr_row = True
            if curr_row and not prev_row: up = row - padding
            if prev_row and not curr_row: down = row + padding
            prev_row = curr_row

        self.blob_x = (left + right) // 2
        self.blob_y = (up + down) // 2
        self.blob_w = right - left
        self.blob_h = down - up

    def genarete_rotated(self):
        new_blob = copy.deepcopy(self)
        deg=np.random.uniform(-50, high=50)
        new_blob.rotate(deg)
        new_blob.mark_mask()
        return new_blob

    def rotate(self, deg):
        crop_mid_x = self.shape[1] // 2
        crop_mid_y = self.shape[0] // 2
        M = cv2.getRotationMatrix2D((crop_mid_x, crop_mid_y), deg ,1)
        self.mask = cv2.warpAffine(self.mask.astype(float), M, (self.shape[1], self.shape[0]))
        self.mask = self.mask.astype(bool)

    def negative(self):
        blob_cp = self
        blob_cp.mask = ~blob_cp.mask
        return blob_cp


def blob_texture(texture, blob, pos=None):
    texture_b = copy.deepcopy(texture)
    if blob.shape[0] > texture_b.shape[0] or blob.shape[1] > texture_b.shape[1]:
        texture_b = cv2.resize(texture_b, (blob.shape[1], blob.shape[0]))
        no_pos = True
    else:
        x_diff = texture_b.shape[1] - blob.shape[1]
        y_diff = texture_b.shape[0] - blob.shape[0]
        if pos is None:
            x_transl = np.random.randint(0, high=x_diff+1)
            y_transl = np.random.randint(0, high=y_diff+1)
        else:
            x_transl = pos[0]
            y_transl = pos[1]
        texture_b = texture_b[y_transl:y_transl + blob.shape[0], x_transl:x_transl + blob.shape[1]]
        no_pos = False

    texture_b.setflags(write=1)
    for c in range(texture_b.shape[0]):
        for r in range(texture_b.shape[1]):
            if not blob.mask[c][r]: texture_b[c,r,:]=0

    pos = (x_transl, y_transl) if not no_pos else None

    return texture_b, pos


def join_blob(bg, texture_b, blob, prev_pos = None):
    if prev_pos is None:
        x_pos = np.random.randint(0, high=bg.shape[1]) - blob.shape[1]//2
        y_pos = np.random.randint(0, high=bg.shape[0]) - blob.shape[0]//2
    else:
        x_pos = int(np.random.uniform(prev_pos['x']-blob.blob_w, prev_pos['x']+blob.blob_w))
        y_pos = int(np.random.uniform(prev_pos['y']-blob.blob_h, prev_pos['y']+blob.blob_h))

    pos={'x':x_pos, 'y':y_pos}

    new_img = copy.deepcopy(bg)
    new_img.setflags(write=1)
    for r in range(blob.shape[0]):
        for c in range(blob.shape[1]):
            if blob.mask[r][c] and 0 <= r+y_pos < new_img.shape[0] and 0 <= c+x_pos < new_img.shape[1]:
                new_img[r+y_pos,c+x_pos,:] = texture_b[r,c,:]

    rectangle = mark_blob(pos, blob, new_img)

    return new_img, rectangle, pos


def mark_blob(pos, blob, new_img):
    mid_x = pos['x'] + blob.blob_x
    mid_y = pos['y'] + blob.blob_y
    width = blob.blob_w
    height = blob.blob_h

    if mid_x + width // 2 < 0 or mid_x - width // 2 > new_img.shape[1]:
        return None
    elif mid_x - width // 2 < 0:
        diff = -(mid_x - width // 2)
        width = width - diff
        mid_x = width // 2
    elif mid_x + width // 2 > new_img.shape[1]:
        diff = (mid_x + width // 2) - new_img.shape[1]
        width = width - diff
        mid_x = new_img.shape[1] - width // 2

    if mid_y + height // 2 < 0 or mid_y - height // 2 > new_img.shape[0]:
        return None
    elif mid_y - height // 2 < 0:
        diff = -(mid_y - height // 2)
        height = height - diff
        mid_y = height // 2
    elif mid_y + height // 2 > new_img.shape[0]:
        diff = (mid_y + height // 2) - new_img.shape[0]
        height = height - diff
        mid_y = new_img.shape[0] - height // 2

    return [mid_x, mid_y, width, height]