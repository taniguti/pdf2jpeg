#!/usr/bin/python
# -*- coding: utf-8 -*-

# モジュールのimport
import sys
import os

# モジュール os.pathのクラスsplitextを初期化
from os.path import splitext
from objc import YES, NO
from Foundation import NSData
from AppKit import *

numOfArgs = len(sys.argv)
pdf_file = sys.argv[1].decode('utf-8')
pdf_filename = os.path.basename(pdf_file)
if (numOfArgs > 2):
    output_dir = sys.argv[2].decode('utf-8')
else:
    output_dir = os.path.dirname(pdf_file)

fileData = NSData.dataWithContentsOfFile_(pdf_file)
refer = NSPDFImageRep.imageRepWithData_(fileData)
numOfPages = refer.pageCount()

for n in range (0, numOfPages):
    refer.setCurrentPage_(n)
    img = NSImage.alloc().init()
    img.addRepresentation_(refer)
    pdf_size = refer.size()
    width, height = pdf_size
    tiff = img.TIFFRepresentation()
    bmp = NSBitmapImageRep.imageRepWithData_(tiff)
    jpeg = bmp.representationUsingType_properties_(NSJPEGFileType, {NSImageCompressionFactor: 1.0})
    jpeg_file = "%s/%s-%d.jpg" % (output_dir,splitext(pdf_filename)[0], n)
    if not os.path.exists (jpeg_file):
        jpeg.writeToFile_atomically_(jpeg_file, False)
