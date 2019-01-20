"""Read passwords from a LastPass CSV file and check each of them against
the Pwned Passwords database.
"""

import csv
import hashlib
import requests

def num_pw_found(byte_string):
    """Check the online Pwned Passwords database for the given password.

    Return the number of times the password was found, or 0 otherwise.
    """
    hasher = hashlib.sha1()
    hasher.update(byte_string)
    digest = hasher.hexdigest().upper()
    pw_list = requests.get('https://api.pwnedpasswords.com/range/{}'.format(digest[:5]))
    for line in pw_list.text.split('\n'):
        info = line.split(':')
        if info[0] == digest[5:]:
            return int(info[1])
    return 0

def check_lastpass_csv(filename):
    """Open a LastPass CSV file and check each password in the file against
    the Pwned Passwords database.
    """
    total_pw = 0
    hacked_pw = 0
    with open(filename, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader) # skip header row
        for row in csvreader:
            if len(row) == 7:
                pw_bytes = row[2].encode('utf-8')
                num_found = num_pw_found(pw_bytes)
                if num_found > 0:
                    print('\nHacked password: "{}" found {} time(s)'.format(row[2], num_found))
                    print('Full entry: {}'.format(row))
                    hacked_pw += 1
                else:
                    print('.', end='', flush=True)
                total_pw += 1
            else:
                print('\nBadly formatted row: {}'.format(row))
    print('\nChecked {} passwords, {} have been hacked.'.format(total_pw, hacked_pw))

if __name__ == "__main__":
    check_lastpass_csv('export.csv')
