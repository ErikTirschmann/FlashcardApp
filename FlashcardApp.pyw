import os
import random
import shutil
import sys
import tkinter as tki

from pathlib import Path
from tkinter import ttk
from tkinter.messagebox import showinfo

db_folder = 'Database'
db_backup = 'Backup'

font_tuple = ('Arial', 10)


###############################################################################
# help and support functions
#------------------------------------------------------------------------------
#
def db_showinfo():
    """
    Opens a text window which explains the function of the buttons in the database category
    """
    tki.messagebox.showinfo('Info', '[Button Erstellen]\n\nAktiviert das obere Textfeld um die Eingabe eines Datenbanknamens zu ermöglichen.\n\n\n[Button Bestätigen]\n\nVersucht eine Datenbank zu erstellen die den im oberen Textfeld angegebenen Namen trägt.\n\n\n[Button Entfernen]\n\nEntfernt die momentan aktivierte Datenbank.')

def qu_showinfo():
    """
    Opens a text window which explains the function of the buttons in the question category
    """
    tki.messagebox.showinfo('Info', '[Button Erstellen]\n\nAktiviert das obere und untere Textfeld um die Eingabe einer Frage / Antwort Kombination zu ermöglichen.\n\n\n[Button bestätigen]\n\nVersucht eine Fragen / Antwort Kombination in die momentan aktive Datenbank zu schreiben.\n\n\n[Button Entfernen]\n\nEntfernt die derzeitige Frage / Antwort Kombination aus der momentan aktiven Datenbank.')

def show_help():
    """
    Open the help pdf in the default pdf application of the operating system
    """
    os.startfile('FlashcardApp - Hilfe.pdf')
    
###############################################################################
# hotfixes
#------------------------------------------------------------------------------
#
def return_hotfix(event = None):
    """
    prevent the return key from creating a new line in the upper text box
    """
    if event is None:
        return 'break'
        
def combobox_hotfix(event = None):
    """
    reset the app when changing the database
    """
    clear_and_lock_b()
    if str(bt_create_qu['state']) == 'normal':
        qu_button_lock()
    if str(bt_create_db['state']) == 'normal':
        db_button_lock()

###############################################################################
# file-handling
#------------------------------------------------------------------------------
#
def list_files(file_path):
    """
    creates a list of all files of a type within a folder
    
    file_path      : String  -- folder location to search for files    
    returns        : List    -- all files inside the folder
    """
    if Path(file_path).is_dir():
        return sorted(next(os.walk(file_path))[2])
    else:
        os.mkdir(file_path)
        return []

def slct_files(file_path, file_extension = '.txt'):
    """
    select files by extension
    
    file_path      : String  -- folder location to search for files
    file_extension : String  -- the extension you want to search for
    returns        : List    -- all files with the extension .*
    """
    all_files = list_files(file_path)
    ext_files = []
    for file in range(0, len(all_files)):
        if all_files[file].endswith(file_extension):
            ext_files.append(all_files[file])
    return ext_files
    
def show_files(file_path, file_extension = '.txt'):
    """
    removes the file extension from the strings to output them in a list
    
    file_path      : List    -- folder location to search for files
    file_extension : String  -- the extension you want to remove
    returns        : List    -- a list of filenames withouth extensions
    """
    ext_files = slct_files(file_path)
    cln_files = []
    for file in range(0, len(ext_files)):
        cln_files.append(ext_files[file].replace(file_extension, ''))
    return cln_files
    
def remove_files(bk_folder):
    """
    remove all files of a type from a folder
    
    folder         : String  -- folder location where the files are
    files          : List    -- files in the bk_folder 
    """
    files = slct_files(bk_folder)
    for file in range(0, len(files)):
        os.remove(os.path.join(bk_folder, files[file]))
        
def copy_files(db_folder, bk_folder):
    """
    copy all files from one folder to another
    
    db_folder: String -- name of the database folder
    bk_folder: String -- name of the backup folder
    files    : List   -- files in the db_folder
    """
    files = slct_files(db_folder)
    for file in range(0, len(files)):
        shutil.copyfile(os.path.join(db_folder, files[file]), os.path.join(bk_folder, files[file]))
        
def create_backup():
    """
    create a backup of the database
    """
    remove_files(db_backup)
    copy_files(db_folder, db_backup)

def db_create():
    """
    create a new database file
    """
    if Path(db_folder).is_dir() and len(tb_question.get('1.0', 'end')) > 3:
        file_name = os.path.join(db_folder, str.strip(tb_question.get('1.0', 'end')) + '.txt')
        try:
            with open(file_name, 'x', encoding = 'utf-8') as f:
                f.close()
            clear_and_lock(tb_question)
            tb_question.configure(background = '#eceff4')
            cb_select_db['values'] = sorted(show_files(db_folder))
        except OSError:
            tki.messagebox.showerror('Fehler', f'{file_name} existiert bereits!')
            clear_and_lock(tb_question)
            tb_question.configure(background = '#eceff4')
            
def db_remove():
    """
    remove a selected database
    """
    if cb_select_db.get() != '' and tki.messagebox.askquestion('Achtung', f'Möchten sie {cb_select_db.get()} wirklich unwiederruflich löschen?') == 'yes':
        os.remove(os.path.join(db_folder, cb_select_db.get() + '.txt'))
        cb_select_db.set('')
        cb_select_db['values'] = sorted(list_files(db_folder))
    else:
        tki.messagebox.showerror('Fehler', 'Keine Datenbank ausgewählt!')
        
###############################################################################
# data-handling
#------------------------------------------------------------------------------
#
def read_lines(file):
    """
    return the lines in a textfile
    
    file           : String  -- name of the file you want to read
    returns        : List    -- All lines of the file
    """
    with open(file, 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
        f.close()
        return lines
        
def write_lines(file, lines):
    """
    write a list of lines to a file
    
    file           : String  -- name of the file you want to write
    lines          : List    -- List of strings you want to write line by line
    """
    with open(file, 'w', encoding = 'utf-8') as f:
        f.writelines(lines)
        f.close()
        
def already_used(lines, value):
    """
    check if a value already exists in a file
    
    lines          : List    -- List of strings you want to search for
    value          : String  -- a text sniped you're lookin for
    """
    for line in range(len(lines)):
        if lines[line].split('###')[0] == value:
            tki.messagebox.showerror('Fehler', f'{qust} ist bereits in der Datenbank enthalten!')
            return True
            
def remove_line(lines):
    """
    remove the line in the question textbox from a list of lines
    
    lines          : List    -- list of lines
    """
    for line in lines:
        if line.startswith(tb_question.get('1.0', 'end').strip()):
            lines.remove(line)
    return lines

def qu_create():
    """
    create a new quest in the selected database
    """
    if len(tb_question.get('1.0', 'end')) > 1 and len(tb_question.get('1.0', 'end')) > 1:
        file = os.path.join(db_folder, str.strip(cb_select_db.get()) + '.txt')
        try:
            question = str.strip(tb_question.get('1.0', 'end'))
            answer = str.strip(tb_answer.get('1.0', 'end')).replace('\n', ';;;')
            lines = read_lines(file)
            if already_used(lines, question) != True:
                lines.append(f'{question}###{answer}\n')
                write_lines(file, lines)
                clear_and_lock_b()
        except FileNotFoundError:
            tki.messagebox.showerror('Fehler', 'Keine Datenbank ausgewählt!')
            
def qu_remove():
    """
    remove a quest from the selected database
    """
    if len(tb_question.get('1.0', 'end')) > 3 :
        if tki.messagebox.askquestion('Achtung', 'Möchten sie den Eintrag {0} wirklich entfernen?'.format(tb_question.get('1.0', 'end').strip())) == 'yes':
            file_name = os.path.join(db_folder, str.strip(cb_select_db.get() + '.txt'))
            lines = read_lines(file_name)
            with open(file_name, 'w', encoding = 'utf-8') as f:
                f.writelines(remove_line(lines))
                f.close()
            clear_and_lock_b()
            
def qu_show():
    """
    show a question in the question textbox
    """
    try:
        file = os.path.join(db_folder, str.strip(cb_select_db.get() + '.txt'))
        lines = read_lines(file)
        if len(lines) == 0:
            tki.messagebox.showerror('Fehler', 'Die Datenbank enthält keinen Inhalt!')
            return
        # make sure it's not the same question
        elif len(lines) > 1:
            question = lines[random.randint(0, len(lines) - 1)].split('###')[0]
            while question == tb_question.get('1.0', 'end').strip():
                question = lines[random.randint(0, len(lines) - 1)].split('###')[0]
        else:
            question = lines[0]
        clear_and_lock(tb_answer)
        clear_content(tb_question)
        tb_question.insert('1.0', question)
        tb_question['state'] = 'disabled'
    except FileNotFoundError:
        tki.messagebox.showerror('Fehler', 'Keine Datenbank ausgewählt!')
        
def an_show():
    """
    show the answer for the question in the question box inside the answer box
    """
    file = os.path.join(db_folder, str.strip(cb_select_db.get() + '.txt'))
    lines = read_lines(file)
    for line in lines:
        if line.startswith(tb_question.get('1.0', 'end').strip()):
            clear_content(tb_answer)
            parts = line.split('###')[1].strip().split(';;;')
            for part in range(0, len(parts)):
                tb_answer.insert('1.0', (parts[part] + '\n'))
            tb_answer['state'] = 'disabled'

###############################################################################
# surface-interactions
#------------------------------------------------------------------------------
#
def clear_content(_object):
    """
    removes the shown text of an object
    """
    _object['state'] = 'normal'
    _object.delete('1.0', 'end')

def clear_and_lock(_object):
    """
    removes the shown text of an object and locks it
    """
    clear_content(_object)
    _object['state'] = 'disabled'
    _object.configure(background = '#eceff4')
    
def clear_and_lock_b():
    """
    reset both textboxes
    """
    clear_and_lock(tb_question)
    clear_and_lock(tb_answer)

def db_button_lock():
    """
    lock all the buttons used for database interactions
    """
    clear_and_lock(tb_question)
    clear_and_lock(tb_answer)
    # lock the question buttons before handling with the database
    if str(bt_create_qu['state']) == 'normal':
        qu_button_lock()
    if str(bt_create_db['state']) == 'disabled':
        if tki.messagebox.askquestion('Warnung', 'Möchte sie wirklich die Datenbanken bearbeiten?') == 'yes':
            bt_create_db['state'] = bt_remove_db['state'] = bt_accept_db['state'] = 'normal'
            lb_database.config(background = '#bf616a')
            tb_question['state'] = tb_answer['state'] = 'disabled'
    else:
        bt_create_db['state'] = bt_remove_db['state'] = bt_accept_db['state'] = 'disabled'
        lb_database.config(background = '#a3be8c')

def qu_button_lock():
    """
    lock all the buttons used for question interactions
    """
    # lock the database buttons before handling with the questions
    if str(bt_create_db['state']) == 'normal':
        db_button_lock()
    if str(bt_create_qu['state']) == 'disabled':
        if tki.messagebox.askquestion('Warnung', 'Möchten sie wirklich die Fragen bearbeiten?') == 'yes':
            bt_create_qu['state'] = bt_remove_qu['state'] = bt_accept_qu['state'] = 'normal'
            lb_question.config(background = '#bf616a')
    else:
        bt_create_qu['state'] = bt_remove_qu['state'] = bt_accept_qu['state'] = 'disabled'
        lb_question.config(background = '#a3be8c')
        clear_and_lock(tb_question)
        clear_and_lock(tb_answer)

def db_create_input():
    """
    prepare the textboxes for input of database files
    """
    qu_create_input()
    tb_answer.configure(background = '#eceff4')
    tb_answer['state'] = 'disabled'
    tb_question.configure(background = '#ffffff')
    
def qu_create_input():
    """
    prepare the textboxes for input of question files
    """
    clear_content(tb_question)
    clear_content(tb_answer)
    tb_question.focus_set()
    tb_question.configure(background = '#ffffff')
    tb_answer.configure(background = '#ffffff')

###############################################################################
# surface and main-loop
#------------------------------------------------------------------------------
#
if __name__ == '__main__':
    root = tki.Tk()
    # window size, and position on the screen
    window_w = 550
    window_h = 310
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    center_x = int(screen_w / 2 - window_w / 2)
    center_y = int(screen_h / 2 - window_h / 2)

    root.title('Flashcards')
    root.iconbitmap('Pictures/icon.ico')
    root.geometry(f'{window_w}x{window_h}+{center_x}+{center_y}')
    root.resizable(False, False)
    ###------------------------------------------------------------------------
    ### grid setup
    root.columnconfigure(0, weight = 1) # wide buttons
    root.columnconfigure(1, weight = 1) # *
    root.columnconfigure(2, weight = 1) # *
    root.columnconfigure(3, weight = 2) # labels
    root.columnconfigure(4, weight = 1) # slim buttons
    root.columnconfigure(5, weight = 1) # *
    ###------------------------------------------------------------------------
    ### row 1: database selection
    sv_select_db = tki.StringVar()
    cb_select_db = ttk.Combobox(root, textvariable = sv_select_db)
    cb_select_db['values'] = show_files(db_folder)
    cb_select_db['state'] = 'readonly'
    cb_select_db.grid(column = 0, row = 1, padx = 5, pady = 5, columnspan = 6, sticky = 'ew')
    ###------------------------------------------------------------------------
    ### row 2: database handling
    bt_create_db = ttk.Button(root, text = 'Erstellen', width = 15, state = 'disabled', command = db_create_input)
    bt_create_db.grid(column = 0, row = 2, padx = 5, pady = 5, sticky = 'w')
    bt_remove_db = ttk.Button(root, text = 'Entfernen', width = 15, state = 'disabled', command = db_remove)
    bt_remove_db.grid(column = 1, row = 2, padx = 0, pady = 5, sticky = 'w')
    bt_accept_db = ttk.Button(root, text = "Bestätigen", width = 15, state = 'disabled', command = db_create)
    bt_accept_db.grid(column = 2, row = 2, padx = 5, pady = 5, sticky = 'w')
    lb_database = ttk.Label(root, text = 'Datenbank', width = 35, borderwidth = 3, anchor = 'center', relief = 'sunken', background = '#a3be8c')
    lb_database.grid(column = 3, row = 2, padx = 5, pady = 5, ipady = 3, sticky = 'e')
    bt_help_db = ttk.Button(root, text = '⌘', width = 5, command = db_showinfo)
    bt_help_db.grid(column = 4, row = 2, padx = 0, pady = 5, sticky = 'e')
    bt_lock_db = ttk.Button(root, text = '🕱', width = 5, command = db_button_lock)
    bt_lock_db.grid(column = 5, row = 2, padx = 5, pady = 5, sticky = 'e')
    ###------------------------------------------------------------------------
    ### row 3: question handling
    bt_create_qu = ttk.Button(root, text = 'Erstellen', width = 15, state = 'disabled', command = qu_create_input)
    bt_create_qu.grid(column = 0, row = 3, padx = 5, pady = 5, sticky = 'w')
    bt_remove_qu = ttk.Button(root, text = 'Entfernen', width = 15, state = 'disabled', command = qu_remove)
    bt_remove_qu.grid(column = 1, row = 3, padx = 0, pady = 5, sticky = 'w')
    bt_accept_qu = ttk.Button(root, text = "Bestätigen", width = 15, state = 'disabled', command = qu_create)
    bt_accept_qu.grid(column = 2, row = 3, padx = 5, pady = 5, sticky = 'w')
    lb_question = ttk.Label(root, text = 'Fragen', width = 35, anchor = 'center', borderwidth = 3, relief = 'sunken', background = '#a3be8c')
    lb_question.grid(column = 3, row = 3, padx = 5, pady = 5, ipady = 3, sticky = 'e')
    bt_help_qu = ttk.Button(root, text = '⌘', width = 5, command = qu_showinfo)
    bt_help_qu.grid(column = 4, row = 3, padx = 0, pady = 5, sticky = 'e')
    bt_lock_qu = ttk.Button(root, text = '🕱', width = 5, command = qu_button_lock)
    bt_lock_qu.grid(column = 5, row = 3, padx = 5, pady = 5, sticky = 'e')
    ###------------------------------------------------------------------------
    ### row 4: question textbox
    tb_question = tki.Text(root, height = 1, state = 'disabled')
    tb_question.grid(column = 0, row = 4, padx = 5, pady = 5, columnspan = 6, sticky = 'ew')
    tb_question.configure(font = font_tuple, background = '#eceff4')
    ###------------------------------------------------------------------------
    ### row 5: answer textbox
    tbs_frame = tki.Frame(root)
    tbs_frame.columnconfigure(0, weight = 1) # Reihe für Textbox und Scrollbar
    tbs_frame.grid(column = 0, row = 5, padx = 5, pady = 5, columnspan = 6, sticky = 'ew')
    tb_answer = tki.Text(tbs_frame, height = 8, wrap = 'word', state = 'disabled')
    tb_answer.grid(column = 0, row = 0, padx = 0, pady = 0, sticky = 'ew')
    tb_answer.configure(font = font_tuple, background = '#eceff4')
    sb_answer = ttk.Scrollbar(tbs_frame, orient = 'vertical', command = tb_answer.yview)
    sb_answer.grid(column = 1, row = 0, padx = 0, pady = 0, sticky = 'nse')
    tb_answer['yscrollcommand'] = sb_answer.set
    ###------------------------------------------------------------------------
    ### row 6: question/answer handling, help, backup
    bt_next = ttk.Button(root, text = 'Frage', width = 15, command = qu_show)
    bt_next.grid(column = 0, row = 6, padx = 5, pady = 5, sticky = 'w')
    bt_answer = ttk.Button(root, text = 'Antwort', width = 15, command = an_show)
    bt_answer.grid(column = 1, row = 6, padx = 0, pady = 5, sticky = 'w')
    bt_help_fi = ttk.Button(root, text = '？', width = 5, command = show_help)
    bt_help_fi.grid(column = 4, row = 6, padx = 0, pady = 5, sticky = 'e')
    bt_backup = ttk.Button(root, text = '☁', width = 5, command = create_backup)
    bt_backup.grid(column = 5, row = 6, padx = 5, pady = 5, sticky = 'e')
    ###------------------------------------------------------------------------
    ### return hotfix
    tb_question.bind('<Return>', lambda e: return_hotfix())
    cb_select_db.bind('<<ComboboxSelected>>', lambda e: combobox_hotfix())
    


    root.mainloop()
