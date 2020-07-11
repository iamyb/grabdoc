#!/usr/bin/env python 
import os, sys, cv2, argparse
import numpy as np
from utils.DocumentSegmentation import DocSegModel
from utils.QuadCorners import get_corners

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('input', help='specify the input image path')
    parser.add_argument('-o', '--output',nargs='?',required=True,
                        help='specify output file name with png extention')
    args=parser.parse_args()

    if not os.path.exists(args.input):
        sys.exit('Error: invalid input image file path: %s' % args.input)

    fname_out = args.output
    if fname_out.split('.')[-1] not in ['png']:
        sys.exit('Error: output file name should be with PNG extention!')

    model = DocSegModel()
    mask,img = model.predict(args.input)
    #print(np.unique(mask))

    img = cv2.imread(args.input)
    #c0, c1, c2, c3 = list(get_corners(mask.astype(np.uint8)))
    corners_l = list(get_corners(mask.astype(np.uint8)))
    corners_l.sort(key=lambda x: np.sum(x))

    c0, c1, c2, c3 = corners_l[0],corners_l[1],corners_l[2],corners_l[3]

    cv2.line(img, tuple(c0.astype(np.uint32)), tuple(c1.astype(np.uint32)), [255, 255, 0], 2)
    cv2.line(img, tuple(c0.astype(np.uint32)), tuple(c2.astype(np.uint32)), [255, 255, 0], 2)
    cv2.line(img, tuple(c3.astype(np.uint32)), tuple(c1.astype(np.uint32)), [255, 255, 0], 2)
    cv2.line(img, tuple(c3.astype(np.uint32)), tuple(c2.astype(np.uint32)), [255, 255, 0], 2)

    cv2.imwrite(fname_out, img)
