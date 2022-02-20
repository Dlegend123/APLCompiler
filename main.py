
import sys
from BasicExecute import BasicExecute
from BasicLex import BasicLex
from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename

from BasicParser import BasicParser

compiler = Tk()
compiler.title('EndGame')
compiler.geometry('650x550+200+200')
compiler.config(highlightbackground='dimgrey', highlightthickness=5)
file_path = ''


def set_file_path(path):
    global file_path
    file_path = path


def save_as():
    if file_path == '':
        path = asksaveasfilename(filetypes=[('Python Files', '*')])
    else:
        path = file_path
    with open(path, 'w') as file:
        code = editor.get('1.0', END)
        file.write(code)
        set_file_path(path)


def open_file():
    path = askopenfilename(filetypes=[('Python Files', '*')])
    with open(path, 'r') as file:
        code = file.read()
        editor.delete('1.0', END)
        editor.insert('1.0', code)
        set_file_path(path)


def run():
    if file_path == '':
        save_prompt = Toplevel()
        text = Label(save_prompt, text='Please save your code')
        text.pack()

        return
    #command = f'python {file_path}'
    #process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if __name__ == '__main__':
        lexer = BasicLex()
        parser = BasicParser()
        pk_exe = Tk()
        pk_exe.title(file_path.split("/")[-1])
        env = {}
        #os.system("start /B start cmd.exe @cmd /k pyinstaller --onefile -w " + file_path.split("/")[-1])
        text = editor.get('1.0', END)
        if text:
            n_editor = Text(pk_exe, background='darkred', fg="white", height=12, highlightthickness=5, highlightbackground='dimgrey')
            n_editor.pack()
            code_output.delete("1.0", END)
            for x in text.rstrip('\r\n').split("\n"):
                tree = parser.parse(lexer.tokenize(x))
                #code_output.insert("1.0", tree)
                n_editor.delete('1.0', END)
                BasicExecute(tree, env, n_editor, code_output)
            #output, error = process.communicate()
        if len(parser.errors) > 0:
            code_output.insert("1.0", "\n")
            for error in parser.errors:
                code_output.insert("1.0", error)
                code_output.insert("1.0", "\n")


menu_bar = Menu(compiler)
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=save_as)
file_menu.add_command(label='Save As', command=save_as)
file_menu.add_command(label='Exit', command=sys.exit)
menu_bar.add_cascade(label='File', menu=file_menu)

run_bar = Menu(menu_bar, tearoff=0)
run_bar.add_command(label='Run', command=run)
menu_bar.add_cascade(label='Run', menu=run_bar)
compiler.config(menu=menu_bar)

editor = Text(bg='#EEC900', fg='black', highlightthickness='1', highlightbackground='dimgrey')
editor.config()
editor.pack()
code_output = Text(height=12, bg='#3B3B3B', fg='white', highlightthickness='1', highlightbackground='dimgrey')
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
