#!/usr/bin/python
# -*- coding: utf-8-*-
# =======================================================================
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

import os
# =======================================================================
_ALPHA_sm = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"];
_ALPHA_bg = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"];
# =======================================================================
def _createImgFromAlpha(_font_dir, _font_name, _font_size, _alpha_data, _exclu):
    # -------------------------------------------------------------------
    # font = ImageFont.truetype("Arial-Bold.ttf",14)
    """
    _font_name = "LiberationMono-Regular.ttf";
    _font_path = "/usr/share/fonts/truetype/ttf-liberation/";
    _font_size = 24;
    """

    font = ImageFont.truetype(_font_dir+_font_name, _font_size);
    
    for _LETTER in _alpha_data:
        img=Image.new("RGBA", (100,100),(255,255,255))
        draw = ImageDraw.Draw(img)
        draw.text((10, 10),_LETTER,(0,0,0),font=font)
        draw = ImageDraw.Draw(img)
        #img.show()
        img.save("test/"+_LETTER+"_"+_exclu+"_"+str(_font_size)+"px_"+_font_name.split(".")[0]+".png")



    # -------------------------------------------------------------------
# =======================================================================

_FONTS_DIRECTORYS = [
    "/usr/share/fonts/truetype/msttcorefonts/",
    "/usr/share/fonts/truetype/liberation/",
    #"/usr/share/fonts/truetype/lyx/",
    "/usr/share/fonts/truetype/freefont/",
    "/usr/share/fonts/truetype/ttf-dejavu/"
]

def _true_all_fonts(_FONTS_DIRECTORYS):
    # -------------------------------------------------------------------

    for _directory in _FONTS_DIRECTORYS:
        for _font_name in os.listdir(_directory):
            _font_name_no_exe = _font_name.split(".")[0];
            print(_font_name);
            if _font_name_no_exe == "Webdings":
                print("-------------------------------------------------------")
                print(_font_name_no_exe)
                continue;

            _createImgFromAlpha(_directory, _font_name, 24, _ALPHA_sm, "_small_");
            _createImgFromAlpha(_directory, _font_name, 24, _ALPHA_bg, "_big_");


    # -------------------------------------------------------------------

# =======================================================================

_true_all_fonts(_FONTS_DIRECTORYS);


