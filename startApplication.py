from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys

import json
# keys:
#   'colorIdentity'
#   'colors'
#   'convertedManaCost'
#   'foreignData'
#   'layout'
#   'legalities'
#   'manaCost'
#   'name'
#   'printings'
#   'purchaseUrls'
#   'rulings'
#   'scryfallOracleId'
#   'subtypes'
#   'supertypes'
#   'text'
#   'type'
#   'types'
#   'uuid'


def load_initial_database(database):
    items = json.loads(database)
    return items
 
 
class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("GUI/02_sammlung.ui", self)

        with open("./AllCards.json") as input:
            cache = input.read()
            self.database = json.loads(cache)
            self.cards = [i for i in self.database]
            self.cards.sort()

        self.list_sammlung_gefundene_karten = self.findChild(QListWidget, "list_sammlung_gefundene_karten")
        self.list_sammlung_gefundene_karten.doubleClicked.connect(self.list_view_double_clicked)
        self.init_list_view()

        self.btn_sammlung_zur_sammlung_hinzufuegen = self.findChild(QPushButton, "btn_sammlung_zur_sammlung_hinzufuegen")

        self.line_edit_sammlung_name = self.findChild(QLineEdit, "line_edit_sammlung_name")
        self.line_edit_sammlung_name.textChanged.connect(self.line_edit_text_changed)

        # color filters
        self.chkbox_sammlung_farbeR = self.findChild(QCheckBox, "chkbox_sammlung_farbeR")
        self.chkbox_sammlung_farbeR.stateChanged.connect(self.color_filter)
        self.chkbox_sammlung_farbeG = self.findChild(QCheckBox, "chkbox_sammlung_farbeG")
        self.chkbox_sammlung_farbeG.stateChanged.connect(self.color_filter)
        self.chkbox_sammlung_farbeB = self.findChild(QCheckBox, "chkbox_sammlung_farbeB")
        self.chkbox_sammlung_farbeB.stateChanged.connect(self.color_filter)
        self.chkbox_sammlung_farbeS = self.findChild(QCheckBox, "chkbox_sammlung_farbeS")
        self.chkbox_sammlung_farbeS.stateChanged.connect(self.color_filter)
        self.chkbox_sammlung_farbeW = self.findChild(QCheckBox, "chkbox_sammlung_farbeW")
        self.chkbox_sammlung_farbeW.stateChanged.connect(self.color_filter)
        self.chkbox_sammlung_exklusiv = self.findChild(QCheckBox, "chkbox_sammlung_exklusiv")
        self.chkbox_sammlung_exklusiv.stateChanged.connect(self.color_filter)

        self.show()

    def list_view_double_clicked(self):
        items = self.list_sammlung_gefundene_karten.selectedIndexes()
        for item in items:
            print(item.row())
            card = self.database[self.cards[item.row()]]
            for key in card.keys():
                if key == 'foreignData':
                    continue
                print(key, card[key], "\n")

    def line_edit_text_changed(self):
        text = self.line_edit_sammlung_name.text().lower()
        for card in self.cards:
            if card.lower().startswith(text):
                item = self.list_sammlung_gefundene_karten.findItems(card, QtCore.Qt.MatchRegExp)[0]
                item.setSelected(True)
                self.list_sammlung_gefundene_karten.scrollToItem(item)
                break

    def color_filter(self):
        filters = []
        if self.chkbox_sammlung_farbeR.isChecked():
            filters.append("R")
        if self.chkbox_sammlung_farbeG.isChecked():
            filters.append("G")
        if self.chkbox_sammlung_farbeB.isChecked():
            filters.append("U")
        if self.chkbox_sammlung_farbeS.isChecked():
            filters.append("B")
        if self.chkbox_sammlung_farbeW.isChecked():
            filters.append("W")

        if len(filters) == 0:
            self.init_list_view()
            return

        filtered_cards = []
        if self.chkbox_sammlung_exklusiv.isChecked():
            for card in self.cards:
                colors = self.database[card]['colors']
                if len(colors) == len(filters):
                    addCard = True
                    for f in filters:
                        if not (f in colors):
                            addCard = False
                            break

                    if addCard:
                        filtered_cards.append(card)
        else:
            for card in self.cards:
                colors = set(self.database[card]['colors'])
                filters = set(filters)
                if len(colors.intersection(filters)) > 0:
                    filtered_cards.append(card)

        self.set_list_view(filtered_cards)

    def init_list_view(self):
        self.list_sammlung_gefundene_karten.clear()
        for item in self.cards:
            t = ""
            item_text = item + " type: "
            colors = self.database[item]['colors']
            if len(colors) == 1:
                item_text += colors[0]
            else:
                for i in colors:
                    item_text += i + " "

            self.list_sammlung_gefundene_karten.addItem(item_text)

    def set_list_view(self, cards):
        self.list_sammlung_gefundene_karten.clear()
        for item in cards:
            t = ""
            item_text = item + " type: "
            colors = self.database[item]['colors']
            if len(colors) == 1:
                item_text += colors[0]
            else:
                for i in colors:
                    item_text += i + " "

            self.list_sammlung_gefundene_karten.addItem(item_text)
 
 
app = QApplication(sys.argv)
window = UI()
app.exec_()
