import customtkinter
from Database import *
from Functions import *


class AuthorFrame(customtkinter.CTkFrame):

    def refresh_author_combobox(self):
        self.authorCombobox.configure(values=authors)

    def delete_author(self):
        if self.delete_author is None or not self.delete_author.winfo_exists():
            self.delete_author = DeleteAuthor(self)  # create window if its None or destroyed
        else:
            self.delete_author.focus()  # if window exists focus it

    def rename_author(self):
        if self.rename_author is None or not self.rename_author.winfo_exists():
            self.rename_author = RenameAuthor(self)  # create window if its None or destroyed
        else:
            self.RenameAuthor.focus()  # if window exists focus it

    def author_dialogue_window(self):
        dialog = customtkinter.CTkInputDialog(text="Name your new author: ", title="Author creation",
                                              button_fg_color=light_pink, button_text_color=black)
        dialog.geometry('%d+%d' % (
            get_x_coordinates(self.winfo_width(), self.winfo_screenwidth()),
            get_y_coordinates(self.winfo_height(), self.winfo_screenheight())
        ))

        # FIXME check input | fix if user presses X button

        # checks if blank or exists
        new_author = dialog.get_input()
        if check_exists(new_author, authors, False) is True:
            authors.append(new_author)

        self.refresh_author_combobox()

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # adding labels combobox and button
        self.authorLabel = customtkinter.CTkLabel(self,
                                                  text="Sort by author",
                                                  text_color=light_pink,
                                                  fg_color="transparent")
        self.authorLabel.grid(row=0, column=0, padx=20)

        self.authorCombobox = customtkinter.CTkComboBox(self,
                                                        values=authors,
                                                        fg_color=light_pink,
                                                        text_color=black,
                                                        dropdown_fg_color=light_pink,
                                                        dropdown_hover_color=dark_pink,
                                                        dropdown_text_color=black,
                                                        state="readonly")
        self.authorCombobox.grid(row=1, column=0, padx=10, pady=10)

        self.authorAddButton = customtkinter.CTkButton(self,
                                                       text="Add author",
                                                       fg_color=light_pink,
                                                       text_color=black,
                                                       hover_color=dark_pink,
                                                       command=self.author_dialogue_window)
        self.authorAddButton.grid(row=2, column=0, padx=20, pady=20)

        self.authorDeleteButton = customtkinter.CTkButton(self,
                                                          text="Delete author",
                                                          fg_color=light_pink,
                                                          text_color=black,
                                                          hover_color=dark_pink,
                                                          command=self.delete_author)
        self.authorDeleteButton.grid(row=3, column=0, padx=20, pady=20)
        self.delete_author = None

        self.authorRenameButton = customtkinter.CTkButton(self,
                                                          text="Rename author",
                                                          fg_color=light_pink,
                                                          text_color=black,
                                                          hover_color=dark_pink,
                                                          command=self.rename_author)
        self.authorRenameButton.grid(row=4, column=0, padx=20, pady=20)
        self.rename_author = None


class DeleteAuthor(customtkinter.CTkToplevel):

    def removal(self, name_of_author):
        authors.remove(name_of_author)
        self.destroy()

    # FIXME i need to update the combobox somehow too

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.attributes('-topmost', 1)
        self.title("Delete Author")
        self.geometry('%d+%d' % (
            get_x_coordinates(self.winfo_width(), self.winfo_screenwidth()),
            get_y_coordinates(self.winfo_height(), self.winfo_screenheight())
        ))

        buttons = []
        index = 0

        num_loops = 0
        r = 0
        c = 0

        if len(authors) != 0:

            for i in authors:
                # create labels and buttons
                self.button = customtkinter.CTkButton(self,
                                                      text=i,
                                                      fg_color=light_pink,
                                                      text_color=black,
                                                      hover_color=dark_pink,
                                                      command=lambda x=i: self.removal(x))
                buttons.append(self.button)

                # display labels and buttons
                buttons[index].grid(row=r, column=c, padx=20, pady=20)
                if c == 2:
                    c = 0
                    r += 1
                else:
                    c += 1
                num_loops += 1
                index += 1

        else:
            self.label = customtkinter.CTkLabel(self, text="There are no existing authors.")
            self.label.grid(row=0, column=0, padx=20, pady=20)


class RenameAuthor(customtkinter.CTkToplevel):

    def rename(self, name_of_author):
        dialog = customtkinter.CTkInputDialog(text="Rename author: ", title="Rename author",
                                              button_fg_color=light_pink, button_text_color=black)
        new_author = dialog.get_input()

        if check_exists(new_author, tags, True) is True:
            authors.remove(name_of_author)
            authors.append(new_author)
            authors.sort()

        self.destroy()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.attributes('-topmost', 1)
        self.title("Rename author")
        self.geometry('%d+%d' % (
            get_x_coordinates(self.winfo_width(), self.winfo_screenwidth()),
            get_y_coordinates(self.winfo_height(), self.winfo_screenheight())
        ))

        buttons = []
        index = 0
        num_loops = 0
        r = 0
        c = 0

        if len(authors) != 0:

            for i in authors:
                # create labels and buttons
                self.button = customtkinter.CTkButton(self,
                                                      text=i,
                                                      fg_color=light_pink,
                                                      text_color=black,
                                                      hover_color=dark_pink,
                                                      command=lambda x=i: self.rename(x))
                buttons.append(self.button)

                # display labels and buttons
                buttons[index].grid(row=r, column=c, padx=20, pady=20)
                if c == 2:
                    c = 0
                    r += 1
                else:
                    c += 1
                num_loops += 1
                index += 1

        # TODO change to gray out buttons instead
        else:
            self.label = customtkinter.CTkLabel(self, text="There are no existing authors.")
            self.label.grid(row=0, column=0, padx=20, pady=20)
