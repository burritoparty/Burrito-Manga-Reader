from Database import *
from Library_Reader import *
from Import import *
from Tag import *
from Author import *
# create database
# test line# test line
if os.path.exists("D:\Burrito Manga Reader\library.json") is False:
    print("made json")
    file = open("D:\Burrito Manga Reader\library.json", "x")
    with open("D:\Burrito Manga Reader\library.json", 'w') as f:
        books_json = {
                    "book": [
                    ]
                }
        json.dump(books_json, f, indent=2)
    file.close()

# create tag database
if os.path.exists("D:\\Burrito Manga Reader\\tags.json") is False:
    print("made json")
    file = open("D:\\Burrito Manga Reader\\tags.json", "x")
    with open("D:\\Burrito Manga Reader\\tags.json", 'w') as f:
        books_json = {
                    "tags": [
                    ]
                }
        json.dump(books_json, f, indent=2)
    file.close()



# sorting database
tags.sort()
authors.sort()

customtkinter.set_appearance_mode("system")
root = customtkinter.CTk()  # main window
root.title("Burrito Manga Reader")  # name of program
# set dimensions and center window
root.geometry('%dx%d+%d+%d' % (1920, 1080,
                               get_x_coordinates(1920, root.winfo_screenwidth()),
                               get_y_coordinates(1080, root.winfo_screenheight())))
root.attributes('-topmost', 0)

# make frames
root.bookDisplayTabs = BookFrame(master=root, width=1625, height=1025)
root.tagFrame = TagFrame(bookframe=root.bookDisplayTabs, master=root)
root.authorFrame = AuthorFrame(master=root)
root.importFrame = ImportFrame(master=root)

# place frames
root.tagFrame.grid(row=0, column=0, padx=20, pady=20)
root.authorFrame.grid(row=1, column=0, padx=20, pady=20)
root.importFrame.grid(row=2, column=0, padx=20, pady=0)
root.bookDisplayTabs.grid(row=0, column=1, rowspan=10, sticky="nsew", padx=20, pady=20)

root.mainloop()
