import os
import sys

from PIL import Image, ImageDraw


# test line
def resource(relative_path):
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def add_corners(im: Image.Image, rad: int):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im


# returns the x coordinate for use in centering window
# ex: get_x_coordinates(1920, root.winfo_screenwidth())
def get_x_coordinates(width: int, screen_width: int):
    return (screen_width / 2) - (width / 2)


# returns the y coordinate for use in centering window
# ex: get_y_coordinates(1080, root.winfo_screenwidth())
def get_y_coordinates(height: int, screen_height: int):
    return (screen_height / 2) - (height / 2)


# provide a string to check if it exists in a list
# returns True if it exists in the provided list
# check case is false if caps do not matter
def check_exists(new_string: str, db_list: list, check_case: bool):
    is_new = True

    # caps do not matter
    if check_case is False:

        if new_string != '':
            for i in db_list:
                if new_string.lower() == str(i).lower():
                    is_new = False

    # caps do matter
    else:
        if new_string != '':
            for i in db_list:
                if new_string == str(i):
                    is_new = False

    if new_string == '':
        is_new = False

    return is_new


# shortens title with an ellipse
def shorten_string(title: str):
    twentyfive = False
    fifty = False
    # lol there's def a better way to do this, but it works so whatever
    for (index, _) in enumerate(title):
        if index > 25 and twentyfive is False and str(title[index]).isspace():
            title = title[:index + 1] + "\n" + title[index + 1:]
            twentyfive = True
        elif index > 50 and fifty is False and str(title[index]).isspace():
            title = title[:index + 1] + "\n" + title[index + 1:]
            fifty = True
            title = title[0:index]
            title += "..."

    return title

# places \n
def indent_string(title: str):
    twentyfive = False
    fifty = False
    seventy = False
    hundred = False
    hun_25 = False
    hun_50 = False
    hun_75 = False
    twohun = False
    # lol there's def a better way to do this, but it works so whatever
    for (index, _) in enumerate(title):
        if index > 25 and twentyfive is False and str(title[index]).isspace():
            title = title[:index + 1] + "\n" + title[index + 1:]
            twentyfive = True
        elif index > 50 and fifty is False and str(title[index]).isspace():
            title = title[:index + 1] + "\n" + title[index + 1:]
            fifty = True
        elif index > 75 and seventy is False and str(title[index]).isspace():
            title = title[:index + 1] + "\n" + title[index + 1:]
            seventy = True
        elif index > 100 and hundred is False and str(title[index]).isspace():
            title = title[:index + 1] + "\n" + title[index + 1:]
            hundred = True
        elif index > 125 and hun_25 is False and str(title[index]).isspace():
            title = title[:index + 1] + "\n" + title[index + 1:]
            hun_25 = True
        elif index > 150 and hun_50 is False and str(title[index]).isspace():
            title = title[:index + 1] + "\n" + title[index + 1:]
            hun_50 = True
        elif index > 175 and hun_75 is False and str(title[index]).isspace():
            title = title[:index + 1] + "\n" + title[index + 1:]
            hun_75 = True
        elif index > 200 and twohun is False and str(title[index]).isspace():
            title = title[:index + 1] + "\n" + title[index + 1:]
            twohun = True

    return title
