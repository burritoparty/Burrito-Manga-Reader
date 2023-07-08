import json
from os import path
import customtkinter
from Database import *
from Functions import *


class TagFrame(customtkinter.CTkFrame):

    def tag_append_call(self, tags_json):
        tags = []
        if path.isfile(tags_json) is False:
            print("path dont exist")
        else:
            # create the dialogue box
            tags_append_dialogue = customtkinter.CTkInputDialog(text="New tag: ", title="Append a new tag")
            tags_append_dialogue.geometry('0+0')

            # load the json
            with open(tags_json, 'r') as f:
                load_tags = json.load(f)

            # load the tag names from the json into an array
            for i in load_tags['tags']:
                tags.append(i['name'])

            # get the input from the user
            new_tag = tags_append_dialogue.get_input()

            # check if the input is valid
            if check_exists(new_tag, tags, False) is False:
                error = customtkinter.CTkToplevel()
                error.geometry("0+0")
                label = customtkinter.CTkLabel(error,
                                               text="this tag already exists\n(not case sensitive)",
                                               font=("Roboto", 20))
                label.grid(padx=10, pady=10)
            else:
                # append to load_tags
                load_tags["tags"].append({
                    "name": new_tag
                })
                with open(tags_json, 'w') as f:
                    json.dump(load_tags, f, indent=2)


    def __init__(self, tag_json, bookframe, master, **kwargs):
        super().__init__(master, **kwargs)

        # make the label
        self.tag_label = customtkinter.CTkLabel(self,
                                                text="Sort by tag",
                                                text_color=light_pink,
                                                fg_color="transparent")

        # make the buttons
        self.tag_append = customtkinter.CTkButton(self,
                                                  text="Add tag",
                                                  fg_color=light_pink,
                                                  text_color=black,
                                                  hover_color=dark_pink,
                                                  command=lambda x=tag_json: self.tag_append_call(x))
        self.tag_delete = customtkinter.CTkButton(self,
                                                  text="Delete tag",
                                                  fg_color=light_pink,
                                                  text_color=black,
                                                  hover_color=dark_pink)
        self.tag_rename = customtkinter.CTkButton(self,
                                                  text="Rename tag",
                                                  fg_color=light_pink,
                                                  text_color=black,
                                                  hover_color=dark_pink)

        self.tag_label.grid(row=0, column=0, padx=20)
        self.tag_append.grid(row=2, column=0, padx=20, pady=20)
        self.tag_delete.grid(row=3, column=0, padx=20, pady=20)
        self.tag_rename.grid(row=4, column=0, padx=20, pady=20)
