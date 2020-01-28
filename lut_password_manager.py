# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 12:09:40 2020

@author: SimoneLutero
"""

import json
import sys
import os
import pyperclip
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from getpass import getpass
from lut_print_utils import print_title
from lut_print_utils import print_with_frame
import string as str

def login_to_storage(storage_filename):
    for attempts in range(0,3):
        #print_title()
        print('Insert Main Password:')
        password = getpass()
        try:
            get_decrypted_storage(storage_filename, password)
            print('Successful access')
        except (KeyError, ValueError):
            print('Authentication failed')
            print('Attempts remained: ', 2 - attempts)
            #scatta foto webcam
            continue
        
        main_storage_menu(storage_filename, password)
        return

def create_encrypted_storage(new_storage_filename, main_storage_password, debug_mode=False):
    
    main_storage_password_encoded = main_storage_password.encode('utf8')
    if debug_mode:
        print('main_storage_password_encoded is: ', main_storage_password_encoded)
        print()
        
    main_storage_password_padded = pad(main_storage_password_encoded, 16)
    if debug_mode:
        print('main_storage_password_padded is: ', main_storage_password_padded)
        print()
        
    #Instantiates AES cipher for encryption
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
    
    new_storage_filename = open(new_storage_filename, 'wb')
    
    new_storage_filename.write(cipher.iv)
    
    new_storage_filename.write(data_encrypted)
    
    new_storage_filename.close()
    if debug_mode:
        print(new_storage_filename, 'has been created', end='\n\n')
  
def update_encrypted_storage(storage_filename, main_storage_password, new_storage_data, debug_mode=False):
    
    main_storage_password_encoded = main_storage_password.encode('utf8')
    if debug_mode:
        print('main_storage_password_encoded is: ', main_storage_password_encoded)
        print()
        
    main_storage_password_padded = pad(main_storage_password_encoded, 16)
    if debug_mode:
        print('main_storage_password_padded is: ', main_storage_password_padded)
        print()
        
    #Instantiates AES cipher for encryption
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
    
    storage_filename = open(storage_filename, 'wb')
    
    storage_filename.write(cipher.iv)
    
    storage_filename.write(data_encrypted)
    
    storage_filename.close()
    if debug_mode:
        print(storage_filename, 'has been updated', end='\n\n')
    
def get_decrypted_storage(storage_filename, main_storage_password, debug_mode=False):
    try:
        main_storage_password_encoded = main_storage_password.encode('utf8')
        main_storage_password_padded = pad(main_storage_password_encoded, 16)
        
        storage_file = open(storage_filename, 'rb')
        
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
    for record in data:
        print(record[0])

def get_password_by_label(storage_filename, main_storage_password):
    data = get_decrypted_storage(storage_filename, main_storage_password)
    print('Enter the label: ')
    label = input()
    for record in data:
        if record[0].lower() == label.lower():
            print('Label: ', record[0])
            print('Username: ', record[1])
            pyperclip.copy(record[2])
            print('Password: ', 'Copied to clipboard')#record[2])
            return
    print('Label not found')
    
def add_new_password_to_storage(storage_filename, main_storage_password, new_label, new_username, new_password):
    data = get_decrypted_storage(storage_filename, main_storage_password)
    data.append((new_label, new_username, new_password))
    update_encrypted_storage(storage_filename, main_storage_password, data)
    
def add_a_new_password(storage_filename, main_storage_password):
    print('Enter a label for the new password:')
    new_label = input()
    print('Enter an associated username (or something useful for you to associate with this password)')
    new_username = input()
    print('Enter the password:')
    new_password = getpass()
    print('Retype the password to confirm')
    confirm_password = getpass()
    if(new_password == confirm_password):
        add_new_password_to_storage(storage_filename, main_storage_password, new_label, new_username, new_password)
    else:
        print('Passwords entered are not equals, the password has not been added')
        
def remove_a_password_by_label(storage_filename, main_storage_password):
    data = get_decrypted_storage(storage_filename, main_storage_password)
    print('Enter the label: ')
    label = input()
    for record in data:
        if record[0].lower() == label.lower():
            data.remove(record)
            update_encrypted_storage(storage_filename, main_storage_password, data)
            return
    print('Label not found')
       
def main_storage_menu(storage_filename, main_storage_password):
    while True:
        #print_title()
        print_with_frame(storage_filename, '[]')
        
        print('1) Get password by label')
        print('2) Show labels')
        print('3) Add a new password')
        print('4) Remove a password by label')
        print('5) Return to storage selection')
        print('0) Exit')
        
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
            remove_a_password_by_label(storage_filename, main_storage_password)
            continue
        if choice == '5':
            break
        if choice == '0':
            sys.exit(0)
        
        #In any other case
        #os.system('cls')
            
def login_to_a_storage():
    print('Enter storage filename')
    storage_filename = input()
    if not storage_filename.endswith('.bin'):
        storage_filename += '.bin'
    for file in os.listdir():
        if file.lower() == storage_filename.lower():
            login_to_storage(storage_filename)
            return
    print('Storage not found')

def show_storages():
    for file in os.listdir():
        if file.endswith('.bin'):
            print(file)

def add_a_new_storage():
    print('Enter new storage filename')
    new_storage_filename = input()
    if not new_storage_filename.endswith('.bin'):
        new_storage_filename += '.bin'
    for file in os.listdir():
        if file.lower() == new_storage_filename.lower():
            print('Storage with the same name already exists')
            return
    print('Enter a new password for the storage: ')
    password = getpass()
    print('Retype the password to confirm: ')
    confirm_password = getpass()
    if password == confirm_password:
        create_encrypted_storage(new_storage_filename, password)
    else:
        print('Passwords entered are not equals, the storage has not been created')
    
def remove_a_storage():
    print('Enter filename of the storage to delete')
    storage_filename_to_delete = input()
    if not storage_filename_to_delete.endswith('.bin'):
        storage_filename_to_delete += '.bin'
    for file in os.listdir():
        if file.lower() == storage_filename_to_delete.lower():
            for attempts in range(0,3):
                print('Insert Main Password:')
                password = getpass()
                try:
                    get_decrypted_storage(storage_filename_to_delete, password)
					print("Storage", storage_filename_to_delete, "will be deleted, do you confirm? (y/n)")
					choice = input()
					if choice.lower() == 'y':
						os.remove(storage_filename_to_delete)
					return
                except (KeyError, ValueError):
                    print('Authentication failed')
                    print('Attempts remained: ', 2 - attempts)
                    #scatta foto webcam
                    continue
    print('Storage not found')

def main_menu():
    while True:
        #print_title()
        print()
        print('1) Access to a storage')
        print('2) Show storages')
        print('3) Add a new storage')
        print('4) Remove a storage')
        print('0) Exit')
        
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

#Program Start
print_title()
main_menu()