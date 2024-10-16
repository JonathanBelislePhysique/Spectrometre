
def lbl_coord_to_img_coord(roi_lab=[0, 0, 0, 0], lbl_size_x=0, lbl_size_y=0, im_size_x=0, im_size_y=0):
    x1 = int(roi_lab[0] * im_size_x / lbl_size_x)
    x2 = int(roi_lab[2] * im_size_x / lbl_size_x)
    y1 = int(roi_lab[1] * im_size_y / lbl_size_y)
    y2 = int(roi_lab[3] * im_size_y / lbl_size_y)
    return [x1, y1, x2, y2]


if __name__ == '__main__':
    print(lbl_coord_to_img_coord(roi_lab=[160, 120, 320, 240],
                                 lbl_size_x=320,
                                 lbl_size_y=240,
                                 im_size_x=1280,
                                 im_size_y=1024))
