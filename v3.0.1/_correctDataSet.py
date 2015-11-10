#!/usr/bin/python
# -*- coding: utf-8-*-
# =======================================================================
from PIL import Image
import os

# =======================================================================
def one():
    # ------------------------------------------------------------------- 
    test_image = "alpha/a_5_URW_Bookman_L.png"
    original = Image.open(test_image)
    #original.show()

    width, height = original.size   # Get dimensions

    left = width/10
    top = height/10
    right = 4
    bottom = 4

    cropped_example = original.crop((0, 30, width, height-30))
    cropped_example.show()
    # ------------------------------------------------------------------- 

# =======================================================================
def _correct_this(_img_path,_img_name):
    # ------------------------------------------------------------------- 
    #img = Image.new( 'RGB', (255,255), "black") # create a new black image
    new_img = Image.new( 'RGB', (30,30), "white") # create a new black image
    new_img_pixels = new_img.load() # create the pixel map
    # -------------------------------------------------------------------
    
    original_img = Image.open(_img_path+_img_name);
    original_pixels = original_img.load();
    #original.show()
    #width, height = original.size   # Get dimensions
    _VALIND_COLOR_RANGE = 200;

    _FST_X_ROW = 1000000;
    _FST_Y_ROW = 1000000;

    # ------------------------------------------------------------------- 
    for _X in xrange(original_img.size[0]):
        for _Y in xrange(original_img.size[1]):
            if(original_pixels[_X, _Y][0]+original_pixels[_X, _Y][1]+original_pixels[_X, _Y][2])/3 < _VALIND_COLOR_RANGE:
                if _X < _FST_X_ROW:
                    _FST_X_ROW = _X;

    for _Y in xrange(original_img.size[1]):
        for _X in xrange(original_img.size[0]):
            if(original_pixels[_X, _Y][0]+original_pixels[_X, _Y][1]+original_pixels[_X, _Y][2])/3 < _VALIND_COLOR_RANGE:
                if _Y < _FST_Y_ROW:
                    _FST_Y_ROW = _Y;

    # ------------------------------------------------------------------- 
    #exit();
    if _FST_Y_ROW == 1000000:
        _FST_Y_ROW = 0;
    if _FST_X_ROW == 1000000:
        _FST_X_ROW = 0;

    if _FST_X_ROW == 0 and _FST_Y_ROW == 0:
        #print("Image begins in the corner! Exit now.")
        return 0;
    else:
        print(_img_name);
        print("_FST_Y_ROW: ",_FST_Y_ROW);
        print("_FST_X_ROW: ",_FST_X_ROW);
    # ------------------------------------------------------------------- 
    # Create nex pixel matrix
    _NEW_PIXEL_MATRIX = []

    for _X in xrange(_FST_X_ROW, original_img.size[0]):
        for _Y in xrange(_FST_Y_ROW, original_img.size[1]):
            if(original_pixels[_X, _Y][0]+original_pixels[_X, _Y][1]+original_pixels[_X, _Y][2])/3 < _VALIND_COLOR_RANGE:
                _NEW_PIXEL_MATRIX.append([_X-_FST_X_ROW, _Y-_FST_Y_ROW, original_pixels[_X, _Y][0], original_pixels[_X, _Y][1], original_pixels[_X, _Y][2]]);

    # ------------------------------------------------------------------- 
    """
    for _X in xrange(_FST_X_ROW, new_img.size[0]):    # for every pixel:
        for _Y in xrange(_FST_Y_ROW, new_img.size[1]):
            new_img_pixels[_X,_Y] = (0, 0, 255) # set the colour accordingly
    """

    try:
        for _PIXEL in _NEW_PIXEL_MATRIX:
            new_img_pixels[_PIXEL[0],_PIXEL[1]] = (_PIXEL[2],_PIXEL[3],_PIXEL[4]) # set the colour accordingly
            #print(_PIXEL);
            #exit();
    except Exception as _index_error:
        print(_PIXEL)
        _ans = raw_input("Continue ? (y/n)")
        if _ans == "n":
            return 0;
    # ------------------------------------------------------------------- 
    #new_img.show();
    new_img.save(_img_path+_img_name);
    # ------------------------------------------------------------------- 

# =======================================================================
def _convert_all():

    # ------------------------------------------------------------------- 
    _img_path = "test/";
    # ------------------------------------------------------------------- 
    for img_name in os.listdir(_img_path):
        _correct_this(_img_path, img_name)
    # ------------------------------------------------------------------- 

# =======================================================================
_convert_all();
