# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 18:07:09 2020

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


def print_with_frame(to_print, frame_char='#', new_line_after=True, new_line_before=True, space_before=0):
    if new_line_before:
        print()
    if len(frame_char) == 1:
        print(space_before * ' ', frame_char * (len(to_print) + 4))
        print(space_before * ' ', frame_char, ' ' * len(to_print), frame_char)
        print(space_before * ' ', frame_char, to_print, frame_char)
        print(space_before * ' ', frame_char, ' ' * len(to_print), frame_char)
        print(space_before * ' ', frame_char * (len(to_print) + 4))
    if len(frame_char) == 2:
        print(space_before * ' ', frame_char * int((len(to_print) / 2) + 4), sep='')
        print(space_before * ' ', frame_char, ' ' * int(len(to_print)), ' ' * (4 - len(to_print) % 2), frame_char, sep='')
        print(space_before * ' ', frame_char, ' ' * (2 - len(to_print) % 2), to_print, ' ' * 2, frame_char, sep='')
        print(space_before * ' ', frame_char, ' ' * int(len(to_print)), ' ' * (4 - len(to_print) % 2), frame_char, sep='')
        print(space_before * ' ', frame_char * int((len(to_print) / 2) + 4), sep='')
    if new_line_after:
        print()


def print_title(enabled_ascii_art=True):
    if enabled_ascii_art:
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
