import subprocess

from sly import Lexer

from BasicExecute import BasicExecute
from BasicLex import BasicLex
from BasicParser import BasicParser
from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
compiler = Tk()
compiler.title('Python EndGame')
file_path = ''

def set_file_path(path):
    global file_path
    file_path = path

def save_as():
    path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
    with open(path, 'w') as file:
        code = editor.get('1.0', END)
        file.write(code)

def open_file():
    path = askopenfilename(filetypes=[('Python Files', '*.py')])
    with open(path, 'r') as file:
        code = file.read()
        editor.delete('1.0', END)
        editor.insert('1.0', code)
        set_file_path(path)

def run():

    if __name__ == '__main__':
        lexer = BasicLex()
        parser = BasicParser()
        env = {}

        text = editor.get('1.0', END)
        code_output.delete('1.0', END)
        if text:
            for x in text.rstrip('\r\n').split("\n"):
                tree = parser.parse(lexer.tokenize(x))
                BasicExecute(tree, env, code_output, x, text.rstrip('\r\n').split("\n")[-1])

menu_bar = Menu(compiler)
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=run)
file_menu.add_command(label='Save As', command=save_as)
file_menu.add_command(label='Exit', command=exit)
menu_bar.add_cascade(label='File', menu=file_menu)

run_bar = Menu(menu_bar, tearoff=0)
run_bar.add_command(label='Run', command=run)
menu_bar.add_cascade(label='Run', menu=run_bar)

compiler.config(menu=menu_bar)
editor = Text()
editor.pack()
code_output = Text(height=13)
code_output.pack()
compiler.mainloop()
"""
import sys
from PyQt6 import QtWidgets, QtCore

app = QtWidgets.QApplication(sys.argv)
widget = QtWidgets.QWidget()
widget.resize(400, 200)
widget.setWindowTitle("This is PyQt Widget example")
widget.show()
exit(app.exec())
"""