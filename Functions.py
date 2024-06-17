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


# sort a dict
def sorting(dictionary: dict):
    new_dict = list(dictionary.keys())
    new_dict.sort()
    sorted_dict = {i: dictionary[i] for i in new_dict}

    return sorted_dict


# given a string, parse the start for a num and return it
def get_num(filename: str):
    number = ""
    number_found = False
    # for each character in the string
    for char in filename:
        # if it is a digit
        if char.isdigit():
            number += char
            number_found = True
        elif number_found:
            break

    return int(number)


# given an array of strings, return a dictionary {num : string}
def get_dict(files):
    new_dict = dict()

    for f in files:
        new_dict.update({get_num(f): f})

    return new_dict


# files is an array of the file names
def rename(directory: str, files):
    editing_directory = directory + "/"
    # make the new directory
    # print(directory)
    new_folder = os.path.join(editing_directory, "temp")
    os.mkdir(new_folder)
    new_folder += "/"

    # load the array of string
    for filename in os.listdir(editing_directory):
        if filename != "temp":
            files.append(filename)

    # make the array a dict and sort it by leading numbers in the string
    files_dict = get_dict(files)
    files_dict = sorting(files_dict)

    # for each element in the dictionary
    for i in files_dict:
        # the new file to make's name and directory
        if i > 999:
            new_file = new_folder + str(i) + ".jpg"
        elif i > 99:
            new_file = new_folder + "0" + str(i) + ".jpg"
        elif i > 9:
            new_file = new_folder + "00" + str(i) + ".jpg"
        else:
            new_file = new_folder + "000" + str(i) + ".jpg"

        # the old file's name and directory
        file = editing_directory + files_dict.get(i)
        # rename the file and put it in the new folder
        os.rename(file, new_file)

    # now move all files in the new directory back up
    for filename in os.listdir(new_folder):
        # source to move from
        new_file = editing_directory + "temp/" + filename
        # dst to move to
        old_file = editing_directory + filename
        os.rename(new_file, old_file)

    # delete the temporary folder
    os.rmdir(editing_directory + "temp")


# returns the location of the first item in a directory (numerically)
def get_first_location(directory: str, files):
    editing_directory = directory + "/"

    # load the array of string
    for filename in os.listdir(editing_directory):
        if filename != "temp":
            files.append(filename)

    # make the array a dict and sort it by leading numbers in the string
    files_dict = get_dict(files)
    files_dict = sorting(files_dict)

    return editing_directory + files_dict.get(1)
