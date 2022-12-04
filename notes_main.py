from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
        QApplication, QWidget, 
        QHBoxLayout, QVBoxLayout, 
        QGroupBox, QRadioButton,  
        QPushButton, QLabel, QButtonGroup,
        QTextEdit, QLineEdit, QListWidget, QInputDialog)
import json
app = QApplication([])
notes_win = QWidget()
notes_win.setWindowTitle('jest')
notes_win.resize(900, 700)

notes = {
        'добро пожаловать' : {
                'текст' : 'это',
                'теги' : ['добро', 'инструкция']
        }
}

with open('notes_data.json', 'w') as file:
        json.dump(notes, file)

list_notes = QListWidget()
list_notes_label = QLabel('список заметок')

button_note_create = QPushButton('создать заметку')
button_note_del = QPushButton('удалить заметку')
button_note_save = QPushButton('сохранить заметку')

field_tag = QLineEdit('')
field_tag.setPlaceholderText('Введите текст or тег')
field_text = QTextEdit()
button_tag_add = QPushButton('добавить к заметке')
button_tag_del = QPushButton('открепить от замктки')
button_tag_search = QPushButton('искать заметки по тегу')
list_tags = QListWidget()
list_tags_label = QLabel('список тегов')

layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)
col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)
row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)
row_2 = QHBoxLayout()
row_2.addWidget(button_note_save)

col_2.addLayout(row_1)
col_2.addLayout(row_2)

col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)
row_3 = QHBoxLayout()
row_3.addWidget(button_tag_del)
row_3.addWidget(button_tag_add)
row_4 = QHBoxLayout()
row_4.addWidget(button_tag_search)

col_2.addLayout(row_3)
col_2.addLayout(row_4)

layout_notes.addLayout(col_1, stretch = 2)
layout_notes.addLayout(col_2, stretch = 1)
notes_win.setLayout(layout_notes)

def add_note():
        note_name, ok = QInputDialog.getText(notes_win, 'добавить заметку', 'название заметки')
        if ok and note_name != '':
                notes[note_name] = {'текст' : '', 'теги' : []}
                list_notes.addItem(note_name)
                list_tags.addItems(notes[note_name]['теги'])
                print(notes)

def show_note():
        key = list_notes.selectedItems()[0].text()
        print(key)
        field_text.setText(notes[key]['текст'])
        list_tags.clear()
        list_tags.addItems(notes[key]['теги'])

def save_note():
        if list_notes.selectedItems():
                key = list_notes.selectedItems()[0].text()
                notes[key]['текст'] = field_text.toPlainText()
                with open('notes_data.json', 'w') as file:
                        json.dump(notes, file, sort_keys = True, ensure_ascii = False)
                print(notes)
        else:
                print('заметка для сохранение не выбрана')

def del_note():
        if list_notes.selectedItems():
                key = list_notes.selectedItems()[0].text()
                del notes[key]
                list_notes.clear()
                list_tags.clear()
                lise_taxt.clear()
                list_notes.addItems(notes)
                with open('notes_data.json', 'w') as file:
                        json.dump(notes, file, sort_keys = True, ensure_ascii = False)
                print(notes)
        else:
                print('заметка для удаления не выбрана')

def add_tag():
        if list_notes.selectedItems():
                key = list_notes.selectedItems()[0].text()
                tag = field_tag.text()
                if not tag in notes[key]['теги']:
                        notes[key]['теги'].append(tag)
                        list_tags.addItem(tag)
                        field_tag.clear()
                with open('notes_data.json', 'w') as file:
                        json.dump(notes, file, sort_keys = True, ensure_ascii = False)
                        print(notes)
        else:
                print('заметка для добавление не выюрана')

def del_tag():
        if list_tags.selectedItems():
                key = list_notes.selectedItems()[0].text()
                tag = list_tags.selectedItems()[0].text()
                notes[key]['теги'].remove(tag)
                list_tags.clear()
                list_tags.addItems(notes[key]['теги'])
                with open('notes_data.json', 'w') as file:
                        json.dump(notes, file, sort_keys = True, ensure_ascii = False)
        else:
                print('тег для удаления не выбран')

def search_tag():
        print(button_note_search.text())
        tag = field_tag.text()
        if button_note_search.text() == 'искать заметки по тегу' and tag:
                print(tag)
                notes_filtered = {}
                for note in notes:
                        if tag in notes[note]['теги']:
                                notes_filtered[note] = notes[note]
                button_note_search.setText('сюросить пойск')
                list_notes.clear()
                list_tags.clear()
                list_notes.addItems(notes_filtered)
                print(button_note_search.text())
        elif button_note_search.text() == 'сбросить поиск':
                field_tag.clear()
                list_notes.clear()
                list_tags.clear()
                list_notes.addItems(notes)
                button_tag_search.setText('искать заметки по тегу')
                print(button_tag_search.text())
        else:
                pass

button_note_create.clicked.connect(add_note)
list_notes.itemClicked.connect(show_note)
button_note_save.clicked.connect(save_note)
button_note_del.clicked.connect(del_note)  
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)      

notes_win.show()

with open('notes_data.json', 'r') as file:
        notes = json.load(file)
list_notes.addItems(notes)

app.exec()
