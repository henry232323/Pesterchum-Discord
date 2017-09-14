#!/usr/bin/env python3
# Copyright (c) 2016-2017, henry232323
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from PyQt5.QtGui import QIcon, QDesktopServices, QStandardItemModel
from PyQt5.QtCore import Qt, pyqtSlot, QModelIndex, QVariant, QUrl
from PyQt5.QtWidgets import QMainWindow, QSystemTrayIcon, QTreeView
from PyQt5 import uic

from random import randint, choice

from dialogs import *


class Gui(QMainWindow):
    def __init__(self, loop, app, **kwargs):
        super(__class__, self).__init__(**kwargs)
        self.app = app
        self.loop = loop
        self.theme = self.app.theme
        self.offset = None
        self.tabWindow = None
        self.quirkWindow = None
        self.memosWindow = None
        self.mood_buttons = dict()

    def initialize(self):
        uic.loadUi(self.theme["ui_path"] + "/Main.ui", self)

        self.nameButton.setText(self.app.client.user.name)
        self.nameButton.setIcon(QIcon(self.theme["path"] + "/chummy.png"))

        # Fix dimensions
        width = self.frameGeometry().width()
        height = self.frameGeometry().height()
        self.setFixedSize(width, height)

        # Initialize top Menu
        self.menubar = self.menuBar()
        self.clientMenu = self.menubar.addMenu("CLIENT")
        self.profileMenu = self.menubar.addMenu("PROFILE")
        self.helpMenu = self.menubar.addMenu("HELP")

        # Create QUIRKS button in 'PROFILE' menu
        self.quirkAction = QAction("QUIRKS", self)
        self.quirkAction.triggered.connect(self.openQuirkWindow)
        self.profileMenu.addAction(self.quirkAction)

        # Create SWITCH button in 'PROFILE' menu
        self.authAction = QAction("SWITCH", self)
        self.authAction.triggered.connect(lambda: self.app.openAuth(i=False))
        self.profileMenu.addAction(self.authAction)

        # Create OPTIONS button in 'CLIENT' menu
        self.optionsAction = QAction("OPTIONS", self)
        self.optionsAction.triggered.connect(self.openOptions)
        self.clientMenu.addAction(self.optionsAction)

        # Create MEMOS button in 'CLIENT' menu
        self.openMemos = QAction("MEMOS", self)
        self.openMemos.triggered.connect(self.openMemosWindow)
        self.clientMenu.addAction(self.openMemos)

        # Create HIDE button in 'CLIENT' menu
        self.toggleHidden = QAction("HIDE", self)
        self.toggleHidden.triggered.connect(self.toggleHide)
        self.clientMenu.addAction(self.toggleHidden)

        # Create IDLE button in 'CLIENT' menu
        self.toggleIdled = QAction("IDLE", self)
        self.toggleIdled.triggered.connect(self.toggleIdle)
        self.clientMenu.addAction(self.toggleIdled)

        # Create EXIT button in 'CLIENT' menu
        self.exitClient = QAction("EXIT", self)
        self.exitClient.triggered.connect(self.app.exit)
        self.clientMenu.addAction(self.exitClient)

        if self.app.trayIcon is None:
            # Create a tray icon for the app so you can hide and unhide the app
            self.app.trayIcon = QSystemTrayIcon(QIcon(self.app.theme["path"] + "/trayicon.png"), self.app)
            self.app.trayIcon.show()
        self.app.trayIcon.setContextMenu(self.clientMenu)

        # Set window info
        self.setWindowTitle('Pesterchum')
        self.setWindowIcon(QIcon(self.theme["path"] + "/trayicon.png"))
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Create QStandardItemModel for QTreeView
        self.friendsItems = dict()
        self.friendsUsers = dict()
        self.friendsModel = self.FriendsModel(self.app)

        # Create HELP button in 'HELP' menu
        self.openHelpAction = QAction("HELP", self)
        self.openHelpAction.triggered.connect(self.openHelp)
        self.helpMenu.addAction(self.openHelpAction)

        # Create REPORT BUG button in 'HELP' menu
        self.openBugAction = QAction("REPORT BUG", self)
        self.openBugAction.triggered.connect(self.openBug)
        self.helpMenu.addAction(self.openBugAction)

        # Create DEBUG button in 'HELP' menu
        self.openDebugAction = QAction("DEBUG", self)
        self.openDebugAction.triggered.connect(self.openDebug)
        self.helpMenu.addAction(self.openDebugAction)

        # Create a QStandardItem for each friend, friendsModel will auto update
        for channel in self.app.client.private_channels:
            if isinstance(channel, discord.GroupChannel):
                if not channel.name:
                    friend = ", ".join(map(lambda c: c.display_name, channel.recipients))
                else:
                    friend = channel.name
            else:
                friend = channel.recipient.display_name
            self.friendsUsers[friend] = channel

            treeitem = QStandardItem(friend)
            treeitem.setText(friend)
            treeitem.setIcon(QIcon(self.theme["path"] + "/{}.png".format(choice(self.app.moods.moods))))
            self.friendsModel.appendRow(treeitem)
            self.friendsItems[friend] = treeitem

        self.friendsModel.sort(0)
        self.chumsTree.setModel(self.friendsModel)
        self.chumsTree.doubleClicked.connect(self.open_privmsg)
        self.chumsTree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.chumsTree.setSelectionMode(QTreeView.SingleSelection)
        self.chumsTree.setSelectionBehavior(QTreeView.SelectRows)
        self.chumsTree.setExpandsOnDoubleClick(True)
        self.chumsTree.setItemsExpandable(True)

        self.pesterButton.clicked.connect(self.privmsg_pester)
        self.blockButton.clicked.connect(self.block_selected)
        self.addChumButton.clicked.connect(self.add_selected)

        for num in range(23):
            name = "moodButton{}".format(num)
            if hasattr(self, name):
                button = getattr(self, name)
                self.mood_buttons[num] = button
                mood_name = self.app.moods.getName(num)
                button.setIcon(QIcon(os.path.join(self.theme["path"], "{}.png".format(mood_name))))
                button.clicked.connect(self.make_setMood(button))

        self.colorButton.setStyleSheet('background-color: rgb({},{},{});'.format(randint(0,255), randint(0,255), randint(0,255)))

        self.show()

    # Methods for moving window
    @pyqtSlot()
    def mousePressEvent(self, event):
        self.offset = event.pos()

    @pyqtSlot()
    def mouseMoveEvent(self, event):
        if self.offset is None:
            return
        x = event.globalX()
        y = event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.move(x - x_w, y - y_w)

    @pyqtSlot()
    def mouseReleaseEvent(self, event):
        self.offset = None

    def privmsg_pester(self):
        """Opens selected user in tree when PESTER! button pressed, same as double click"""
        selected = self.chumsTree.selectedIndexes()
        if selected:
            idx = selected[0]
            user = self.friendsModel.data(idx)
            self.start_privmsg(self.friendsUsers[user])
            self.tabWindow.raise_()
            self.tabWindow.activateWindow()

    def add_selected(self):
        selected = self.chumsTree.selectedIndexes()
        if selected:
            idx = selected[0]
            user = self.friendsModel.data(idx)
            user.send_friend_request()

    def block_selected(self):
        selected = self.chumsTree.selectedIndexes()
        if selected:
            idx = selected[0]
            user = self.friendsModel.data(idx)
            user.block()

    def start_privmsg(self, channel):
        """
        Start a private message window, if one exists add a user to it
        Return the new tab of the user
        """
        if isinstance(channel, (discord.User, discord.Member)):
            ensure_future(self.start_pm(channel))
            return
        if not self.tabWindow:
            self.tabWindow = TabWindow(self.app, self, channel)
            return self.tabWindow.init_user
        else:
            return self.tabWindow.add_user(channel)

    async def start_pm(self, user):
        channel = await user.create_dm()
        self.start_privmsg(channel)

    @pyqtSlot(QModelIndex)
    def open_privmsg(self, index):
        user = self.friendsModel.data(index)
        self.start_privmsg(self.friendsUsers[user])
        self.tabWindow.raise_()
        self.tabWindow.activateWindow()

    def openHelp(self):
        QDesktopServices.openUrl(QUrl("https://github.com/henry232323/Pesterchum-Discord"))

    def openBug(self):
        QDesktopServices.openUrl(QUrl("https://github.com/henry232323/Pesterchum-Discord/issues"))

    def openMemosWindow(self):
        self.memosWindow = MemosWindow(self.app, self)

    def openQuirkWindow(self):
        self.openQuirkWindow = QuirksWindow(self.app)

    def openOptions(self):
        self.optionsWindow = OptionsWindow(self.app, self)

    def openDebug(self):
        self.debugWindow = InteractiveConsole(self.app)

    def toggleHide(self):
        if self.isHidden():
            self.show()
            self.toggleHidden.setIcon(QIcon())
        else:
            self.hide()
            self.toggleHidden.setIcon(QIcon(self.theme["path"] + "/x.png"))

    def toggleIdle(self):
        self.app.idle = not self.app.idle
        if self.app.idle:
            ensure_future(self.app.client.change_presence(status=discord.Status.idle))
            self.toggleIdled.setIcon(QIcon(self.theme["path"] + "/x.png"))
        else:
            ensure_future(self.app.client.change_presence(status=discord.Status.online))
            self.toggleIdled.setIcon(QIcon())

    def make_setMood(self, button):
        '''Makes set mood button for each button, each button deselects all others and sets user mood'''
        def setMood():
            if not button.isChecked():
                button.setChecked(True)
                return
            for num, moodButton in self.mood_buttons.items():
                if button == moodButton:
                    mood_name = self.app.moods.getName(num)
                    self.nameButton.setIcon(QIcon(os.path.join(self.theme["path"], mood_name + ".png")))
                    self.app.change_mood(mood_name)
                else:
                    moodButton.setChecked(False)
        return setMood

    def closeEvent(self, event):
        if self.app.options["interface"]["close"] != 2:
            try:
                self.toggleHide()
                event.ignore()
            except Exception as e:
                print(e)
        else:
            event.accept()

    class FriendsModel(QStandardItemModel):
        def __init__(self, app, parent=None):
            QStandardItemModel.__init__(self, parent)
            self.app = app
            itms = len(self.app.gui.friendsItems.keys())
            self.header_labels = ["Chums ({}/{})".format(itms, itms)]

        def headerData(self, section, orientation, role=Qt.DisplayRole):
            fmt = "Chums ({}/{})"
            itms = len(self.app.gui.friendsItems.keys())
            self.header_labels = [fmt.format(itms, itms)]
            if role == Qt.DisplayRole and orientation == Qt.Horizontal:
                return self.header_labels[section]
            return QStandardItemModel.headerData(self, section, orientation, role)

        def update(self):
            itms = len(self.app.gui.friendsItems.keys())
            self.setHeaderData(0, Qt.Orientation(1),
                               QVariant("Chums ({}/{})".format(itms, itms)))
