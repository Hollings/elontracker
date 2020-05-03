#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from lib.waveshare_epd import epd2in13_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

def writeText(text, rectangle):
    # # partial update
    logging.info("Writing Text")
    text_image = Image.new('1', (epd.height, epd.width), 255)
    text_draw = ImageDraw.Draw(text_image)
    epd.init(epd.FULL_UPDATE)
    epd.displayPartBaseImage(epd.getbuffer(text_image))
    epd.init(epd.PART_UPDATE)
    text_draw.rectangle(tuple(rectangle), fill=255)
    text_draw.text((120, 80), text, font=font24, fill=0)
    epd.displayPartial(epd.getbuffer(text_image))

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd2in13_V2 Demo")
    
    epd = epd2in13_V2.EPD()
    logging.info("init and Clear")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)

    logging.info("Loading Font")
    # Drawing on the image
    font15 = ImageFont.truetype('Font.ttc', 15)
    font24 = ImageFont.truetype('Font.ttc', 24)

    writeText("Test", [120, 80, 220, 105])

    logging.info("Goto Sleep...")
    epd.sleep()



except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()
