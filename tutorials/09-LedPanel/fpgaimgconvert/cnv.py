#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Igor Brkic
# license: MIT

import argparse
import sys
try:
    from PIL import Image
except ImportError:
    print("PIL package is required")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--size', help="Output size WxH (default 64x64, if set to 'same' will take input image's size)", default='64x64', type=str)
    parser.add_argument('-a', '--keep-aspect-ratio', help="Keep aspect ratio when resizing", action='store_true')
    parser.add_argument('-d', '--dither', help="Enable dithering (default false)", action='store_true')
    parser.add_argument('-b', '--debug', help="save output to provided image file", type=str)
    parser.add_argument('-c', '--colors', help="Number of colors in palette (default 16)", default=16, type=int)
    parser.add_argument('-g', '--gamma', help="gamma correction", default=1.0, type=float)
    parser.add_argument('-n', '--gain', help="gain", default=1.0, type=float)
    parser.add_argument('-o', '--output', help="Output file name (default output.mem)", default="output.mem")
    parser.add_argument('-p', '--palette', help="Save palette to file instead of printing to stdout", type=str)
    parser.add_argument('input_image', help="Input image (jpg, png, gif)")
    args = parser.parse_args()

    try:
        im = Image.open(args.input_image)
        im = im.convert('RGB')
    except IOError:
        print("Invalid input image")
        return

    if args.size=='same':
        size = im.size
    else:
        size = [int(s) for s in args.size.split('x')]

    # resize if needed
    if im.size[0]>size[0] or im.size[1]>size[1]:
        if args.keep_aspect_ratio:
            # get scaled dimensions
            if im.size[0]>im.size[1]:
                s = (size[0], int(im.size[1]*(size[0]/float(im.size[0]))))
            else:
                s = (int(im.size[0]*(size[1]/float(im.size[1]))), size[1])
            out = Image.new(im.mode, size)
            out.paste(im.resize(s, resample=Image.LANCZOS), (int(abs(size[0]-s[0])/2),int(abs(size[1]-s[1])/2)))
            im = out
        else:
            im = im.resize(size, resample=Image.LANCZOS)

    # gamma correction
    if args.gamma!=1.0:
        for y in range(im.height):
            for x in range(im.width):
                px = tuple([int(((c/255.0)**args.gamma)*255) for c in im.getpixel((x, y))])
                im.putpixel((x,y), px)

    # "amplification"
    if args.gain!=1.0:
        for y in range(im.height):
            for x in range(im.width):
                px = tuple([max(0, min(int(c*args.gain),255)) for c in im.getpixel((x, y))])
                im.putpixel((x,y), px)

    if args.dither:
        im = im.convert('RGB', colors=args.colors)
    im = im.quantize(args.colors)
    im = im.convert('RGB')

    if args.debug:
        im.save(args.debug)

    palette = [c[1] for c in im.getcolors()]
    if len(palette)<args.colors:
        palette += [(0,0,0)]*(args.colors-len(palette))
    
    # print out palette
    if args.palette:
        with open(args.palette, 'w') as p:
            for idx, c in enumerate(palette):
                p.write("%02x%02x%02x\n"%(c[0], c[1], c[2]))
    else:
        for idx, c in enumerate(palette):
            print("assign palette[%d] = 24'h%02x%02x%02x;" % (idx, c[0], c[1], c[2]))

    # save output image
    with open(args.output, 'w') as f:
        for y in range(im.height):
            for x in range(im.width):
                f.write("%x\n"%(palette.index(im.getpixel((x, y))),))

if __name__=='__main__':
    main()
