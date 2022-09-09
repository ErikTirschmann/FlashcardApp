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
# Funktion: db_backup()
#------------------------------------------------------------------------------
# Ein Backup des aktuellen Datenbankzustands erstellen
#------------------------------------------------------------------------------
#
def db_backup_files():
    # vorherige Backups Entfernen
    bk_files = list_all_files(db_backup)
    for file in range(0, len(bk_files)):
        os.remove(os.path.join(db_backup, bk_files[file]))
    # Neue Backup dateien erstellen
    db_files = list_all_files(db_folder)
    for file in range(0, len(db_files)):
        shutil.copyfile(os.path.join(db_folder, db_files[file]), os.path.join(db_backup, db_files[file]))

###############################################################################
# Funktion: db_showinfo()
#------------------------------------------------------------------------------
#
def db_showinfo():
    tki.messagebox.showinfo('Info', '[Button Erstellen]\n\nAktiviert das obere Textfeld um die Eingabe eines Datenbanknamens zu ermöglichen.\n\n\n[Button Bestätigen]\n\nVersucht eine Datenbank zu erstellen die den im oberen Textfeld angegebenen Namen trägt.\n\n\n[Button Entfernen]\n\nEntfernt die momentan aktivierte Datenbank.')

###############################################################################
# Function: qu_showinfo()
#------------------------------------------------------------------------------
#
def qu_showinfo():
    tki.messagebox.showinfo('Info', '[Button Erstellen]\n\nAktiviert das obere und untere Textfeld um die Eingabe einer Frage / Antwort Kombination zu ermöglichen.\n\n\n[Button bestätigen]\n\nVersucht eine Fragen / Antwort Kombination in die momentan aktive Datenbank zu schreiben.\n\n\n[Button Entfernen]\n\nEntfernt die derzeitige Frage / Antwort Kombination aus der momentan aktiven Datenbank.')

###############################################################################
# Function: show_help()
#------------------------------------------------------------------------------
#
def show_help():
    os.startfile('FlashcardApp - Hilfe.pdf')
    
###############################################################################
# Funktion return_pressed()
#------------------------------------------------------------------------------
# Verhalten der Eingabetaste bearbeiten
#------------------------------------------------------------------------------
#
def return_pressed(event = None):
    if event is None:
        if str(bt_create_db['state']) == 'normal':
            db_create()
        elif str(bt_create_qu['state']) == 'normal':
            qu_create()

###############################################################################
# Funktion list_all_files()
#------------------------------------------------------------------------------
# file path: String var
# returns: List
#------------------------------------------------------------------------------
# Erzeugt eine Liste aller in file_path enthaltenen Dateien
#------------------------------------------------------------------------------
#
def list_all_files(file_path):
    files = next(os.walk(file_path))[2]
    cleaned = []
    for file in range(0, len(files)):
        cleaned.append(files[file].replace('.txt', ''))
    return cleaned

###############################################################################
# Funktion: clear_content()
#------------------------------------------------------------------------------
# löscht den angezeigten Text des Elements
#------------------------------------------------------------------------------
#
def clear_content(_object):
    _object['state'] = 'normal'
    _object.delete('1.0', 'end')

###############################################################################
def clear_and_lock(_object):
    clear_content(_object)
    _object['state'] = 'disabled'
    _object.configure(background = '#eceff4')

###############################################################################
# Funktion: db_button_lock()
#------------------------------------------------------------------------------
# Sperrt / Entsperrt die Buttons zur Datenbankverwaltung
#------------------------------------------------------------------------------
#
def db_button_lock():
    clear_and_lock(tb_question)
    clear_and_lock(tb_answer)
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

###############################################################################
# Funktion: qu_button_lock()
#------------------------------------------------------------------------------
# Sperrt / entsperrt die Buttons zur Fragenverwaltung
#------------------------------------------------------------------------------
#
def qu_button_lock():
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

###############################################################################
# Funktion: qu_create_input()
#------------------------------------------------------------------------------
# Ermöglicht die Eingabe für einen neuen Frageneintrag
#------------------------------------------------------------------------------
#
def qu_create_input():
    clear_content(tb_question)
    clear_content(tb_answer)
    tb_question.focus_set()
    tb_question.configure(background = '#ffffff')
    tb_answer.configure(background = '#ffffff')

###############################################################################
# Funktion: db_create_input()
#------------------------------------------------------------------------------
# Ermöglicht die Eingabe für einen neuen Datenbankeintrag
#------------------------------------------------------------------------------
#
def db_create_input():
    qu_create_input()
    tb_answer.configure(background = '#eceff4')
    tb_answer['state'] = 'disabled'
    tb_question.configure(background = '#ffffff')

###############################################################################
# Funktion: db_create()
#------------------------------------------------------------------------------
# Erstellt, wenn möglich, eine neue Datenbank
#------------------------------------------------------------------------------
#
def db_create():
    if Path(db_folder).is_dir() and len(tb_question.get('1.0', 'end')) > 3:
        file_name = os.path.join(db_folder, str.strip(tb_question.get('1.0', 'end')) + '.txt')
        try:
            with open(file_name, 'x', encoding = 'utf-8') as f:
                f.close()
            clear_and_lock(tb_question)
            tb_question.configure(background = '#eceff4')
            cb_select_db['values'] = sorted(list_all_files(db_folder))
        except OSError:
            tki.messagebox.showerror('Fehler', f'{file_name} existiert bereits!')
            clear_and_lock(tb_question)
            tb_question.configure(background = '#eceff4')

###############################################################################
# Funktion: qu_create()
#------------------------------------------------------------------------------
# Erstellt, wenn möglich einen neuen Frage / Antwort Eintrag
#------------------------------------------------------------------------------
#
def qu_create():
    if len(tb_answer.get('1.0', 'end')) > 3 and len(tb_question.get('1.0', 'end')) > 5:
        file_name = os.path.join(db_folder, str.strip(cb_select_db.get()) + '.txt')
        try:
            qust = str.strip(tb_question.get('1.0', 'end'))
            answ = str.strip(tb_answer.get('1.0', 'end')).replace('\n', ';;;')
            with open(file_name, 'r', encoding = 'utf-8') as f:
                file_lines = f.readlines()
                f.close()
            for x in range(len(file_lines)):
                if file_lines[x].split('###')[0] == qust:
                    tki.messagebox.showerror('Fehler', f'{qust} ist bereits in der Datenbank enthalten!')
                    return()
            file_lines.append(f'{qust}###{answ}\n')
            with open(file_name, 'w', encoding = 'utf-8') as f:
                f.writelines(file_lines)
                f.close()
            clear_and_lock(tb_question)
            clear_and_lock(tb_answer)
        except FileNotFoundError:
            tki.messagebox.showerror('Fehler', 'Keine Datenbank ausgewählt!')

###############################################################################
# Funktion db_remove()
#------------------------------------------------------------------------------
# Entfernt eine Datenbank fals möglich
#------------------------------------------------------------------------------
#
def db_remove():
    if cb_select_db.get() != '' and tki.messagebox.askquestion('Achtung', f'Möchten sie {cb_select_db.get()} wirklich unwiederruflich löschen?') == 'yes':
        os.remove(os.path.join(db_folder, cb_select_db.get() + '.txt'))
        cb_select_db.set('')
        cb_select_db['values'] = sorted(list_all_files(db_folder))
    else:
        tki.messagebox.showerror('Fehler', 'Keine Datenbank ausgewählt!')

###############################################################################
# Funktion: qu_remove()
#------------------------------------------------------------------------------
# Entfernt einen Eintrag falls möglich
#------------------------------------------------------------------------------
#
def qu_remove():
    if len(tb_question.get('1.0', 'end')) > 3 :
        if tki.messagebox.askquestion('Achtung', 'Möchten sie den Eintrag {0} wirklich entfernen?'.format(tb_question.get('1.0', 'end').strip())) == 'yes':
            file_name = os.path.join(db_folder, str.strip(cb_select_db.get() + '.txt'))
            with open(file_name, 'r', encoding = 'utf-8') as f:
                file_lines = f.readlines()
                f.close()
            for line in file_lines:
                if line.split('###')[0].strip() == tb_question.get('1.0', 'end').strip():
                    file_lines.remove(line)
            with open(file_name, 'w', encoding = 'utf-8') as f:
                f.writelines(file_lines)
                f.close()
            clear_and_lock(tb_question)
            clear_and_lock(tb_answer)

###############################################################################
# Funktion: qu_show()
#------------------------------------------------------------------------------
# Zeigt eine zufällige Frage im oberen Textfeld an
#------------------------------------------------------------------------------
#
def qu_show():
    try:
        file_name = os.path.join(db_folder, str.strip(cb_select_db.get() + '.txt'))
        with open(file_name, 'r', encoding = 'utf-8') as f:
            file_lines = f.readlines()
            f.close()
        qust = file_lines[random.randint(0, len(file_lines) - 1)].split('###')[0]
        # Verhindern dass die selbe Frage nocheinmal kommt
        if len(file_lines) > 1:
            if qust != tb_question.get('1.0', 'end').strip():
                clear_and_lock(tb_answer)
                clear_content(tb_question)
                tb_question.insert('1.0', qust)
                tb_question['state'] = 'disabled'
            else:
                qu_show()
        else:
            clear_and_lock(tb_answer)
            clear_content(tb_question)
            tb_question.insert('1.0', qust)
            tb_question['state'] = 'disabled'
    except FileNotFoundError:
        tki.messagebox.showerror('Fehler', 'Keine Datenbank ausgewählt!')

###############################################################################
# Funktion: qn_show():
#------------------------------------------------------------------------------
# Zeigt die Antwort zur Frage im oberen Textfeld im unteren textfeld an
#------------------------------------------------------------------------------
#
def an_show():
    file_name = os.path.join(db_folder, str.strip(cb_select_db.get() + '.txt'))
    with open(file_name, 'r', encoding = 'utf-8') as f:
        file_lines = f.readlines()
        f.close()
    for line in file_lines:
        if line.split('###')[0].strip() == tb_question.get('1.0', 'end').strip():
            clear_content(tb_answer)
            lst_options = line.split('###')[1].strip().split(';;;')
            for option in range(0, len(lst_options)):
                tb_answer.insert('1.0', (lst_options[option] + '\n'))
            tb_answer['state'] = 'disabled'


if __name__ == '__main__':
    root = tki.Tk()
    ###########################################################################
    # Fenster Proportionen und ausrichtung auf dem Bildschirm
    #--------------------------------------------------------------------------
    #
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
    ###########################################################################
    # Verhalten der eingabestaste
    #--------------------------------------------------------------------------
    #
    root.bind('<Return>', lambda e: return_pressed())

    ###########################################################################
    # Erstellen eines rasters auf dem Fenster
    #--------------------------------------------------------------------------
    #
    root.columnconfigure(0, weight = 1) # Reihen für breite Buttons
    root.columnconfigure(1, weight = 1) #
    root.columnconfigure(2, weight = 1) #
    root.columnconfigure(3, weight = 2) # Reihe fpr Labels
    root.columnconfigure(4, weight = 1) # Reihen für schmale Buttons
    root.columnconfigure(5, weight = 1) #
    ###########################################################################
    # Platzuierung der Elemente auf dem rasters
    #--------------------------------------------------------------------------
    # Reihe 1: Datenbank auswahl
    #--------------------------------------------------------------------------
    #
    sv_select_db = tki.StringVar()
    cb_select_db = ttk.Combobox(root, textvariable = sv_select_db)
    cb_select_db['values'] = sorted(list_all_files(db_folder))
    cb_select_db['state'] = 'readonly'
    cb_select_db.grid(column = 0, row = 1, padx = 5, pady = 5, columnspan = 6, sticky = 'ew')
    #--------------------------------------------------------------------------
    # Reihe 2: Datenbank verwaltung
    #--------------------------------------------------------------------------
    #
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
    #--------------------------------------------------------------------------
    # Reihe 3: Fragen verwaltung
    #--------------------------------------------------------------------------
    #
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
    #--------------------------------------------------------------------------
    # Reihe 4: Fragen Textfeld
    #--------------------------------------------------------------------------
    #
    tb_question = tki.Text(root, height = 1, state = 'disabled')

    tb_question.grid(column = 0, row = 4, padx = 5, pady = 5, columnspan = 6, sticky = 'ew')
    tb_question.configure(font = font_tuple, background = '#eceff4')
    #--------------------------------------------------------------------------
    # Reihe 5: Antwort Textfeld
    #--------------------------------------------------------------------------
    #
    tbs_frame = tki.Frame(root)
    tbs_frame.columnconfigure(0, weight = 1) # Reihe für Textbox und Scrollbar
    tbs_frame.grid(column = 0, row = 5, padx = 5, pady = 5, columnspan = 6, sticky = 'ew')
    tb_answer = tki.Text(tbs_frame, height = 8, wrap = 'word', state = 'disabled')
    tb_answer.grid(column = 0, row = 0, padx = 0, pady = 0, sticky = 'ew')
    tb_answer.configure(font = font_tuple, background = '#eceff4')
    sb_answer = ttk.Scrollbar(tbs_frame, orient = 'vertical', command = tb_answer.yview)
    sb_answer.grid(column = 1, row = 0, padx = 0, pady = 0, sticky = 'nse')
    tb_answer['yscrollcommand'] = sb_answer.set
    #--------------------------------------------------------------------------
    # Reihe 6: Ablauf verwaltung
    #--------------------------------------------------------------------------
    #
    bt_next = ttk.Button(root, text = 'Frage', width = 15, command = qu_show)
    bt_next.grid(column = 0, row = 6, padx = 5, pady = 5, sticky = 'w')
    bt_answer = ttk.Button(root, text = 'Antwort', width = 15, command = an_show)
    bt_answer.grid(column = 1, row = 6, padx = 0, pady = 5, sticky = 'w')
    bt_help_fi = ttk.Button(root, text = '？', width = 5, command = show_help)
    bt_help_fi.grid(column = 4, row = 6, padx = 0, pady = 5, sticky = 'e')
    bt_backup = ttk.Button(root, text = '☁', width = 5, command = db_backup_files)
    bt_backup.grid(column = 5, row = 6, padx = 5, pady = 5, sticky = 'e')

    root.mainloop()
