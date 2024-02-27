# Description
Burrito Manga Reader is a manga reader that is intended exclusively for local manga files. I've found that many PC manga readers
don't really support what I've been looking for as a "local file" reader; so I wanted to build one myself.

# Disclaimer
This manga reader is my very first large programming project, thus the code is messy and does contain some flaws.
However, the manga reader has been throughly tested on windows and works correctly. With that being said, I hope you enjoy the
reader and I hope to someday build this again from the ground up to make it more efficient. Thank you.
## Known bugs
- Very rare crashes when selecting a book to read from library

## Support on the following Operating Systems
- Windows 10/11 (tested)
- Linux (not tested)
- Mac (not tested)

## Supports the following manga file formats
- .jpg
- .png
![Screenshot 2023-09-04 140223](https://github.com/burritoparty/Burrito-Manga-Reader/assets/117869058/5eaba094-247e-469e-b4ee-776f2b33d5d3)

## Installation
When first launching the .exe for the reader, it will try to setup a library location.

On Windows it will default to:
> D:\Burrito Manga Reader Library

To change the library location, on first launch run the following in Windows Powershell:
1. Change to the directory that contains the .exe
  > cd "D:\example directory"
2. Start the program with an argument of a directory
  >  ".\Burrito Manga Reader.exe" D:\Library

## Usage
The main UI contains all books in the library.

**Tags**
- Add Tag: Adds a tag to be used when editing book information.
- Delete Tag: Removes an existing tag.
- Edit Tag: Renames an existing tag.

**Authors**
- Add Author: Adds an author to be used when editing book information.
- Edit Author: Renames an existing author.

**Import Book**
- Opens a window to import a new book.

**Sorting and Filtering**
- Read Later: Opens a new window to browse books that are saved to Read Later.
- Favorites: Opens a new window to browse books that are saved to Favorites.
- Filter by Tag: Opens a new window to select tags to filter by.
- Search by Name: Opens a new window to search by name.
- Filter by Author: Opens a new window to select an author to filter by.

**Tab navigator**
- First Tab: Jumps to the first tab in the library.
- Previous Tab: Goes back by one tab.
- Next Tab: Goes to the next tab.
- Last Tab: Goes to last tab in the library.

**Library**
- Clicking a book will open it's description.
![readermainui](https://github.com/burritoparty/Burrito-Manga-Reader/assets/117869058/02083e21-5974-4d02-8322-3cc7ba952872)

### Importing a book
To import a book click the Import Book button.
**There must be an existing author in the system to add the book to the library, and an author must be selected in the import window using the dropdown.**
- Link: Save a link to the manga.
- Name: Set the name of the manga. This can be used to search the library by name.
- Author: Set the author of the manga. This can be used to search the library by author.
- Select Tags: Set the tags of the manga. These are used for filtering the library.
- Select Book: Use this to point the program to the directory of the book you want to import.
- Submit Book: Finish editing the book's info, and will import the book.
- Add an Author: Will add an author to the library, and place the added author into the author entry.
- Read Later: Adds or removes the book to the read later list.
- Favorite: Adds or removes the book to the favorites list.
![importwindow](https://github.com/burritoparty/Burrito-Manga-Reader/assets/117869058/d585ce73-7ec4-4430-9405-6381fe610410)

### Book Description
Click the Cover on the left to begin reading.
- Update buttons: Will update the books information to the information present in the entry.
- Read Later: Adds or removes the book from the read later list.
- Favorite: Adds or removes the book from the favorites list.
- Tags: Adds or removes tags from the book's description.
![bookdescription](https://github.com/burritoparty/Burrito-Manga-Reader/assets/117869058/62b6e82e-4803-4360-92a9-780838e655e1)

### Book Reader
Hotkeys:
- Previous Page: left arrow, a
- Next Page: right arrow, d
- Exit Reader: esc
![Screenshot 2023-09-04 135450](https://github.com/burritoparty/Burrito-Manga-Reader/assets/117869058/112a97a8-c214-471d-8fdb-664df5c3ac38)
