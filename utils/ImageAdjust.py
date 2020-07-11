#!/usr/bin/env python
# coding: utf-8

import cv2
import numpy as np

class ImageAdjust:
    def __init__(self, img, desired_size):
        old_size = img.shape[:2] # old_size is in (height, width) format
        ratio = float(desired_size)/max(old_size)
        new_size = tuple([int(x*ratio) for x in old_size])

        delta_w = desired_size - new_size[1]
        delta_h = desired_size - new_size[0]

        top, bottom = delta_h//2, delta_h-(delta_h//2)
        left, right = delta_w//2, delta_w-(delta_w//2)

        self.top, self.bottom, self.left, self.right = top, bottom, left, right
        self.desired_size = desired_size
        self.old_size = old_size
        self.new_size = new_size

    def resize(self,img):
        im = cv2.resize(img, (self.new_size[1], self.new_size[0]))

        color = [0, 0, 0]
        new_im = cv2.copyMakeBorder(im, self.top, self.bottom, self.left, 
                self.right, cv2.BORDER_CONSTANT,value=color)
        
        return new_im
    
    def recover(self, img):
        im = img[self.bottom:(self.desired_size-self.top), 
                 self.left:self.desired_size-self.right]
        im = cv2.resize(im, (self.old_size[1], self.old_size[0]))

        return im

