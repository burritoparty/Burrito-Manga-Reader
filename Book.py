import os

import customtkinter
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

    # if you need the pages as thumbnail size, set `is_thumbnail` to True
    def get_pages(self, is_thumbnail: bool):

        # load pages
        images: list[Image.Image] = []
        pages: list[customtkinter.CTkImage] = []
        valid_images = [".jpg", ".png"]

        if is_thumbnail:
            single_page_size = (175, 250)
            double_page_size = (175, 250)
        else:
            single_page_size = (950, 1300)
            double_page_size = (1600, 1200)

        for f in os.listdir(self.path):
            ext = os.path.splitext(f)[1]
            if ext.lower() not in valid_images:
                continue
            w, h = (Image.open(os.path.join(self.path, f))).size
            if w < h:
                images.append(Image.open(os.path.join(
                    self.path, f)).resize(single_page_size))
            else:
                images.append(Image.open(os.path.join(
                    self.path, f)).resize(double_page_size))

        for i in images:
            w, h = i.size
            if w < h:
                pages.append((customtkinter.CTkImage(
                    dark_image=i, size=single_page_size)))
            else:
                pages.append((customtkinter.CTkImage(
                    dark_image=i, size=double_page_size)))

        return pages

    def get_full_cover(self):
        VALID_IMAGES = (".jpg", ".png")
        LANDSCAPE_COVER = (550, 400)
        PORTRAIT_COVER = (400, 550)
        cover_im = None
        for f in os.listdir(self.path):
            ext = os.path.splitext(f)[1]
            if ext.lower() not in VALID_IMAGES:
                continue
            cover_im = Image.open(os.path.join(
                self.path, f))
            break

        # There should have a cover image.
        assert cover_im

        w, h = cover_im.size
        if w > h:
            cover_im.resize(LANDSCAPE_COVER)
            return customtkinter.CTkImage(
                dark_image=self.add_corners(cover_im, 10), size=LANDSCAPE_COVER)
        else:
            cover_im.resize(PORTRAIT_COVER)
            return customtkinter.CTkImage(
                dark_image=self.add_corners(cover_im, 10), size=PORTRAIT_COVER)



    def add_corners(self, im: Image.Image, rad: int):
        circle = Image.new('L', (rad * 2, rad * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
        alpha = Image.new('L', im.size, 255)
        w, h = im.size
        alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
        alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
        alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
        alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)),
                    (w - rad, h - rad))
        im.putalpha(alpha)
        return im

    def get_cover_width(self):
        self.cover.cget("size")

    def __init__(self, path: str, name: str, author: str, link: str, tagged: list[str]):
        self.path = path
        self.name = name
        self.author = author
        self.link = link
        self.tagged = tagged
        self.cover = None
        LANDSCAPE_COVER = (300, 250)
        PORTRAIT_COVER = (250, 350)
        VALID_IMAGES = (".jpg", ".png")

        cover_im = None
        if self.path != '':
            for f in os.listdir(self.path):
                ext = os.path.splitext(f)[1]
                if ext.lower() not in VALID_IMAGES:
                    continue
                cover_im = Image.open(os.path.join(path, f))
                break

            # There should have a cover image.
            assert cover_im

            w, h = cover_im.size
            if w > h:
                cover_im.resize(LANDSCAPE_COVER)
                self.cover = customtkinter.CTkImage(
                    dark_image=self.add_corners(cover_im, 10), size=LANDSCAPE_COVER)
            else:
                cover_im.resize(PORTRAIT_COVER)
                self.cover = customtkinter.CTkImage(
                    dark_image=self.add_corners(cover_im, 10), size=PORTRAIT_COVER)


