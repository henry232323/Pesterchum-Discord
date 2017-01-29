from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QDesktopServices, \
    QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, pyqtSlot, QModelIndex, QVariant
from PyQt5 import uic

import asyncio

from dialogs import *


class Gui(QMainWindow):
    def __init__(self, loop, app, **kwargs):
        super(__class__, self).__init__(**kwargs)
        self.app = app
        self.loop = loop
        self.theme = self.app.theme
        self.tabWindow = None
        self.quirkWindow = None
        self.memosWindow = None

    def initialize(self):
        self.widget = uic.loadUi("themes/pesterchum2.5/ui/Main.ui", self)

        self.nameButton.setText(self.app.client.user.name)

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
        self.authAction.triggered.connect(self.app.openAuth)
        self.profileMenu.addAction(self.authAction)

        # Create OPTIONS button in 'CLIENT' menu
        self.optionsAction = QAction("OPTIONS", self)
        self.optionsAction.triggered.connect(self.openOptions)
        self.clientMenu.addAction(self.optionsAction)

        # Create MEMOS button in 'CLIENT' menu
        self.openMemos = QAction("MEMOS", self)
        self.openMemos.triggered.connect(self.openMemosWindow)
        self.clientMenu.addAction(self.openMemos)

        # Create EXIT button in 'CLIENT' menu
        self.exitClient = QAction("EXIT", self)
        self.exitClient.triggered.connect(self.app.exit)
        self.clientMenu.addAction(self.exitClient)

        # Make window movable from 'Pesterchum' label, for lack of Title Bar
        self.appLabel.mousePressEvent = self.label_mousePressEvent
        self.appLabel.mouseMoveEvent = self.label_mouseMoveEvent

        # Set window info
        self.setWindowTitle('Pesterchum')
        self.setWindowIcon(QIcon("resources/pc_chummy.png"))
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Create QStandardItemModel for QTreeView
        self.friendsItems = dict()
        self.friendsUsers = dict()
        self.friendsModel = self.FriendsModel(self.app)

        # Create a QStandardItem for each friend, friendsModel will auto update
        for channel in self.app.client.private_channels:
            if channel.type == channel.type.group:
                if not channel.name:
                    friend = ",".join(map(lambda c: c.name, channel.recipients))
                else:
                    friend = channel.name
            else:
                friend = channel.user.name
            self.friendsUsers[friend] = channel.user

            treeitem = QStandardItem(friend)
            treeitem.setText(friend)
            treeitem.setIcon(QIcon(self.theme["path"] + "/offline.png"))
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

        self.show()

    # Methods for moving window
    @pyqtSlot()
    def label_mousePressEvent(self, event):
        self.offset = event.pos()

    @pyqtSlot()
    def label_mouseMoveEvent(self, event):
        x = event.globalX()
        y = event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.move(x - x_w, y - y_w)

    def start_privmsg(self, user):
        """
        Start a private message window, if one exists add a user to it
        Return the new tab of the user
        """
        if not self.tabWindow:
            self.tabWindow = TabWindow(self.app, self, user)
            return self.tabWindow.init_user
        else:
            return self.tabWindow.add_user(user)

    @pyqtSlot(QModelIndex)
    def open_privmsg(self, index):
        user = self.friendsModel.data(index)
        self.start_privmsg(self.friendsUsers[user])
        self.tabWindow.raise_()
        self.tabWindow.activateWindow()

    def drawTree(self):
        for name, item in self.friendsItems.items():
            index = self.friendsModel.indexFromItem(item)
            self.chumsTree.setRowHidden(index.row(), self.friendsModel.parent(index), False)

    def openMemosWindow(self):
        self.memosWindow = MemosWindow(self.app, self)

    def openQuirkWindow(self):
        self.openQuirkWindow = QuirksWindow(self.app)

    def openOptions(self):
        try:
            self.optionsWindow = OptionsWindow(self.app, self)
        except Exception as e:
            print(e)

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
