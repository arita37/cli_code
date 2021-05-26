# Sublime tools
Actions based on the currently selected text/word, in Sublime Text 2/3.
This package adds:

 - `stackoverflow` search
 - `Git` custom git command
 ## Install
 go to your Sublime packages directory(Sublime Text/Packages) Then run this command  `git clone https://github.com/arita37/cli_code/tree/dev/cli_code/sublime/googlesearch`.

Or you can download the package as a zip file   then copy it into your Sublime packages directory.  
[https://github.com/arita37/cli_code/tree/dev/cli_code/sublime/googlesearch](https://github.com/arita37/cli_code/tree/dev/cli_code/sublime/googlesearch)

**important**
in short all you need to do is to put the folder `googlesearch` in your sublime Packages folder `(Preferences->Browse Packeges..)`

## Usage
we are using this command style
`command::subcommand`
**you have to follow this style .**
you need to select the text and press **`ctrl + alt + g`** 
the two commands available 

 - `git`
 - `stack`

sub command for the `stack` is the text to search in stack overflow , the sub command in `git` will be ignored for now
example:

 1. `stack::how to add module in python` : 
	- first will open up browser window and search for 'how to add 		 					module in python in stackoverflow
	- delete the text `stack::how to add module in python`
2. `git::any text` :
	- first will add and commit all files with size less than 7 Mb and last edit from with in the last week
	- push it to the remote repo
	- delete the text 