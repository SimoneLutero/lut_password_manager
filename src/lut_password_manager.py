# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 12:09:40 2020

@author: SimoneLutero
"""

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                         #
#        ____                 __                     __   __              #
#       / __ \___ _   _____  / /___  ____  ___  ____/ /  / /_  __  __     #
#      / / / / _ \ | / / _ \/ / __ \/ __ \/ _ \/ __  /  / __ \/ / / /     #
#     / /_/ /  __/ |/ /  __/ / /_/ / /_/ /  __/ /_/ /  / /_/ / /_/ /      #
#    /_____/\___/|___/\___/_/\____/ .___/\___/\__,_/  /_.___/\__, /       #
#                                /_/                        /____/        #
#    _____ _                               __         __                  #
#   / ___/(_)___ ___  ____  ____  ___     / /  __  __/ /____  _________   #
#   \__ \/ / __ `__ \/ __ \/ __ \/ _ \   / /  / / / / __/ _ \/ ___/ __ \  #
#  ___/ / / / / / / / /_/ / / / /  __/  / /__/ /_/ / /_/  __/ /  / /_/ /  #
# /____/_/_/ /_/ /_/\____/_/ /_/\___/  /_____\__,_/\__/\___/_/   \____/   #
#                                                                         #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import argparse
import json
import os
import sys
from datetime import datetime
from getpass import getpass
import pyperclip
from pyperclip import PyperclipException
from cv2 import cv2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from lut_print_utils import print_title
from lut_print_utils import print_with_frame


class FunctionalDirectories:
    """
    Contains paths of Security Snapshots Directory and Storages Directory
    """
    security_snapshots_dir = ''
    storages_path = ''


FunDir = FunctionalDirectories()


def login_to_storage(storage_filename):
    """
    Does the log in to the selected storage, checking the password.

    Parameters:
        storage_filename (str): name of the storage .bin file
    """
    for attempts in range(0, 3):
        password = getpass('Insert Main Password: ')
        try:
            get_decrypted_storage(storage_filename, password)
            print('Successful access')
        except (KeyError, ValueError):
            print('Authentication failed')
            print('Attempts remained: ', 2 - attempts)
            # Security snapshot
            webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            ret, frame = webcam.read()
            if not ret:
                print('Could not access to webcam')
                continue
            now_datetime = datetime.now()
            now_timestamp = now_datetime.strftime("%Y%m%d_%H%M%S%f")
            img_filename = "security_snapshot_login_{}_{}.png".format(
                storage_filename[:-4], now_timestamp)
            cv2.imwrite(FunDir.security_snapshots_dir+img_filename, frame)
            webcam.release()
            cv2.destroyAllWindows()
            continue

        main_storage_menu(storage_filename, password)
        return


def create_encrypted_storage(new_storage_filename, main_storage_password, debug_mode=False):
    """
    Create a new storage

    Parameters:
        new_storage_filename (str): The name of the storage .bin file to create.
        main_storage_password (str): The password that will be used to access to the new storage.
    """
    main_storage_password_encoded = main_storage_password.encode('utf8')
    if debug_mode:
        print('main_storage_password_encoded is: ',
              main_storage_password_encoded, end='\n\n')

    main_storage_password_padded = pad(main_storage_password_encoded, 16)
    if debug_mode:
        print('main_storage_password_padded is: ',
              main_storage_password_padded, end='\n\n')

    # Instantiates AES cipher for encryption
    cipher = AES.new(main_storage_password_padded, AES.MODE_CBC)

    data = []
    if debug_mode:
        print('data is: ', data, end='\n\n')

    data_json = json.dumps(data)
    if debug_mode:
        print('data_json is: ', data_json, end='\n\n')

    data_json_encoded = data_json.encode('utf8')
    if debug_mode:
        print('data_json_encoded is: ', data_json_encoded, end='\n\n')

    data_padded = pad(data_json_encoded, AES.block_size)
    if debug_mode:
        print('data_padded is: ', data_padded, end='\n\n')

    data_encrypted = cipher.encrypt(data_padded)
    if debug_mode:
        print('data_encrypted is: ', data_encrypted, end='\n\n')

    if debug_mode:
        print('cipher.iv is: ', cipher.iv, end='\n\n')

    new_storage_filename = open(
        FunDir.storages_path+new_storage_filename, 'wb')

    new_storage_filename.write(cipher.iv)

    new_storage_filename.write(data_encrypted)

    new_storage_filename.close()

    print(new_storage_filename, ' has been created', end='\n\n')


def update_encrypted_storage_password(storage_filename, actual_main_storage_password,
                                      new_main_storage_password, debug_mode=False):
    new_main_storage_password_encoded = new_main_storage_password.encode(
        'utf8')
    if debug_mode:
        print('main_storage_password_encoded is: ',
              new_main_storage_password_encoded, end='\n\n')

    new_main_storage_password_padded = pad(
        new_main_storage_password_encoded, 16)
    if debug_mode:
        print('main_storage_password_padded is: ',
              new_main_storage_password_padded, end='\n\n')

    # Instantiates AES cipher for encryption
    cipher = AES.new(new_main_storage_password_padded, AES.MODE_CBC)

    data = get_decrypted_storage(
        storage_filename, actual_main_storage_password)
    if debug_mode:
        print('data is: ', data, end='\n\n')

    data_json = json.dumps(data)
    if debug_mode:
        print('data_json is: ', data_json, end='\n\n')

    data_json_encoded = data_json.encode('utf8')
    if debug_mode:
        print('data_json_encoded is: ', data_json_encoded, end='\n\n')

    data_padded = pad(data_json_encoded, AES.block_size)
    if debug_mode:
        print('data_padded is: ', data_padded, end='\n\n')

    data_encrypted = cipher.encrypt(data_padded)
    if debug_mode:
        print('data_encrypted is: ', data_encrypted, end='\n\n')

    if debug_mode:
        print('cipher.iv is: ', cipher.iv, end='\n\n')

    storage_filename = open(FunDir.storages_path+storage_filename, 'wb')

    storage_filename.write(cipher.iv)

    storage_filename.write(data_encrypted)

    storage_filename.close()

    print('The main password of storage ',
          storage_filename, ' has been updated', end='\n\n')


def update_encrypted_storage(storage_filename, main_storage_password, new_storage_data,
                             debug_mode=False):
    main_storage_password_encoded = main_storage_password.encode('utf8')
    if debug_mode:
        print('main_storage_password_encoded is: ',
              main_storage_password_encoded, end='\n\n')

    main_storage_password_padded = pad(main_storage_password_encoded, 16)
    if debug_mode:
        print('main_storage_password_padded is: ',
              main_storage_password_padded, end='\n\n')

    # Instantiates AES cipher for encryption
    cipher = AES.new(main_storage_password_padded, AES.MODE_CBC)

    data = new_storage_data
    if debug_mode:
        print('data is: ', data, end='\n\n')

    data_json = json.dumps(data)
    if debug_mode:
        print('data_json is: ', data_json, end='\n\n')

    data_json_encoded = data_json.encode('utf8')
    if debug_mode:
        print('data_json_encoded is: ', data_json_encoded, end='\n\n')

    data_padded = pad(data_json_encoded, AES.block_size)
    if debug_mode:
        print('data_padded is: ', data_padded, end='\n\n')

    data_encrypted = cipher.encrypt(data_padded)
    if debug_mode:
        print('data_encrypted is: ', data_encrypted, end='\n\n')

    if debug_mode:
        print('cipher.iv is: ', cipher.iv, end='\n\n')

    storage_filename = open(FunDir.storages_path+storage_filename, 'wb')

    storage_filename.write(cipher.iv)

    storage_filename.write(data_encrypted)

    storage_filename.close()

    print(storage_filename, ' has been updated', end='\n\n')


def get_decrypted_storage(storage_filename, main_storage_password, debug_mode=False):
    try:
        main_storage_password_encoded = main_storage_password.encode('utf8')
        main_storage_password_padded = pad(main_storage_password_encoded, 16)

        storage_file = open(FunDir.storages_path+storage_filename, 'rb')

        iv = storage_file.read(16)
        if debug_mode:
            print('iv is: ', iv, end='\n\n')

        ciphertext = storage_file.read()
        if debug_mode:
            print('ciphertext is: ', ciphertext, end='\n\n')

        storage_file.close()

        cipher = AES.new(main_storage_password_padded, AES.MODE_CBC, iv)

        data_decrypted = cipher.decrypt(ciphertext)
        if debug_mode:
            print('data_decrypted: ', data_decrypted, end='\n\n')

        data_unpadded = unpad(data_decrypted, AES.block_size)
        if debug_mode:
            print('data_unpadded: ', data_unpadded, end='\n\n')

        data_decoded = data_unpadded.decode('utf8')
        if debug_mode:
            print('data_decoded: ', data_decoded, end='\n\n')

        data = json.loads(data_decoded)
        if debug_mode:
            print('data is: ', data, end='\n\n')

        return data

    except (KeyError, ValueError) as e:
        print('file decryption failed')
        if debug_mode:
            print('Error is: ', e)
        raise e


def show_labels(storage_filename, main_storage_password):
    data = get_decrypted_storage(storage_filename, main_storage_password)
    if len(data) == 0:
        print('Storage empty, no labels present')
        return

    print('Labels:', end='\n\n')
    for record in data:
        print('-', record[0])


def get_password_by_label(storage_filename, main_storage_password):
    data = get_decrypted_storage(storage_filename, main_storage_password)
    label = input('Enter the label: ')
    for record in data:
        if record[0].lower() == label.lower():
            print('Label: ', record[0])
            print('Username: ', record[1])
            try:
                pyperclip.copy(record[2])
            except PyperclipException:
                print(
                    'It seems you do not have a copy/paste mechanism for your system. If on Linux try sudo apt-install xclip.')
                choice = input(
                    'Do you want to see the password in clear? (y/n):')
                if choice == 'y':
                    print('The password is:', record[2])
                return
            print('Password:  Copied to clipboard')  # record[2])
            return
    print('Label not found')


def add_new_password_to_storage(storage_filename, main_storage_password, new_label, new_username, new_password):
    data = get_decrypted_storage(storage_filename, main_storage_password)
    data.append((new_label, new_username, new_password))
    update_encrypted_storage(storage_filename, main_storage_password, data)


def add_a_new_password(storage_filename, main_storage_password):
    new_label = input('Enter a label for the new password: ')
    data = get_decrypted_storage(storage_filename, main_storage_password)
    for record in data:
        if record[0].lower() == new_label.lower():
            print('Label already exists')
            return
    new_username = input(
        'Enter an associated username (or something useful for you to associate with password): ')
    new_password = getpass('Enter the password: ')
    confirm_password = getpass('Retype the password to confirm: ')
    if new_password == confirm_password:
        add_new_password_to_storage(
            storage_filename, main_storage_password, new_label, new_username, new_password)
        print('Password associated with label', new_label, 'has been added')
    else:
        print('Passwords entered are not equals, the password has not been added')


def edit_main_storage_password(storage_filename):
    for attempts in range(0, 3):
        actual_password = getpass('Insert actual Main Password: ')
        try:
            get_decrypted_storage(storage_filename, actual_password)
            new_password = getpass('Insert new Main Password: ')
            confirm_new_password = getpass('Retype the password to confirm: ')
            if new_password == confirm_new_password:
                update_encrypted_storage_password(
                    storage_filename, actual_password, new_password)
            else:
                print(
                    'Passwords entered are not equals, the password has not been added')
            return
        except (KeyError, ValueError):
            print('Authentication failed')
            print('Attempts remained: ', 2 - attempts)
            # Security snapshot
            webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            ret, frame = webcam.read()
            if not ret:
                print('Could not access to webcam')
                continue
            now_datetime = datetime.now()
            now_timestamp = now_datetime.strftime("%Y%m%d_%H%M%S%f")
            img_filename = "security_snapshot_login_{}_{}.png".format(
                storage_filename[:-4], now_timestamp)
            cv2.imwrite(FunDir.security_snapshots_dir+img_filename, frame)
            webcam.release()
            cv2.destroyAllWindows()
            continue


def edit_a_password_by_label(storage_filename, main_storage_password):
    data = get_decrypted_storage(storage_filename, main_storage_password)
    label_to_edit = input('Enter the label: ')
    for record in data:
        if record[0].lower() == label_to_edit.lower():
            new_password = getpass('Insert new Password: ')
            confirm_new_password = getpass('Retype the password to confirm: ')
            if new_password == confirm_new_password:
                data.remove(record)
                record[2] = new_password
                data.append(record)
                update_encrypted_storage(
                    storage_filename, main_storage_password, data)
            else:
                print(
                    'Passwords entered are not equals, the password has not been edited')
                return
            print('Password associated with label',
                  label_to_edit, 'has been edited')
            return
    print('Label not found')


def rename_a_label(storage_filename, main_storage_password):
    data = get_decrypted_storage(storage_filename, main_storage_password)
    label_to_edit = input('Enter the Label to rename: ')
    for record in data:
        if record[0].lower() == label_to_edit.lower():
            new_label = input('Enter new Label: ')
            data.remove(record)
            record[0] = new_label
            data.append(record)
            update_encrypted_storage(
                storage_filename, main_storage_password, data)
            print('The Label has been renamed')
            return
    print('Label not found')


def remove_a_password_by_label(storage_filename, main_storage_password):
    data = get_decrypted_storage(storage_filename, main_storage_password)
    label_to_delete = input('Enter the label: ')
    for record in data:
        if record[0].lower() == label_to_delete.lower():
            data.remove(record)
            update_encrypted_storage(
                storage_filename, main_storage_password, data)
            print('Password associated with Label ' +
                  label_to_delete + ' has been deleted')
            return
    print('Label not found')


def main_storage_menu(storage_filename, main_storage_password):
    """
    Provide the user interactions with password in the accessed storage

    Parameters:
        storage_filename (str): the name of the storage .bin file.
        main_storage_password (str): the password of the storage.
    """
    while True:
        # print_title()
        print_with_frame(storage_filename, '[]', space_before=60)

        print('1) Get password by label')
        print('2) Show labels')
        print('3) Add a new password')
        print('4) Edit a password by label')
        print('5) Remove a password by label')
        print('6) Rename a label')
        print('7) Edit main storage password')
        print('8) Return to storage selection')
        print('0) Exit', end='\n\n')

        choice = input()
        if choice == '1':
            get_password_by_label(storage_filename, main_storage_password)
            continue
        if choice == '2':
            show_labels(storage_filename, main_storage_password)
            continue
        if choice == '3':
            add_a_new_password(storage_filename, main_storage_password)
            continue
        if choice == '4':
            edit_a_password_by_label(storage_filename, main_storage_password)
            continue
        if choice == '5':
            remove_a_password_by_label(storage_filename, main_storage_password)
            continue
        if choice == '6':
            rename_a_label(storage_filename, main_storage_password)
            continue
        if choice == '7':
            edit_main_storage_password(storage_filename)
            continue
        if choice == '8':
            break
        if choice == '0':
            sys.exit(0)


def check_if_storage_exists_and_login(storage_filename):
    """
    Check if the entered storage exists, if yes starts login procedure.

    Parameters:
        storage_filename (str): the name of storage .bin file
    """
    if not storage_filename.endswith('.bin'):
        storage_filename += '.bin'
    if check_if_storage_exists(storage_filename):
        login_to_storage(storage_filename)


def check_if_storage_exists(storage_filename):
    """
    Check if the entered storage exists.

    Parameters:
        storage_filename (str): the name of storage .bin file
    """
    if not storage_filename.endswith('.bin'):
        storage_filename += '.bin'
    for file_to_check in os.listdir(FunDir.storages_path):
        if file_to_check.lower() == storage_filename.lower():
            return True
    print('Storage not found')
    return False


def login_to_a_storage():
    """
    Ask for the storage name and starts login procedure
    """
    storage_filename = input('Enter storage filename: ')
    check_if_storage_exists_and_login(storage_filename)


def show_storages():
    """
    Show a list of the existent storages
    """
    print('Storages:', end='\n\n')
    founded = False
    for file_to_check in os.listdir(FunDir.storages_path):
        if file_to_check.endswith('.bin'):
            print('-', file_to_check)
            founded = True
    if not founded:
        print('No storages present')


def add_a_new_storage():
    """
    Ask for the storage name, ask for the password and creates it
    """
    new_storage_filename = input('Enter new storage filename: ')
    if not new_storage_filename.endswith('.bin'):
        new_storage_filename += '.bin'
    for file_to_check in os.listdir(FunDir.storages_path):
        if file_to_check.lower() == new_storage_filename.lower():
            print('Storage with the same name already exists')
            return
    password = getpass('Enter a new password for the storage: ')
    confirm_password = getpass('Retype the password to confirm: ')
    if password == confirm_password:
        create_encrypted_storage(new_storage_filename, password)
    else:
        print('Passwords entered are not equals, the storage has not been created')


def remove_a_storage():
    """
    Ask for the storage name, check the password and removes it
    """
    storage_filename_to_delete = input(
        'Enter filename of the storage to delete: ')
    if not storage_filename_to_delete.endswith('.bin'):
        storage_filename_to_delete += '.bin'
    for file_to_check in os.listdir(FunDir.storages_path):
        if file_to_check.lower() == storage_filename_to_delete.lower():
            for attempts in range(0, 3):
                password = getpass('Insert Main Password: ')
                try:
                    get_decrypted_storage(storage_filename_to_delete, password)
                    choice = input('Storage ' + storage_filename_to_delete +
                                   ' will be deleted, do you confirm? y/n: ')
                    if choice.lower() == 'y':
                        os.remove(FunDir.storages_path +
                                  storage_filename_to_delete)
                        print('Storage ' + storage_filename_to_delete +
                              ' has been deleted')
                    return
                except (KeyError, ValueError):
                    print('Authentication failed')
                    print('Attempts remained: ', 2 - attempts)
                    # Security Snapshot
                    webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                    ret, frame = webcam.read()
                    if not ret:
                        print('Could not access to webcam')
                        continue
                    now_datetime = datetime.now()
                    now_timestamp = now_datetime.strftime("%Y%b%d_%H%M%S%f")
                    img_filename = "security_snapshot_rem_{}_{}.png".format(
                        storage_filename_to_delete, now_timestamp)
                    cv2.imwrite(FunDir.security_snapshots_dir +
                                img_filename, frame)
                    webcam.release()
                    cv2.destroyAllWindows()
                    continue
    print('Storage not found')


def main_menu():
    """
    Provide user interactions with storages
    """
    while True:
        # print_title()
        print()
        print('1) Access to a storage')
        print('2) Show storages')
        print('3) Add a new storage')
        print('4) Remove a storage')
        print('0) Exit', end='\n\n')

        choice = input()
        if choice == '1':
            login_to_a_storage()
            continue
        if choice == '2':
            show_storages()
            continue
        if choice == '3':
            add_a_new_storage()
            continue
        if choice == '4':
            remove_a_storage()
            continue
        if choice == '0':
            sys.exit(0)


def set_directories():
    """
    Check if functionals directories exist, if not it creates them.
    """
    for file in os.listdir('./'):
        if file == 'storages':
            FunDir.storages_path = './storages/'
        if file == 'security_snapshots':
            FunDir.security_snapshots_dir = './security_snapshots/'

    if FunDir.storages_path == '':
        print('storages dir not found')
        os.mkdir('storages')
        FunDir.storages_path = './storages/'
        print('new storages dir has been created')

    if FunDir.security_snapshots_dir == '':
        print('security_snapshots dir not found')
        os.mkdir('security_snapshots')
        FunDir.security_snapshots_dir = './security_snapshots/'
        print('new security_snapshots dir has been created')


def get_password_by_storage_and_label_cl(storage_filename, label):
    """
    Gets password by storage and label entered on command line

    Parameters:
        storage_filename (str): the name of storage .bin file.
        label (str): the label of the password to retrieve.
    """
    if not storage_filename.endswith('.bin'):
        storage_filename += '.bin'
    for file_to_check in os.listdir(FunDir.storages_path):
        if file_to_check.lower() == storage_filename.lower():
            for attempts in range(0, 3):
                password = getpass('Insert Main Storage Password: ')
                try:
                    data = get_decrypted_storage(storage_filename, password)
                    print('Successful access')
                    for record in data:
                        if record[0].lower() == label.lower():
                            print('Label: ', record[0])
                            print('Username: ', record[1])
                            pyperclip.copy(record[2])
                            # record[2])
                            print('Password:  Copied to clipboard')
                            return
                    print('Label not found')
                    return
                except (KeyError, ValueError):
                    print('Authentication failed')
                    print('Attempts remained: ', 2 - attempts)
                    # Security snapshot
                    webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                    ret, frame = webcam.read()
                    if not ret:
                        print('Could not access to webcam')
                        continue
                    now_datetime = datetime.now()
                    now_timestamp = now_datetime.strftime("%Y%m%d_%H%M%S%f")
                    img_filename = "security_snapshot_login_{}_{}.png".format(
                        storage_filename[:-4], now_timestamp)
                    cv2.imwrite(FunDir.security_snapshots_dir +
                                img_filename, frame)
                    webcam.release()
                    cv2.destroyAllWindows()
                    continue
    print('Storage not found')


def program_main():
    """
    Starts the password manager if it is running as a program.
    """
    set_directories()
    parser = argparse.ArgumentParser()
    parser.add_argument('storage', metavar='storage_name', nargs='?', default=None, help='name of storage file where '
                                                                                         'passwords are stored')
    parser.add_argument('label', metavar='label_name', nargs='?', default=None, help='name of label associated with '
                                                                                     'the password')
    args = parser.parse_args()

    storage_filename = args.storage
    label_to_find = args.label

    if storage_filename and label_to_find:
        get_password_by_storage_and_label_cl(storage_filename, label_to_find)
        return
    if storage_filename and not label_to_find:
        check_if_storage_exists_and_login(storage_filename)
        return
    print_title()
    main_menu()


def module_main():
    """
    Initialize the password manager if it is running as a module.
    """
    set_directories()


# Program Start
if __name__ == '__main__':
    program_main()
if __name__ == 'lut_password_manager':
    module_main()
