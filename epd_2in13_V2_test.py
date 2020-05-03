#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import textwrap
import requests
import json
import twitter
f = open("conf.json","r")
config = json.loads(f.read());

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from lib.waveshare_epd import epd2in13_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

def writeText(text, rectangle, font):
    text = '\n'.join(textwrap.wrap(text, 32))

    # # partial update
    logging.info("Writing Text")
    text_image = Image.new('1', (epd.height, epd.width), 255)
    text_draw = ImageDraw.Draw(text_image)
    # epd.init(epd.FULL_UPDATE)
    epd.displayPartBaseImage(epd.getbuffer(text_image))
    epd.init(epd.PART_UPDATE)
    text_draw.rectangle(tuple(rectangle), fill=0)
    text_draw.rectangle(tuple(rectangle), fill=255)
    text_draw.text(tuple(rectangle[0:2]), text, font=font, fill=0)
    epd.displayPartial(epd.getbuffer(text_image))

logging.basicConfig(level=logging.DEBUG)
testTweet = """@elonmusk Anyone think they can get a good multiplayer Minecraft working on Teslas? Or maybe create a game that interacts virtually with reality like Pokémon Go while driving safely? Like a complex version of Pac-man or Mario Kart?"""
api = twitter.Api(config['consumer_key'],
                  config['consumer_secret'],
                  config['access_token_key'],
                  config['access_token_secret']
                  )

try:
    logging.info("epd2in13_V2 Demo")
    
    epd = epd2in13_V2.EPD()
    logging.info("init and Clear")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)

    logging.info("Loading Font")
    # Drawing on the image
    tweetFont = ImageFont.truetype('Font.ttc', 12)
    moneyFont = ImageFont.truetype('Font.ttc', 20)
    writeText(testTweet, [0,0,200,122], tweetFont)
    writeText("15%", [200,50,200,122], moneyFont)
    logging.info("Goto Sleep...")
    epd.sleep()

except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()
