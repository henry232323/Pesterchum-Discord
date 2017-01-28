from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QTextCursor, QStandardItem, QColor
from PyQt5.QtCore import Qt
from PyQt5 import uic

import discord

from messages import *
from formatting import fmt_memo_msg, rgb


class PrivateMessageWidget(QWidget):
    def __init__(self, app, container, parent, user):
        """
        The widget within each tab of TabWindow, a display
        for new private messages and user input
        :param app: `pesterchum.App` Master app reference
        :param container: Associated `QStackedWidget`
        :param parent: `gui.Gui` Master GUI reference
        :param user: `discord.User` associated Discord User object
        """
        super(__class__, self).__init__()
        self.parent = parent
        uic.loadUi(app.theme["ui_path"] + "/PrivateMessageWidget.ui", self)
        self.user = user
        self.app = app
        self.container = container
        self.userLabel.setText(user.name.join(["::", "::"]))
        self.sendButton.clicked.connect(self.send)
        self.userOutput.setReadOnly(True)
        self.userOutput.setMouseTracking(True)
        if not isinstance(user, discord.PrivateChannel):
            self.display_text(fmt_begin_msg(app, self.app.client.user, user))

    def send(self):
        """Send the user the message in the userInput box, called on enter press / send button press"""
        msg = self.userInput.text()
        if msg:
            self.app.send_msg(msg, self.user)
            self.userInput.setText("")

    def display_text(self, msg):
        '''Insert msg into the display box'''
        cursor = self.userOutput.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.userOutput.setTextCursor(cursor)
        self.userOutput.insertHtml(msg)

    def keyPressEvent(self, event):
        '''Use enter key to send'''
        if event.key() == Qt.Key_Return:
            self.send()


class TabWindow(QWidget):
    def __init__(self, app, parent, user):
        """
        A window for storing PrivateMessageWidget instances, a navigation
        between current private message users
        """
        super(__class__, self).__init__()
        self.parent = parent
        self.app = app
        uic.loadUi(app.theme["ui_path"] + "/TabWindow.ui", self)
        self.users = []
        self.ids = []
        self.init_user = self.add_user(user)
        self.tabWidget.removeTab(0)  # Remove two default tabs
        self.tabWidget.removeTab(0)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)
        self.setWindowTitle("Private Message")
        self.setWindowIcon(QIcon("resources/pc_chummy.png"))
        self.show()

    def closeTab(self, currentIndex):
        widget = self.tabWidget.widget(currentIndex)
        widget.deleteLater()
        self.tabWidget.removeTab(currentIndex)
        self.users.remove(widget.user)
        if not self.users:
            self.close()

    def closeEvent(self, event):
        event.accept()
        self.app.gui.tabWindow = None

    def add_user(self, user):
        """
        Add a user & PrivateMessageWidget to window, check if it is already there
        if so, return that user's PM, if not, create and return a PM
        On PrivateMessageWidget creation, send a PESTERCHUM:BEGIN initiation message

        :rtype: `PrivateMessageWidget`
        :param user: The `discord.User` to message
        """
        if user.id not in self.ids:
            windw = PrivateMessageWidget(self.app, self.tabWidget, self, user)
            icon = QIcon("resources/pc_chummy.png")
            a = self.tabWidget.addTab(windw, icon, user.name)
            tab = self.tabWidget.widget(a)
            self.users.append(user)
            self.ids.append(user.id)
            return tab
        else:
            return self.tabWidget.widget(self.ids.index(user.id))


class AddFriendDialog(QDialog):
    def __init__(self, app, parent):
        """
        Dialog opened when the Add [Chum] button is pressed, adds to chumsTree widget
        """
        super(__class__, self).__init__()
        self.parent = parent
        self.app = app
        uic.loadUi(self.app.theme["ui_path"] + "/AddFriendDialog.ui", self)
        self.setWindowTitle('Add Chum')
        self.setWindowIcon(QIcon("resources/pc_chummy.png"))
        self.acceptButton.clicked.connect(self.accepted)
        self.rejectButton.clicked.connect(self.close)
        self.exec_()

    def accepted(self):
        '''Call once accepted, check if name is alphanumeric if not warn and try again'''
        user = self.addChumInput.text()
        if user:
            self.app.add_friend(user)
            self.close()


class AddBlockedDialog(QDialog):
    def __init__(self, app, parent):
        '''
        Dialog opened when the Add button is pressed in TROLLSLUM, adds to parent.blockedList widget
        '''
        super(__class__, self).__init__()
        self.parent = parent
        self.app = app
        uic.loadUi(self.app.theme["ui_path"] + "/AddBlockedDialog.ui", self)
        self.setWindowTitle('TROLLSLUM')
        self.setWindowIcon(QIcon("resources/pc_chummy.png"))
        self.acceptButton.clicked.connect(self.accepted)
        self.rejectButton.clicked.connect(self.close)
        self.exec_()

    def accepted(self):
        '''Call once accepted, check if name is alphanumeric if not warn and try again'''
        user = self.addChumInput.text()
        if user and (user not in self.app.blocked):
            self.app.add_blocked(user)
            item = QListWidgetItem(user)
            self.parent.blockedList.addItem(item)
            if user in self.app.friends.keys():
                index = self.app.gui.chumsTree.indexOfTopLevelItem(self.app.gui.getFriendItem(user)[0])
                self.app.gui.chumsTree.takeTopLevelItem(index)

            self.close()
        else:
            self.close()


class BlockedDialog(QDialog):
    def __init__(self, app, parent):
        super(__class__, self).__init__()
        uic.loadUi(app.theme["ui_path"] + "/BlockedDialog.ui", self)
        self.app = app
        self.parent = parent
        self.setWindowTitle('TROLLSLUM')
        self.setWindowIcon(QIcon("resources/pc_chummy.png"))
        self.addBlockButton.clicked.connect(self.add)
        self.removeBlockButton.clicked.connect(self.remove)
        for user in self.app.blocked:
            self.blockedList.addItem(QListWidgetItem(user))
        self.exec_()

    def add(self):
        dialog = AddBlockedDialog(self.app, self)

    def remove(self):
        selected = self.blockedList.selectedItems()
        if selected:
            item = selected[0]
            index = self.blockedList.indexFromItem(item)
            self.blockedList.takeItem(index.row())
            user = item.text()
            self.app.blocked.remove(user)
            if user in self.app.friends.keys():
                treeitem = QStandardItem(user)
                treeitem.setText(user)
                treeitem.setIcon(QIcon(self.app.theme["path"] + "/offline.png"))
                self.app.gui.friendsModel.appendRow(treeitem)


class OptionsWindow(QWidget):
    def __init__(self, app, parent):
        super(__class__, self).__init__()
        uic.loadUi(app.theme["ui_path"] + "/OptionsWindow.ui", self)
        self.app = app
        self.parent = parent
        self.setWindowTitle('Options')
        self.setWindowIcon(QIcon("resources/pc_chummy.png"))
        self.options = self.app.options
        width = self.frameGeometry().width()
        height = self.frameGeometry().height()
        self.setFixedSize(width, height)
        self.buttons = (self.optionsButton1, self.optionsButton2, self.optionsButton3, self.optionsButton4,
                        self.optionsButton5, self.optionsButton6, self.optionsButton7, self.optionsButton8)

        for index, button in enumerate(self.buttons):
            button.clicked.connect(self.make_call(index, button))

        self.acceptButton.clicked.connect(self.saveConfig)
        self.rejectButton.clicked.connect(self.close)
        self.themesComboBox.addItems(self.app.themes.keys())
        self.themesComboBox.setInsertPolicy(QComboBox.InsertAlphabetically)
        index = self.themesComboBox.findText(self.app.theme_name)
        self.themesComboBox.setCurrentIndex(index)
        self.refreshThemeButton.clicked.connect(lambda: self.app.refresh_theme())

        convo_opt = self.options["conversations"]
        chum_opt = self.options["chum_list"]
        interface_opt = self.options["interface"]

        # Chum List
        self.hideOfflineRadio.setChecked(chum_opt["hide_offline_chums"])
        self.showEmptyRadio.setChecked(chum_opt["show_empty_groups"])
        self.showNumberRadio.setChecked(chum_opt["show_number_of_online_chums"])
        self.sortChumsCombo.addItems(("Alphabetically", "Mood"))
        self.sortChumsCombo.setCurrentIndex(chum_opt["sort_chums"])
        self.lowBandwidthRadio.setChecked(chum_opt["low_bandwidth"])
        # Conversations
        self.timeStampsRadio.setChecked(convo_opt["time_stamps"])
        self.showSecondsRadio.setChecked(convo_opt["show_seconds"])
        self.opVoiceMemoRadio.setChecked(convo_opt["op_and_voice_in_memos"])
        self.animatedSmiliesRadio.setChecked(convo_opt["use_animated_smilies"])
        self.randomEncountersRadio.setChecked(convo_opt["receive_random_encounters"])
        self.clockTypeComboBox.addItems(('12', '24'))
        self.clockTypeComboBox.setCurrentIndex(convo_opt["clock_type"])
        # Interface
        self.tabbedConvoBox.setChecked(interface_opt["tabbed_conversations"])
        self.tabbedMemoBox.setChecked(interface_opt["tabbed_memos"])
        self.blinkPesterBox.setChecked(interface_opt["blink_taskbar_on_pesters"])
        self.blinkMemoBox.setChecked(interface_opt["blink_taskbar_on_memos"])
        self.minimizeCombo.addItems(('Minimize to Taskbar', 'Minimize to Tray', 'Quit'))
        self.minimizeCombo.setCurrentIndex(interface_opt["minimize"])
        self.closeCombo.addItems(('Minimize to Taskbar', 'Minimize to Tray', 'Quit'))
        self.closeCombo.setCurrentIndex(interface_opt["close"])

        self.show()

    def saveConfig(self):
        oldtheme = self.app.theme_name
        try:
            # Chum List
            self.options["chum_list"]["hide_offline_chums"] = self.hideOfflineRadio.isChecked()
            self.options["chum_list"]["show_empty_groups"] = self.showEmptyRadio.isChecked()
            self.options["chum_list"]["show_number_of_online_chums"] = self.showNumberRadio.isChecked()
            self.options["chum_list"]["sort_chums"] = self.sortChumsCombo.currentIndex()
            self.options["chum_list"]["low_bandwidth"] = self.lowBandwidthRadio.isChecked()
            # Conversations
            self.options["conversations"]["time_stamps"] = self.timeStampsRadio.isChecked()
            self.options["conversations"]["show_seconds"] = self.showSecondsRadio.isChecked()
            self.options["conversations"]["op_and_voice_in_memos"] = self.opVoiceMemoRadio.isChecked()
            self.options["conversations"]["use_animated_smilies"] = self.animatedSmiliesRadio.isChecked()
            self.options["conversations"]["receive_random_encounters"] = self.randomEncountersRadio.isChecked()
            self.options["conversations"]["clock_type"] = self.clockTypeComboBox.currentIndex()
            # Interface
            self.options["interface"]["tabbed_conversations"] = self.tabbedConvoBox.isChecked()
            self.options["interface"]["tabbed_memos"] = self.tabbedMemoBox.isChecked()
            self.options["interface"]["blink_taskbar_on_pesters"] = self.blinkPesterBox.isChecked()
            self.options["interface"]["blink_taskbar_on_memos"] = self.blinkMemoBox.isChecked()
            self.options["interface"]["minimize"] = self.minimizeCombo.currentIndex()
            self.options["interface"]["close"] = self.closeCombo.currentIndex()

            self.app.change_theme(self.themesComboBox.currentText())
        except Exception as e:
            self.errorLabel.setText("Error changing theme: \n{}".format(e))
            print(e)

        self.close()

    def make_call(self, index, button):
        def setIndex():
            self.stackedWidget.setCurrentIndex(index)
            button.setChecked(True)
            for Button in self.buttons:
                if button != Button:
                    Button.setChecked(False)

        return setIndex


class MemosWindow(QWidget):
    def __init__(self, app, parent):
        super(__class__, self).__init__()
        uic.loadUi(app.theme["ui_path"] + "/MemoWindow.ui", self)
        self.app = app
        self.parent = parent
        self.setWindowTitle('Memos')
        self.setWindowIcon(QIcon("resources/pc_chummy.png"))
        width = self.frameGeometry().width()
        height = self.frameGeometry().height()
        self.setFixedSize(width, height)
        self.memosTableWidget.setColumnCount(2)
        self.memosTableWidget.setHorizontalHeaderLabels(["Memo", "Users"])
        self.memosTableWidget.doubleClicked.connect(self.openMemo)
        header = self.memosTableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.ctr = 0
        self.servers = dict()
        self.open = dict()

        for server in self.app.client.servers:
            self.servers[server.name] = server
            self.add_channel(server.name, len(server.members))

        self.show()

    def join_button(self):
        name = self.memoNameLineEdit.text()
        if name:
            if not self.app.gui.memoTabWindow:
                self.app.gui.memoTabWindow = MemoTabWindow(self.app, self, name)
                self.close()
                return self.app.gui.memoTabWindow.init_memo
            else:
                self.close()
                return self.app.gui.memoTabWindow.add_memo(name)
        else:
            selected = self.memosTableWidget.selected()
            if not selected:
                return
            else:
                self.openMemo(selected[0])

    def display_message(self, channel, message):
        win = self.getWindow(channel.server)
        win.display_message(channel, message)

    def getWindow(self, server):
        if isinstance(server, discord.Server):
            return self.open[server]
        elif isinstance(server, str):
            return self.servers[server]
        else:
            return None

    def openMemo(self, index):
        server = self.servers[self.memosTableWidget.itemFromIndex(index).text()]
        tab = MemoTabWindow(self.app, self, server)
        self.open[server] = tab
        return tab.memo

    def add_channel(self, memo, usercount):
        self.memosTableWidget.insertRow(self.ctr)
        icn = QIcon(self.app.theme["path"] + "/memo.png")
        mitem = QTableWidgetItem(icn, memo)
        mitem.setFlags(Qt.ItemFlags(Qt.ItemIsSelectable) | Qt.ItemFlags(Qt.ItemIsEnabled))
        uitem = QTableWidgetItem()
        uitem.setData(0, usercount)
        uitem.setTextAlignment(2)
        uitem.setFlags(Qt.ItemFlags(Qt.ItemIsSelectable) | Qt.ItemFlags(Qt.ItemIsEnabled))
        self.memosTableWidget.setItem(self.ctr, 0, mitem)
        self.memosTableWidget.setItem(self.ctr, 1, uitem)
        self.ctr += 1

    def closeEvent(self, event):
        event.accept()
        self.app.gui.memosWindow = None


class MemoMessageWidget(QWidget):
    def __init__(self, app, container, parent, memo):
        '''
        The widget within each tab of TabWindow, a display
        for new private messages and user input
        '''
        super(__class__, self).__init__()
        self.parent = parent
        self.names = []
        uic.loadUi(app.theme["ui_path"] + "/MemoMessageWidget.ui", self)
        self.memo = memo
        self.app = app
        self.container = container
        self.names = self.memo.server.members

        self.memoUsers.setContextMenuPolicy(Qt.CustomContextMenu)
        self.memoUsers.customContextMenuRequested.connect(self.openMemoMenu)
        self.blockContext = QAction("BLOCK")
        self.blockContext.triggered.connect(self.block_selected)
        self.addFriendContext = QAction("ADD FRIEND")
        self.addFriendContext.triggered.connect(self.add_selected_friend)

        self.userLabel.setText(memo.name.join(["::", "::"]))
        self.sendButton.clicked.connect(self.send)
        self.userOutput.setReadOnly(True)
        self.userOutput.setMouseTracking(True)

        if not self.memo.permissions_for(self.memo.server.me).send_messages:
            self.userInput.setReadOnly(True)

    def send(self):
        """Send the user the message in the userInput box, called on enter press / send button press"""
        msg = self.userInput.text()
        if msg.strip():
            self.app.send_msg(msg, self.memo)
            self.userInput.setText("")

    def add_names(self):
        for user in self.names:
            self.add_user_item(user)

    def add_user_item(self, user):
        nam = user.name
        self.memoUsers.addItem(nam)
        itm = self.memoUsers.item(self.memoUsers.count() - 1)
        clr = user.color
        itm.setForeground(QColor(clr.r, clr.g, clr.b))

    def display_text(self, msg):
        '''Insert msg into the display box'''
        cursor = self.userOutput.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.userOutput.setTextCursor(cursor)
        self.userOutput.insertHtml(msg)

    def keyPressEvent(self, event):
        '''Use enter key to send'''
        if event.key() == Qt.Key_Return:
            self.send()

    def openMemoMenu(self, position):
        if indexes:
            menu = QMenu()
            menu.addAction(self.addFriendContext)
            menu.addAction(self.blockContext)
            menu.exec_(self.chumsTree.viewport().mapToGlobal(position))

    def block_selected(self):
        selected = self.memoUsers.selected()
        if selected:
            user = selected[0].text()
            if user not in self.app.blocked:
                self.app.add_blocked(user)

    def add_selected_friend(self):
        selected = self.memoUsers.selected()
        if selected:
            user = selected[0].text()
            if user not in self.app.friends.keys():
                self.app.add_friend(user)


class MemoTabWindow(QWidget):
    def __init__(self, app, parent, memo):
        """
        A window for storing PrivateMessageWidget instances, a navigation
        between current private message users
        """
        super(__class__, self).__init__()
        self.parent = parent
        self.app = app
        uic.loadUi(app.theme["ui_path"] + "/MemoTabWindow.ui", self)
        self.memo = memo
        self.channels = list(filter(lambda x: x.type is discord.ChannelType.text and x.permissions_for(x.server.me).read_messages, self.memo.channels))
        self.tabWidget.removeTab(0)  # Remove two default tabs
        self.tabWidget.removeTab(0)
        self.setWindowTitle("Memos")
        self.setWindowIcon(QIcon(self.app.theme["path"] + "/memo.png"))
        for channel in self.channels:
            self.add_memo(channel)

        self.add_user_items()

        self.show()

    def closeEvent(self, event):
        """On window (or tab) close send a PESTERCHUM:CEASE message to each user, destroy self"""
        try:
            del self.parent.open[self.memo.name]
            event.accept()
        except Exception as e:
            print(e)

    def display_message(self, channel, message):
        self.getWidget(channel).display_text(message)

    def getWidget(self, server):
        try:
            idx = self.channels.index(server)
            return self.tabWidget.widget(idx)
        except IndexError as e:
            print(e)
            return None

    def add_memo(self, memo):
        '''
        Add a user & PrivateMessageWidget to window, check if it is already there
        if so, return that user's PM, if not, create and return a PM
        On PrivateMessageWidget creation, send a PESTERCHUM:BEGIN initiation message
        '''
        windw = MemoMessageWidget(self.app, self.tabWidget, self, memo)
        icon = QIcon(self.app.theme["path"] + "/memo.png")
        a = self.tabWidget.addTab(windw, icon, memo.name)
        tab = self.tabWidget.widget(a)
        return tab

    def add_user_items(self):
        try:
            for member in self.memo.members:
                nam = QListWidgetItem(member.name)
                nam.setForeground(self.app.getColor(member, type=QColor))
                if member.top_role.permissions.administrator:
                    nam.setIcon(QIcon(self.app.theme["path"] + "/op.png"))
                for x in range(self.tabWidget.count()):
                    self.tabWidget.widget(x).memoUsers.addItem(nam)
        except Exception as e:
            print(e)


class AuthDialog(QDialog):
    def __init__(self, app, parent):
        """
        Dialog opened when the Add [Chum] button is pressed, adds to chumsTree widget
        """
        super(__class__, self).__init__()
        self.parent = parent
        self.app = app
        uic.loadUi(self.app.theme["ui_path"] + "/AuthDialog.ui", self)
        self.setWindowTitle('Add Chum')
        self.setWindowIcon(QIcon("resources/pc_chummy.png"))
        self.acceptButton.clicked.connect(self.accepted)
        self.closeButton.clicked.connect(self.rejected)
        self.auth = None
        self.exec_()

    def accepted(self):
        email = self.emailEdit.text()
        passwd = self.passEdit.text()
        token = self.tokenEdit.text()
        self.auth = (email,passwd,token)
        if email and passwd and token:
            self.errorLabel.setText("You must have either a email/pass OR a token (for bot accounts)")

        if not (email and passwd) and not token:
            self.errorLabel.setText("You must have BOTH an email and password OR a token")

        else:
            self.close()

    def rejected(self):
        if hasattr(self.app, "gui")
            self.close()
        else:
            self.app.exit()