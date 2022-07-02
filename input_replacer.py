from sys import argv
import os
from pathlib import Path

script = argv

def input_replacer (file, text_to_be_replace, text_to_replace_it_with):
    """This replace the chosen word in a txt file"""
    with open(file, 'r') as f:
        file_data = f.read()
    
    file_data = file_data.replace(text_to_be_replace, text_to_replace_it_with)
    
    with open(file, 'w') as f:
        f.write(file_data)
        print (f"{file} has been changed")
        f.close()

def name_changer_txt_to_com (file):
    """This changes the file type from '.txt' to '.com'"""
    p = Path(file)
    if file.endswith('.txt'):
        p.rename(p.with_suffix('.com'))

def name_changer_com_to_txt (file):
    """This changes the file type from '.com' to '.txt'"""
    p = Path(file)
    if file.endswith('.com'):
        p.rename(p.with_suffix('.txt'))

print("Text to be replace:>", end = ' ')
text_to_be_replace = input()
print("text to replace it with:>", end = ' ')
text_to_replace_it_with = input()
print(f"Are you sure you want to change {text_to_be_replace} to {text_to_replace_it_with}? [y/n]", end = ' ')
reaffirm = input()

if reaffirm == "y":
    for filename in os.listdir():
        if filename.endswith(".com"):
            input_replacer (filename,text_to_be_replace,text_to_replace_it_with)
            
        if filename.endswith('.txt'):
            input_replacer (filename,text_to_be_replace,text_to_replace_it_with)
            name_changer_txt_to_com(filename)
elif reaffirm == "n":
    quit()
