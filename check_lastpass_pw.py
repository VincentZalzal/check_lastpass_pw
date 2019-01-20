"""Read passwords from a password CSV file and check each of them against
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

def find_password_key(keys):
    """Find the password key name in the given list and return it."""
    if "password" in keys:
        return "password"
    if "Password" in keys:
        return "Password"
    raise Exception('Unable to find the password column in the CSV file; manually add header row.')

def check_password_csv(filename):
    """Open a password CSV file and check each password in the file against
    the Pwned Passwords database.
    """
    total_pw = 0
    hacked_pw = 0
    with open(filename, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        pw_key = find_password_key(csvreader.fieldnames)
        for row in csvreader:
            pw_value = row[pw_key]
            if pw_value is not None:
                pw_bytes = pw_value.encode('utf-8')
                num_found = num_pw_found(pw_bytes)
                if num_found > 0:
                    print('\nHacked password: "{}" found {} time(s)'.format(pw_value, num_found))
                    print('Full entry: {}'.format(row))
                    hacked_pw += 1
                else:
                    print('.', end='', flush=True)
                total_pw += 1
            else:
                print('\nBadly formatted row: {}'.format(row))
    print('\nChecked {} passwords, {} have been hacked.'.format(total_pw, hacked_pw))

if __name__ == "__main__":
    check_password_csv('export.csv')
