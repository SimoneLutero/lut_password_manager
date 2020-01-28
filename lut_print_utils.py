# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 18:07:09 2020

@author: SimoneLutero
"""

def print_with_frame(to_print, frame_char='#', new_line_after=True, new_line_before=True):
    if new_line_before:
        print()
    if len(frame_char) == 1:
        print(frame_char*(len(to_print)+4))
        print(frame_char,' '*len(to_print), frame_char)
        print(frame_char, to_print, frame_char)
        print(frame_char,' '*len(to_print), frame_char)
        print(frame_char*(len(to_print)+4))
    if len(frame_char) == 2:
        print(frame_char*int((len(to_print)/2) + 4))
        print(frame_char,' '*int(len(to_print)), ' '*(4-len(to_print)%2),frame_char, sep='')
        print(frame_char,' '*(2-len(to_print)%2), to_print, ' '*2, frame_char, sep='')
        print(frame_char,' '*int(len(to_print)), ' '*(4-len(to_print)%2), frame_char, sep='')
        print(frame_char*int((len(to_print)/2) + 4))
    if new_line_after:
        print()
        
def print_title(enabledAsciiArt=True):
    if enabledAsciiArt:
        print("""
                ▓██▓     ██   ██ ████████▓    ██▓███   ▄▄▄        ██████   ██████  █     █░ ▒█████   ██▀███  ▓█████▄ 
                ▓██▒     ██  ▓██▒▓  ██▒ ▓▒   ▓██░  ██▒▒████▄    ▒██    ▒ ▒██    ▒ ▓█░ █ ░█░▒██▒  ██▒▓██ ▒ ██▒▒██▀ ██▌
                ▒██░    ▓██  ▒██░▒ ▓██░ ▒░   ▓██░ ██▓▒▒██  ▀█▄  ░ ▓██▄   ░ ▓██▄   ▒█░ █ ░█ ▒██░  ██▒▓██ ░▄█ ▒░██   █▌
                ▒██░    ▓▓█  ░██░░ ▓██▓ ░    ▒██▄█▓▒ ▒░██▄▄▄▄██   ▒   ██▒  ▒   ██▒░█░ █ ░█ ▒██   ██░▒██▀▀█▄  ░▓█▄   ▌
                ░██████▒▒▒█████▓   ▒██▒ ░    ▒██▒ ░  ░ ▓█   ▓██▒▒██████▒▒▒██████▒▒░░██▒██▓ ░ ████▓▒░░██▓ ▒██▒░▒████▓ 
                ░ ▒░   ░░▒ ▒ ▒ ▒   ▒ ░░      ▒ ▒░ ░  ░ ▒▒    ▒ ░▒ ▒ ▒ ▒ ░▒ ▒ ▒ ▒ ░░  ░▒ ▒  ░ ▒░▒░▒░ ░ ▒  ░ ░ ▒▒   ▒ 
                
                                   ███▄ ▄███▓ ▄▄▄       ███▄    █  ▄▄▄        ▄████ ▓█████  ██▀███                   
                                  ▓██▒▀█▀ ██▒▒████▄     ██ ▀█   █ ▒████▄     ██▒ ▀█▒▓█   ▀ ▓██ ▒ ██▒                 
                                  ▓██    ▓██░▒██  ▀█▄  ▓██  ▀█ ██▒▒██  ▀█▄  ▒██░▄▄▄░▒███   ▓██ ░▄█ ▒                 
                                  ▒██    ▒██ ░██▄▄▄▄██ ▓██▒  ▐▌██▒░██▄▄▄▄██ ░▓█  ██▓▒▓█  ▄ ▒██▀▀█▄                   
                                  ▒██▒   ░██▒ ▓█   ▓██▒▒██░   ▓██░ ▓█   ▓██▒░▒▓███▀▒░▒████▒░██▓ ▒██▒                 
                                  ░ ▒░   ░  ░ ▒▒    ▒ ░░ ▒░   ▒ ▒  ▒▒    ▒ ░ ░▒   ▒ ░░ ▒░ ░░ ▒  ░▒ ░                 
                                                      
        """)
    else:
        print("Lut Password Manager")
    