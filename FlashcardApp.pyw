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

tb_color_ds = '#F2F3F5'     # bg-color of the disabled textbox
tb_color_en = '#ffffff'     # bg-color of the enabled textbox
lb_color_rd = '#FF6E4A'     # bg-color of the red label (db and questions)
lb_color_gn = '#A8E4A0'     # bg-color of the green label (db and questions)
fr_color_db = '#E5E4E2'     # bg-color of the frames

font_tuple = ('Arial', 10)  # font for the question / answer textbox

###############################################################################
# help and support functions
#------------------------------------------------------------------------------
#
def show_help():
    """Open help pdf in the default application of os."""
    os.startfile('FlashcardApp - Hilfe.pdf')

###############################################################################
# hotfixes
#------------------------------------------------------------------------------
#
def return_hotfix(event = None):
    """Prevent a newline inside the question textbox."""
    if event is None:
        return 'break'

def combobox_hotfix(event = None):
    """Reset the interface when changing the database."""
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
    """List all files inside a folder.

    Args:
        file_path: the folder path as string
    Returns:
        A list.
    """
    if Path(file_path).is_dir():
        return sorted(next(os.walk(file_path))[2])
    else:
        os.mkdir(file_path)
        return []

def slct_files(file_path, file_extension = '.txt'):
    """List all * files inside a folder.

    Args:
        file_path: the folder path as string
        file_extension: the extension youre lookin for
    Returns:
        A list.
    """
    ext_files = []
    for file in list_files(file_path):
        if file.endswith(file_extension):
            ext_files.append(file)
    return ext_files

def show_files(file_path, file_extension = '.txt'):
    """Remove the file extension in a list of files.

    Args:
        file_path: the folder path as string
        file_extension: the extension you want to remove
    Returns:
        A list.
    """
    files_new = []
    for file in slct_files(file_path):
        files_new.append(file.replace(file_extension, ''))
    return files_new

def remove_files(file_path):
    """Remove all * files of a folder.

    Args:
        file_path: the folder path as string
    """
    for file in slct_files(file_path):
        os.remove(os.path.join(file_path, file))

def copy_files(database_folder, backup_folder):
    """Copy files from one folder to another.

    Args:
        database_folder: the folder path as string
        backup_folder: the folder path as string
    """
    for file in slct_files(database_folder):
        shutil.copyfile(os.path.join(database_folder, file), os.path.join(backup_folder, file))

def create_backup():
    """Create a backup of the database."""
    remove_files(db_backup)
    copy_files(db_folder, db_backup)

def db_create():
    """Create a new database file."""
    if len(tb_question.get('1.0', 'end')) > 1:
        file_name = os.path.join(db_folder, str.strip(tb_question.get('1.0', 'end')) + '.txt')
        try:
            create_file(file_name)
            cb_select_db['values'] = show_files(db_folder)
        except OSError:
            tki.messagebox.showerror('Fehler', f'{file_name} existiert bereits!')
        clear_and_lock(tb_question)

def db_remove():
    """Remove a database."""
    if cb_select_db.get() != '' and tki.messagebox.askquestion('Achtung', f'Möchten sie {cb_select_db.get()} wirklich unwiederruflich löschen?') == 'yes':
        os.remove(os.path.join(db_folder, cb_select_db.get() + '.txt'))
        cb_select_db.set('')
        cb_select_db['values'] = show_files(db_folder)
    else:
        tki.messagebox.showerror('Fehler', 'Keine Datenbank ausgewählt!')

###############################################################################
# data-handling
#------------------------------------------------------------------------------
#
def create_file(file_name):
    """Create a new file.

    Args:
        file: name of the textfile as string.
    """
    with open(file_name, 'x', encoding = 'utf-8') as f:
        f.close()

def read_lines(file):
    """Return the lines of a textfile.

    Args:
        file: name of the textfile as string
    Returns:
        A list.
    """
    with open(file, 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
        f.close()
        return lines

def write_lines(file, lines):
    """Write a list of lines to a file.
    Args:
        file: name of the textfile as string
        lines: list of lines
    """
    with open(file, 'w', encoding = 'utf-8') as f:
        f.writelines(lines)
        f.close()

def already_used(lines, value):
    """Check if a snipet already is used as question.

    Args:
        lines: list of lines
        value: a string sniped you search for
    Returns:
        A boolean.
    """
    for line in lines:
        if line.startswith(value):
            tki.messagebox.showerror('Fehler', f'{value} ist bereits in der Datenbank enthalten!')
            return True

def remove_line(lines):
    """Remove a line that startswith the textbox content.

    Args:
        lines: list of lines
    Returns:
        A list.
    """
    for line in lines:
        if line.startswith(tb_question.get('1.0', 'end').strip()):
            lines.remove(line)
    return lines

def qu_create():
    """Add a new set to the database."""
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
    """Remove a set from the database."""
    if len(tb_question.get('1.0', 'end')) > 1 :
        if tki.messagebox.askquestion('Achtung', 'Möchten sie den Eintrag {0} wirklich entfernen?'.format(tb_question.get('1.0', 'end').strip())) == 'yes':
            file_name = os.path.join(db_folder, str.strip(cb_select_db.get() + '.txt'))
            write_lines(file_name, remove_line(read_lines(file_name)))
            clear_and_lock_b()

def qu_show():
    """Show a question."""
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
            question = lines[0].split('###')[0]
        clear_and_lock(tb_answer)
        clear_content(tb_question)
        tb_question.insert('1.0', question)
        tb_question.configure(background = tb_color_ds)
        tb_question['state'] = 'disabled'
    except FileNotFoundError:
        tki.messagebox.showerror('Fehler', 'Keine Datenbank ausgewählt!')

def an_show():
    """show the answer."""
    file = os.path.join(db_folder, str.strip(cb_select_db.get() + '.txt'))
    for line in read_lines(file):
        if line.startswith(tb_question.get('1.0', 'end').strip()):
            clear_content(tb_answer)
            parts = line.split('###')[1].strip().split(';;;')
            for part in parts:
                tb_answer.insert('1.0', part + '\n')
            tb_answer.configure(background = tb_color_ds)
            tb_answer['state'] = 'disabled'

###############################################################################
# surface-interactions
#------------------------------------------------------------------------------
#
def hide_buttons():
    """Hide the database and question buttons.
    """
    db_button_fr.grid_remove()
    update_winsize()

def show_buttons():
    """Show the database and question buttons.
    """
    db_button_fr.grid()
    update_winsize()

def toggle_buttons():
    """Enable / disable the database and question buttons
    """
    print(db_button_fr.winfo_ismapped())
    if db_button_fr.winfo_ismapped() == 1:
        hide_buttons()
        bt_toggle.configure(text = '⇊')
    else:
        show_buttons()
        bt_toggle.configure(text = '⇈')

def update_winsize():
    """Update the size of the window
    """
    root.update_idletasks()
    window_w = 550
    window_h = root.winfo_reqheight()
    root.geometry(f'{window_w}x{window_h}')

def clear_content(_object):
    """Clear the text value.

    Args:
        _object: a tk/ttk object
    """
    _object['state'] = 'normal'
    _object.delete('1.0', 'end')
    _object.configure(background = tb_color_en)

def clear_and_lock(_object):
    """Clear the text value and set the object to read only.

    Args:
        _object: a tk/ttk object
    """
    clear_content(_object)
    _object['state'] = 'disabled'
    _object.configure(background = tb_color_ds)

def clear_content_b():
    """Clear both textboxes."""
    clear_content(tb_question)
    clear_content(tb_answer)

def clear_and_lock_b():
    """Clear both textboxes and lock em."""
    clear_and_lock(tb_question)
    clear_and_lock(tb_answer)

def db_button_lock():
    """Lock all buttons for database modification."""
    clear_and_lock(tb_question)
    clear_and_lock(tb_answer)
    # lock the question buttons before handling with the database
    if str(bt_create_qu['state']) == 'normal':
        qu_button_lock()
    if str(bt_create_db['state']) == 'disabled':
        if tki.messagebox.askquestion('Warnung', 'Möchte sie wirklich die Datenbanken bearbeiten?') == 'yes':
            bt_create_db['state'] = bt_remove_db['state'] = bt_accept_db['state'] = 'normal'
            lb_database.config(background = lb_color_rd)
            tb_question['state'] = tb_answer['state'] = 'disabled'
    else:
        bt_create_db['state'] = bt_remove_db['state'] = bt_accept_db['state'] = 'disabled'
        lb_database.config(background = lb_color_gn)

def qu_button_lock():
    """Lock all buttons for question modification."""
    # lock the database buttons before handling with the questions
    if str(bt_create_db['state']) == 'normal':
        db_button_lock()
    if str(bt_create_qu['state']) == 'disabled':
        if tki.messagebox.askquestion('Warnung', 'Möchten sie wirklich die Fragen bearbeiten?') == 'yes':
            bt_create_qu['state'] = bt_remove_qu['state'] = bt_accept_qu['state'] = 'normal'
            lb_question.config(background = lb_color_rd)
    else:
        bt_create_qu['state'] = bt_remove_qu['state'] = bt_accept_qu['state'] = 'disabled'
        lb_question.config(background = lb_color_gn)
        clear_and_lock(tb_question)
        clear_and_lock(tb_answer)

def db_create_input():
    """Prepare both textboxes for the database input."""
    qu_create_input()
    clear_and_lock(tb_answer)

def qu_create_input():
    """Prepare both textboxes for the question input"""
    clear_content_b()
    tb_question.focus_set()

###############################################################################
# surface and main-loop
#------------------------------------------------------------------------------
#
if __name__ == '__main__':
    root = tki.Tk()

    root.columnconfigure(0, weight = 1)

    """line 1: combobox

        list all files inside the database folder, select select a file
    """
    sv_select_db = tki.StringVar()
    cb_select_db = ttk.Combobox(root, textvariable = sv_select_db)
    cb_select_db['values'] = show_files(db_folder)
    cb_select_db['state'] = 'readonly'
    cb_select_db.grid(column = 0, row = 0, padx = 5, pady = 5, sticky = 'ew')

    """line 2 + 3: button-frame

        a frame to place the database and question buttons on the grid
    """
    db_button_fr = tki.Frame(root, borderwidth = 1, relief = 'sunken', background = fr_color_db)
    db_button_fr.grid(column = 0, row = 1, padx = 5, pady = 0, sticky = 'ew')

    db_button_fr.columnconfigure(0, weight = 1)
    db_button_fr.columnconfigure(1, weight = 1)
    db_button_fr.columnconfigure(2, weight = 1)
    db_button_fr.columnconfigure(3, weight = 2)
    db_button_fr.columnconfigure(4, weight = 1)

    """line 2: database buttons

        create and remove databases, label, lock buttons
    """
    bt_create_db = ttk.Button(db_button_fr, text = 'Erstellen', width = 15, state = 'disabled', command = db_create_input)
    bt_create_db.grid(column = 0, row = 0, padx = 5, pady = 5)
    bt_remove_db = ttk.Button(db_button_fr, text = 'Entfernen', width = 15, state = 'disabled', command = db_remove)
    bt_remove_db.grid(column = 1, row = 0, padx = 0, pady = 5)
    bt_accept_db = ttk.Button(db_button_fr, text = "Bestätigen", width = 15, state = 'disabled', command = db_create)
    bt_accept_db.grid(column = 2, row = 0, padx = 5, pady = 5)
    lb_database = ttk.Label(db_button_fr, text = 'Datenbank', width = 30, borderwidth = 3, anchor = 'center', relief = 'sunken', background = lb_color_gn)
    lb_database.grid(column = 3, row = 0, padx = 0, pady = 5, ipady = 3)
    bt_lock_db = ttk.Button(db_button_fr, text = '🕱', width = 3, command = db_button_lock)
    bt_lock_db.grid(column = 5, row = 0, padx = 5, pady = 5)

    """line 3: question-buttons

        create and remove question, label, lock buttons
    """
    bt_create_qu = ttk.Button(db_button_fr, text = 'Erstellen', width = 15, state = 'disabled', command = qu_create_input)
    bt_create_qu.grid(column = 0, row = 1, padx = 5, pady = 5)
    bt_remove_qu = ttk.Button(db_button_fr, text = 'Entfernen', width = 15, state = 'disabled', command = qu_remove)
    bt_remove_qu.grid(column = 1, row = 1, padx = 0, pady = 5)
    bt_accept_qu = ttk.Button(db_button_fr, text = "Bestätigen", width = 15, state = 'disabled', command = qu_create)
    bt_accept_qu.grid(column = 2, row = 1, padx = 5, pady = 5)
    lb_question = ttk.Label(db_button_fr, text = 'Fragen', width = 30, anchor = 'center', borderwidth = 3, relief = 'sunken', background = lb_color_gn)
    lb_question.grid(column = 3, row = 1, padx = 0, pady = 5, ipady = 3)
    bt_lock_qu = ttk.Button(db_button_fr, text = '🕱', width = 3, command = qu_button_lock)
    bt_lock_qu.grid(column = 5, row = 1, padx = 5, pady = 5)

    """line 4: question-textbox
    """
    tb_question = tki.Text(root, height = 1, state = 'disabled', borderwidth = 1, relief = 'sunken')
    tb_question.grid(column = 0, row = 4, padx = 5, pady = 5, ipadx = 5, sticky = 'ew')
    tb_question.configure(font = font_tuple, background = tb_color_ds)

    """line 5: answer-textbox
    """
    tbs_frame = tki.Frame(root)
    tbs_frame.grid(column = 0, row = 5, padx = 5, pady = 0, columnspan = 6, sticky = 'ew')
    tbs_frame.columnconfigure(0, weight = 1)

    tb_answer = tki.Text(tbs_frame, height = 10, wrap = 'word', state = 'disabled', borderwidth = 1, relief = 'sunken')
    tb_answer.grid(column = 0, row = 0, padx = 0, pady = 0, ipadx = 5, sticky = 'ew')
    tb_answer.configure(font = font_tuple, background = tb_color_ds)
    sb_answer = ttk.Scrollbar(tbs_frame, orient = 'vertical', command = tb_answer.yview)
    sb_answer.grid(column = 1, row = 0, padx = 0, pady = 0, sticky = 'nse')
    tb_answer['yscrollcommand'] = sb_answer.set

    """ line 6: controll-buttons

        show question, show answer, help, backup
    """
    cn_button_fr = tki.Frame(root, borderwidth = 1, relief = 'sunken', background = fr_color_db)
    cn_button_fr.grid(column = 0, row = 6, padx = 5, pady = 5, sticky = 'ew')

    cn_button_fr.columnconfigure(0, weight = 1)

    bt_next = ttk.Button(cn_button_fr, text = 'Frage', width = 15, command = qu_show)
    bt_next.grid(column = 0, row = 0, padx = 5, pady = 5, sticky = 'w')
    bt_answer = ttk.Button(cn_button_fr, text = 'Antwort', width = 15, command = an_show)
    bt_answer.grid(column = 1, row = 0, padx = 0, pady = 5, sticky = 'w')
    lb_infotx = ttk.Label(cn_button_fr, text = 'FlashCards 2.2 by Erik Tirschmann', width = 37, anchor = 'center', background = fr_color_db)
    lb_infotx.grid(column = 2, row = 0, padx = 5, pady = 5, ipady = 0)
    bt_help_fi = ttk.Button(cn_button_fr, text = '？', width = 3, command = show_help)
    bt_help_fi.grid(column = 3, row = 0, padx = 0, pady = 5, sticky = 'e')
    bt_backup = ttk.Button(cn_button_fr, text = '☁', width = 3, command = create_backup)
    bt_backup.grid(column = 4, row = 0, padx = 5, pady = 5, sticky = 'e')
    bt_toggle = ttk.Button(cn_button_fr, text = '⇊', width = 3, command = toggle_buttons)
    bt_toggle.grid(column = 5, row = 0, padx = 0, pady = 5, sticky = 'e')
    # hotfixes
    tb_question.bind('<Return>', lambda e: return_hotfix())
    cb_select_db.bind('<<ComboboxSelected>>', lambda e: combobox_hotfix())

    ###########################################################################
    # window settings
    root.update_idletasks()
    window_w = 550
    window_h = root.winfo_reqheight()
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    center_x = int(screen_w / 2 - window_w / 2)
    center_y = int(screen_h / 2 - window_h / 2)

    root.title('Flashcards')
    root.iconbitmap('Pictures/fc.ico')
    root.geometry(f'{window_w}x{window_h}+{center_x}+{center_y}')
    root.resizable(False, False)

    hide_buttons()

    root.mainloop()
