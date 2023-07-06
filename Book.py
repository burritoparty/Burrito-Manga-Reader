import gc
import json
import sys
import customtkinter
import os
from PIL import Image, ImageDraw


class Book:

    def get_path(self):
        return self.path

    def get_name(self):
        return self.name

    def get_author(self):
        return self.author

    def get_link(self):
        return self.link

    def get_cover(self):
        return self.cover

    def get_tags(self):
        return self.tagged

    # if you need the pages as thumbnail size, set is_thumbnail to True
    def get_pages(self, is_thumbnail):

        # load pages
        images = []
        pages = []
        valid_images = [".jpg", ".png"]

        if is_thumbnail == True:
            SINGLE_PAGE_SIZE = (175, 250)
            DOUBLE_PAGE_SIZE = (175, 250)

        else:
            SINGLE_PAGE_SIZE = (950, 1300)
            DOUBLE_PAGE_SIZE = (1600, 1200)

        # FIXME need to account for double pages
        for f in os.listdir(self.path):
            ext = os.path.splitext(f)[1]
            if ext.lower() not in valid_images:
                continue
            w,h = (Image.open(os.path.join(self.path, f))).size
            if w < 1600:
                images.append(Image.open(os.path.join(self.path, f)).resize(SINGLE_PAGE_SIZE)) # Image.open(os.path.join(path, f)).resize(COVER_SIZE) old: images.append(Image.open(os.path.join(self.path, f)))
            else:
                images.append(Image.open(os.path.join(self.path, f)).resize(DOUBLE_PAGE_SIZE))

        for i in images:
            w, h = i.size
            if w < 1600:
                pages.append((customtkinter.CTkImage(dark_image=i, size=SINGLE_PAGE_SIZE)))
            else:
                pages.append((customtkinter.CTkImage(dark_image=i, size=DOUBLE_PAGE_SIZE)))

        return pages

    def get_cover(self):
        return self.cover

    def get_full_cover(self):
        VALID_IMAGES = (".jpg", ".png")
        cover_im = None
        for f in os.listdir(self.path):
            ext = os.path.splitext(f)[1]
            if ext.lower() not in VALID_IMAGES:
                continue
            cover_im = Image.open(os.path.join(self.path, f)).resize((400, 550))
            break

        return customtkinter.CTkImage(
            dark_image=self.add_corners(cover_im, 10), size=(400, 550))

    def add_corners(self, im, rad):
        circle = Image.new('L', (rad * 2, rad * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
        alpha = Image.new('L', im._size, 255)
        w, h = im.size
        alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
        alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
        alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
        alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
        im.putalpha(alpha)
        return im


    def __init__(self, path, name, author, link, tagged):
        self.path = path
        self.name = name
        self.author = author
        self.link = link
        self.tagged = tagged
        self.cover = None
        COVER_SIZE = (225, 300)
        VALID_IMAGES = (".jpg", ".png")

        cover_im = None
        for f in os.listdir(self.path):
            ext = os.path.splitext(f)[1]
            if ext.lower() not in VALID_IMAGES:
                continue
            cover_im = Image.open(os.path.join(path, f)).resize(COVER_SIZE)
            break

        # set cover
        self.cover = customtkinter.CTkImage(
            dark_image=self.add_corners(cover_im, 10), size=COVER_SIZE)
