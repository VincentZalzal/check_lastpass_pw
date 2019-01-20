# check_lastpass_pw

This is a simple python script to check a password CSV export file against the
Pwned Passwords database. This should work directly with LastPass and Keepass
export files.

## Requirements

- Python 3 (3.6 on Windows if using non-ASCII characters)
- requests

## How to export a LastPass CSV file

In your browser, open the LastPass extension menu and choose _More Options ->
Advanced -> Export -> LastPass CSV File_. Copy and paste the content into a new
text file. To avoid having to modify the script, name the file `export.csv`, and
save it next to the python script.

**Note**: the first row of the CSV file is assumed to contain the column names.
It should contain either 'password' or 'Password'.

**Note**: the script assumes the CSV file is encoded in utf-8.

## Run

Simply type `python check_lastpass_pw.py`.

**Note**: if you are using Windows and the CSV file contains non-ASCII
characters, you may get an error on the print command. Use python 3.6 or later
to solve the issue.
