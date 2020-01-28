# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 18:03:08 2020

@author: SimoneLutero
"""

import json
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def test_encrypt_decrypt():
    
    #Encrypt
    print('Encryption Phase')
    
    #Generates key used for encryption
    key = get_random_bytes(16)
    
    print('key is: ', key)
    print()
    
    #Instantiates AES cipher for encryption
    cipher = AES.new(key, AES.MODE_CBC)
    
    data = [('w3', 'mail', 'pwd'), ('notes', 'mail', 'pwd')]
    print('data is: ', data)
    print()
    
    data_json = json.dumps(data)
    print('data_json is: ', data_json)
    print()
    
    data_json_encoded = data_json.encode('utf8')
    print('data_json_encoded is: ', data_json_encoded)
    print()
    
    data_padded = pad(data_json_encoded, AES.block_size)
    print('data_padded is: ', data_padded)
    print()
    
    data_encrypted = cipher.encrypt(data_padded)
    print('data_encrypted is: ', data_encrypted)
    print()
    
    print('cipher.iv is: ', cipher.iv)
    print()
    
    # iv_encoded = b64encode(cipher.iv).decode('utf-8')
    # print('iv_encoded is: ', iv_encoded)
    # print()
    
    # ciphertext = b64encode(data_encrypted).decode('utf-8')
    # print('ciphertext is: ', ciphertext)
    # print(
    
    # result_json = json.dumps({'iv':iv_encoded, 'ciphertext':ciphertext})
    # print('result_json is: ', result_json)
    # print()
    
    output_file = open('pwd_storage.bin', 'wb')
    output_file.write(cipher.iv)
    output_file.write(data_encrypted)
    output_file.close()
    
    #Decrypt
    print('Decryption Phase')
    
    # json_input = result_json
    # print('json_input is: ', json_input)
    # print()
    
    try:
        # b64 = json.loads(json_input)
        # print('b64 is: ', b64)
        # print()
        
        # print('iv_encoded is: ', b64['iv'])
        # print()
        
        input_file = open('pwd_storage.bin', 'rb')
        
        #iv = b64decode(b64['iv'])
        iv = input_file.read(16)
        print('iv is: ', iv)
        print()
        
        #ciphertext = b64decode(b64['ciphertext'])
        ciphertext = input_file.read()
        print('ciphertext is: ', ciphertext)
        print()
        
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        data_decrypted = cipher.decrypt(ciphertext)
        print('data_decrypted: ', data_decrypted)
        print()
        
        data_unpadded = unpad(data_decrypted, AES.block_size)
        print('data_unpadded: ', data_unpadded)
        print()
        
        data_decoded = data_unpadded.decode('utf8')
        print('data_decoded: ', data_decoded)
        print()
        
        data = json.loads(data_decoded)
        print('data is: ', data)
        print()
        
        print('data[0] is: ', data[0])
        print()
        
        print('data[0][0] is: ', data[0][0])
        print()
        
    except (KeyError, ValueError) as e:
        print("Incorrect decryption, error: ", e)
