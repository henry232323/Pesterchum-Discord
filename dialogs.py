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

from PyQt5.QtGui import QIcon, QTextCursor, QStandardItem, QColor, QBrush, QTextDocument, QImage
from PyQt5.QtCore import Qt, pyqtSlot, QUrl
from PyQt5.QtWidgets import QDialog, QWidget, QListWidgetItem, QComboBox, QHeaderView, QTableWidgetItem, QAction, QMenu
from PyQt5 import uic

from traceback import format_exc
from contextlib import redirect_stdout
from asyncio import ensure_future
from async_timeout import timeout
from sys import exit as sysexit
from inspect import isawaitable
from io import StringIO
import discord

from formatting import *

import simpleaudio as sa


class PrivateMessageWidget(QWidget):
    def __init__(self, app, parent, user, name):
        """
        The widget within each tab of TabWindow, a display
        for new private messages and user input
        """
        super(__class__, self).__init__()
        uic.loadUi(app.theme["ui_path"] + "/PrivateMessageWidget.ui", self)
        self.user = user
        self.app = app
        self.parent = parent

        # setattr(user, "display_name", friend)
        self.userLabel.setText(name.join(["::", "::"]))
        self.sendButton.clicked.connect(self.send)
        self.userOutput.setReadOnly(True)
        self.userOutput.setMouseTracking(True)
        self.userOutput.anchorClicked.connect(self.anchorClicked)
        self.userOutput.setOpenLinks(False)

        if isinstance(user, discord.DMChannel):
            self.display_text(fmt_begin_msg(app, self.app.client.user, user.recipient))

        ensure_future(self.get_logs())

    @pyqtSlot(QUrl)
    def anchorClicked(self, url):
        urlstr = url.toString()
        if urlstr.startswith("mention="):
            id = urlstr[8:]
            user = discord.utils.get(self.app.client.get_all_members(), id=int(id))
            if user.id != self.app.client.user.id:
                self.app.gui.start_privmsg(user)
        elif urlstr.startswith("channel="):
            id = urlstr[8:]
            channel = discord.utils.get(self.memo.guild.channels, id=int(id))
            if channel.id != self.memo.id:
                self.parent.tabWidget.setCurrentIndex(self.parent.channels.index(channel))
        elif urlstr.startswith("role="):
            pass

    async def get_logs(self):
        ms = ""
        async for message in self.user.history(limit=100, oldest_first=True):
            fmt = fmt_disp_msg(self.app, message.content, message, user=message.author)
            ms += fmt
        self.display_text(ms)
        sa.WaveObject.from_wave_file(os.path.join(self.app.theme["path"], "alarm.wav")).play()

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
        self.setWindowIcon(QIcon(app.theme["path"] + "/trayicon.png"))
        self.show()

    def closeTab(self, currentIndex):
        widget = self.tabWidget.widget(currentIndex)
        widget.deleteLater()
        self.tabWidget.removeTab(currentIndex)
        self.users.remove(widget.user)
        if not self.users:
            self.close()

        sa.WaveObject.from_wave_file(os.path.join(self.app.theme["path"], "cease.wav")).play()

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
            if isinstance(user, discord.User):
                name = user.display_name
            elif isinstance(user, discord.GroupChannel):
                if not user.name:
                    name = ", ".join(map(lambda c: c.display_name, user.recipients))
                else:
                    name = user.name
            else:
                name = user.recipient.display_name

            windw = PrivateMessageWidget(self.app, self, user, name)
            icon = QIcon("resources/pc_chummy.png")
            a = self.tabWidget.addTab(windw, icon, name)
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
        self.setWindowIcon(QIcon(app.theme["path"] + "/trayicon.png"))
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
        self.setWindowIcon(QIcon(app.theme["path"] + "/trayicon.png"))
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
        self.setWindowIcon(QIcon(app.theme["path"] + "/trayicon.png"))
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
        self.setWindowIcon(QIcon(app.theme["path"] + "/trayicon.png"))
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
        self.refreshThemeButton.clicked.connect(lambda: self.app.change_theme(self.themesComboBox.currentText(), f=True))

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
        # Updates
        self.pesterchumUpdatesCheck.setChecked(int(interface_opt["auto_update"]))
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
            # Updates
            self.options["interface"]["auto_update"] = self.pesterchumUpdatesCheck.isChecked()

            self.app.change_theme(self.themesComboBox.currentText())
            # Theme
            self.options["theme"]["theme"] = self.themesComboBox.currentText()
        except Exception as e:
            self.errorLabel.setText("Error changing theme: \n{}".format(e))
            self.app.change_theme(oldtheme)
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
        self.setWindowIcon(QIcon(app.theme["path"] + "/trayicon.png"))
        #width = self.frameGeometry().width()
        #height = self.frameGeometry().height()
        #self.setFixedSize(width, height)
        self.memosTableWidget.setColumnCount(2)
        self.memosTableWidget.setHorizontalHeaderLabels(["Memo", "Users"])
        self.memosTableWidget.doubleClicked.connect(self.openMemo)
        header = self.memosTableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.ctr = 0
        self.open = dict()
        for guild in self.app.client.guilds:
            self.add_channel(guild.name, len(guild.members))
        self.memosTableWidget.sortItems(0)
        self.joinMemoButton.clicked.connect(self.join_button)

        self.show()

    def join_button(self):
        name = self.memoNameLineEdit.text()
        if name:
            try:
                items = self.memosTableWidget.findItems(name, Qt.MatchExactly)
                self.openMemo(self.memosTableWidget.indexFromItem(items[0]))
            except:
                import traceback; traceback.print_exc()
        else:
            selected = self.memosTableWidget.selectedItems()
            if not selected:
                return
            else:
                self.openMemo(selected[0])

    def display_message(self, channel, message):

        win = self.getWindow(channel.guild)
        win.display_message(channel, message)

    def getWindow(self, guild):
        if isinstance(guild, discord.Guild):
            return self.open[guild]
        elif isinstance(guild, str):
            return discord.utils.get(self.app.client.guilds, name=guild)
        else:
            return None

    def openMemo(self, index):
        if index.column():
            index = index.sibling(index.row(), 0)
        item = self.memosTableWidget.itemFromIndex(index)
        guild = discord.utils.get(self.app.client.guilds, name=item.text())
        tab = MemoTabWindow(self.app, self, guild)
        self.open[guild] = tab
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
        """
        The widget within each tab of TabWindow, a display
        for new private messages and user input
        """
        super(__class__, self).__init__()
        self.parent = parent
        self.names = []
        uic.loadUi(app.theme["ui_path"] + "/MemoMessageWidget.ui", self)
        self.memo = memo
        self.app = app
        self.container = container
        self.names = self.memo.guild.members

        self.memoUsers.setContextMenuPolicy(Qt.CustomContextMenu)
        self.memoUsers.customContextMenuRequested.connect(self.openMemoMenu)
        self.messageContext = QAction("MESSAGE")
        self.messageContext.triggered.connect(self.message_user)
        self.blockContext = QAction("BLOCK")
        self.blockContext.triggered.connect(self.block_user)
        self.blockContext = QAction("UNBLOCK")
        self.blockContext.triggered.connect(self.unblock_user)
        self.friendContext = QAction("ADD FRIEND")
        self.friendContext.triggered.connect(self.send_friend_request)
        self.removeContext = QAction("REMOVE FRIEND")
        self.removeContext.triggered.connect(self.remove_friend)

        self.userLabel.setText(memo.name.join(["::", "::"]))
        self.sendButton.clicked.connect(self.send)
        self.userOutput.setReadOnly(True)
        self.userOutput.setMouseTracking(True)
        self.userOutput.anchorClicked.connect(self.anchorClicked)
        self.userOutput.setOpenLinks(False)
        self.userOutput.document().setDefaultStyleSheet(self.app.theme["styles"])
        self.userOutput.setHtml("<body>\n</body>")

        if not self.memo.permissions_for(self.memo.guild.me).send_messages:
            self.userInput.setReadOnly(True)

        ensure_future(self.load_emojis())
        ensure_future(self.get_logs())

    async def load_emojis(self):
        for emoji in self.memo.guild.emojis:
            with timeout(10):
                async with self.app.session.get(emoji.url) as response:
                    img = await response.read()
                    qmg = QImage()
                    qmg.loadFromData(img)
                    self.userOutput.document().addResource(QTextDocument.ImageResource, QUrl(emoji.url), qmg)

    @pyqtSlot(QUrl)
    def anchorClicked(self, url):
        urlstr = url.toString()
        if urlstr.startswith("mention="):
            id = urlstr[8:]
            user = discord.utils.get(self.app.client.get_all_members(), id=int(id))
            if user.id != self.app.client.user.id:
                self.app.gui.start_privmsg(user)
        elif urlstr.startswith("channel="):
            id = urlstr[8:]
            channel = discord.utils.get(self.memo.guild.channels, id=int(id))
            if channel.id != self.memo.id:
                self.parent.tabWidget.setCurrentIndex(self.parent.channels.index(channel))
        elif urlstr.startswith("role="):
            pass

    async def get_logs(self):
        ms = ""
        async for message in self.memo.history(limit=100, reverse=True):
            fmt = fmt_disp_msg(self.app, message.content, message, user=message.author)
            ms += fmt
        self.display_text(ms)

    def send(self):
        """Send the user the message in the userInput box, called on enter press / send button press"""
        msg = self.userInput.text()
        if msg.strip():
            self.app.send_msg(msg, self.memo)
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

    def openMemoMenu(self, position):
        menu = QMenu()
        selected = self.memoUsers.selectedItems()
        if selected:
            user = selected[0].text()
            member = self.memo.guild.get_member_named(user)
            if self.app.client.user.bot and member is not self.memo.guild.me:
                menu.addAction(self.messageContext)

            elif member is not self.memo.guild.me:
                menu.addAction(self.messageContext)

                if member.is_friend():
                    menu.addAction(self.removeContext)
                else:
                    menu.addAction(self.friendContext)

                if member.is_blocked():
                    menu.addAction(self.removeBlockContext)
                else:
                    menu.addAction(self.blockContext)

            else:
                return

        menu.exec_(self.memoUsers.viewport().mapToGlobal(position))

    def message_user(self):
        selected = self.memoUsers.selectedItems()
        if selected:
            user = selected[0].text()
            member = self.memo.guild.get_member_named(user)
            if member.id != self.app.client.user.id:
                ensure_future(self.app.gui.start_pm(member))

    def block_user(self):
        selected = self.memoUsers.selectedItems()
        if selected:
            user = selected[0].text()
            member = self.memo.guild.get_member_named(user)
            if member.id != self.app.client.user.id:
                ensure_future(user.block())

    def unblock_user(self):
        selected = self.memoUsers.selectedItems()
        if selected:
            user = selected[0].text()
            member = self.memo.guild.get_member_named(user)
            if member.id != self.app.client.user.id:
                ensure_future(user.unblock())

    def send_friend_request(self):
        selected = self.memoUsers.selectedItems()
        if selected:
            user = selected[0].text()
            member = self.memo.guild.get_member_named(user)
            if member.id != self.app.client.user.id:
                ensure_future(user.send_friend_request())

    def remove_friend(self):
        selected = self.memoUsers.selectedItems()
        if selected:
            user = selected[0].text()
            member = self.memo.guild.get_member_named(user)
            if member.id != self.app.client.user.id:
                ensure_future(user.remove_friend())


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

        # Filter channels by read permission
        self.channels = list(filter(lambda x: x.permissions_for(x.guild.me).read_messages, self.memo.text_channels))

        # Remove two default tabs
        self.tabWidget.removeTab(0)
        self.tabWidget.removeTab(0)

        self.setWindowTitle("Memos")
        self.setWindowIcon(QIcon(self.app.theme["path"] + "/memo.png"))
        for channel in self.channels:
            self.add_memo(channel)

        self.add_user_items()

        self.show()
        sa.WaveObject.from_wave_file(os.path.join(self.app.theme["path"], "alarm2.wav")).play()

    def closeEvent(self, event):
        """On window (or tab) close send a PESTERCHUM:CEASE message to each user, destroy self"""
        del self.parent.open[self.memo]
        event.accept()
        sa.WaveObject.from_wave_file(os.path.join(self.app.theme["path"], "cease.wav")).play()

    def display_message(self, channel, message):
        self.getWidget(channel).display_text(message)

    def getWidget(self, guild):
        try:
            idx = self.channels.index(guild)
            return self.tabWidget.widget(idx)
        except IndexError as e:
            print(e)

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
        for member in sorted(self.memo.members, key=lambda x: (max([r.position for r in x.roles if r.hoist], default=0), x.display_name), reverse=True):
            nam = QListWidgetItem(member.display_name)
            clra = member.color
            clr = QBrush()
            clr.setColor(QColor(clra.r, clra.g, clra.b))
            nam.setForeground(clr)
            if member.top_role.permissions.administrator:
                nam.setIcon(QIcon(self.app.theme["path"] + "/op.png"))
            widget = self.tabWidget.widget(0)
            widget.memoUsers.addItem(nam)


class AuthDialog(QDialog):
    def __init__(self, app, parent, f=False, i=True):
        """
        Dialog opened when the Add [Chum] button is pressed, adds to chumsTree widget
        """
        super(__class__, self).__init__()
        self.parent = parent
        self.app = app
        self.i = i
        self.fin = False
        uic.loadUi(self.app.theme["ui_path"] + "/AuthDialog.ui", self)
        self.setWindowTitle('Auth')
        self.setWindowIcon(QIcon(app.theme["path"] + "/trayicon.png"))
        self.acceptButton.clicked.connect(self.accepted)
        self.acceptButton.setDefault(True)
        self.closeButton.clicked.connect(self.rejected)
        if f:
            self.errorLabel.setText("""Invalid token! Failed to login. Make sure if you are using a bot to check the bot account check""")
        else:
            self.errorLabel.setText("""Discord no longer allows usernames/passwords!
Check the README for how to find yours!""")
        self.auth = None
        self.exec_()

    def accepted(self):
        token = self.tokenEdit.text().strip("\"")
        bot = self.botCheck.isChecked()
        self.auth = (token, bot)
        if not token:
            return
        else:
            self.fin = True
            self.close()

    def rejected(self):
        if hasattr(self.app, "gui"):
            self.close()
        else:
            self.app.exit()

    def closeEvent(self, event):
        if self.i and not self.fin:
            event.accept()
            self.app.exit()
        else:
            event.accept()


class QuirksWindow(QWidget):
    def __init__(self, app):
        super(__class__, self).__init__()
        self.app = app
        uic.loadUi(self.app.theme["ui_path"] + "/QuirksWindow.ui", self)
        self.addQuirkButton.clicked.connect(self.openQuirk)
        self.editQuirkButton.clicked.connect(self.editQuirk)
        self.removeQuirkButton.clicked.connect(self.removeQuirk)
        self.cancelButton.clicked.connect(self.closeWin)
        self.okButton.clicked.connect(self.save)
        self.testButton.clicked.connect(self.testQuirks)
        for type, quirk in self.app.quirks.quirks:
            self.quirksList.addItem("{}:{}".format(type, quirk))

        self.setWindowTitle('Quirks')
        self.setWindowIcon(QIcon(app.theme["path"] + "/trayicon.png"))

        self.show()

    def openQuirk(self):
        AddQuirkWindow(self.app, self)

    def editQuirk(self):
        pass

    def removeQuirk(self):
        items = self.quirksList.selectedItems()
        for item in items:
            row = self.quirksList.indexFromItem(item).row()
            self.app.quirks.quirks.pop(row)
            self.quirksList.takeItem(row)

    def closeWin(self):
        self.close()

    def save(self):
        self.close()

    def testQuirks(self):
        pass


class AddQuirkWindow(QWidget):
    def __init__(self, app, parent):
        super(__class__, self).__init__()
        self.app = app
        self.parent = parent
        uic.loadUi(self.app.theme["ui_path"] + "/AddQuirkWindow.ui", self)

        self.buttons = ('opts', 'prefix', 'suffix', 'replace', 'regex', 'random')
        self.setWindowTitle('Quirks')
        self.setWindowIcon(QIcon(app.theme["path"] + "/trayicon.png"))

        enableNext = lambda: self.nextButton.setEnabled(True)
        self.nextButton.setEnabled(False)
        self.prefixRadio.clicked.connect(enableNext)
        self.suffixRadio.clicked.connect(enableNext)
        self.replaceRadio.clicked.connect(enableNext)
        self.regexRadio.clicked.connect(enableNext)
        self.randomRadio.clicked.connect(enableNext)

        self.nextButton.clicked.connect(self.next)
        self.nextButton_2.clicked.connect(self.next)
        self.nextButton_3.clicked.connect(self.next)
        self.nextButton_4.clicked.connect(self.next)
        self.nextButton_5.clicked.connect(self.next)
        self.nextButton_6.clicked.connect(self.next)

        self.backButton.clicked.connect(self.back)
        self.backButton_2.clicked.connect(self.back)
        self.backButton_3.clicked.connect(self.back)
        self.backButton_4.clicked.connect(self.back)
        self.backButton_5.clicked.connect(self.back)
        self.backButton_6.clicked.connect(self.back)

        self.cancelButton.clicked.connect(self.close)
        self.cancelButton_2.clicked.connect(self.close)
        self.cancelButton_3.clicked.connect(self.close)
        self.cancelButton_4.clicked.connect(self.close)
        self.cancelButton_5.clicked.connect(self.close)
        self.cancelButton_6.clicked.connect(self.close)

        self.addRandomButton.clicked.connect(self.addRandom)
        self.removeRandomButton.clicked.connect(self.removeRandom)
        self.reloadFuncs.clicked.connect(self.reload_functions)
        self.randReloadFuncs.clicked.connect(self.rand_reload_functions)

        self.randomRegex = list()

        self.show()

    def back(self):
        self.stackWidget.setCurrentIndex(0)

    def next(self):
        index = self.stackWidget.currentIndex()
        if index == 0:
            if self.prefixRadio.isChecked():
                self.stackWidget.setCurrentIndex(1)
            elif self.suffixRadio.isChecked():
                self.stackWidget.setCurrentIndex(2)
            elif self.replaceRadio.isChecked():
                self.stackWidget.setCurrentIndex(3)
            elif self.regexRadio.isChecked():
                self.stackWidget.setCurrentIndex(4)
                self.addFuncs()
            elif self.randomRadio.isChecked():
                self.stackWidget.setCurrentIndex(5)
                self.randAddFuncs()
        elif index == 1:
            value = self.prefixLineEdit.text()
            self.app.quirks.append(("prefix", value,))
        elif index == 2:
            value = self.suffixLineEdit.text()
            self.app.quirks.append(("suffix", value,))
        elif index == 3:
            value = (self.replaceReplaceLineEdit.text(), self.replaceWithLineEdit.text())
            self.app.quirks.append(("replace", value,))
        elif index == 4:
            replace = self.regexpReplaceLineEdit.text()
            fm = self.regexpLineEdit.text()
            if not ("(" in fm and ")" in fm):
                fm = "({})".format(fm)
            value = (fm, replace)
            self.app.quirks.append(("regex", value,))
        elif index == 5:
            fm = self.randomRegexpLineEdit.text()
            if not ("(" in fm and ")" in fm):
                fm = "({})".format(fm)
            value = (fm, tuple(self.randomRegex))
            self.app.quirks.append(("random", value,))
        if index != 0:
            self.parent.quirksList.addItem("{}:{}".format(self.buttons[index], value))
            self.close()

    def addRandom(self):
        nq = self.addRandomLineEdit.text()
        self.randomList.addItem(nq)
        self.randomRegex.append(nq)
        self.addRandomLineEdit.setText("")

    def removeRandom(self):
        items = self.randomList.selectedItems()
        for item in items:
            self.randomRegex.remove(item.text())
            self.randomList.takeItem(self.randomList.indexFromItem(item).row())

    def randAddFuncs(self):
        for func in self.app.quirks.qfuncs.values():
            self.randRegexFuncs.addItem(func.__name__ + "()")

    def addFuncs(self):
        for func in self.app.quirks.qfuncs.values():
            self.regexFuncs.addItem(func.__name__ + "()")

    def reload_functions(self):
        self.regexFuncs.reset()
        self.app.quirks.reload()
        self.addFuncs()

    def rand_reload_functions(self):
        self.randRegexFuncs.reset()
        self.app.quirks.reload()
        self.addFuncs()


class ConnectingDialog(QDialog):
    def __init__(self, app, parent):
        super(__class__, self).__init__()
        uic.loadUi(app.theme["ui_path"] + "/ConnectingDialog.ui", self)
        self.app = app
        self.parent = parent
        self.app.connectingDialog = self
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.connectingExitButton.clicked.connect(sysexit)
        self.setWindowTitle('Connecting')
        self.setWindowIcon(QIcon(app.theme["path"] + "/trayicon.png"))
        self.app.connectingDialog = self
        width = self.frameGeometry().width()
        height = self.frameGeometry().height()
        self.setFixedSize(width, height)

    # Methods for moving window
    @pyqtSlot()
    def mousePressEvent(self, event):
        self.offset = event.pos()

    @pyqtSlot()
    def mouseMoveEvent(self, event):
        x = event.globalX()
        y = event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.move(x - x_w, y - y_w)


class InteractiveConsole(QWidget):
    def __init__(self, app):
        super(__class__, self).__init__()
        uic.loadUi(app.theme["ui_path"] + "/PrivateMessageWidget.ui", self)
        self.app = app

        self.userLabel.setText("::DEBUG::")
        self.setWindowTitle("Debug")
        self.setWindowIcon(QIcon("resources/sburb.png"))
        self.sendButton.clicked.connect(self.send)
        self.sendButton.setText("GO!")
        self.userOutput.setReadOnly(True)
        self.userOutput.setMouseTracking(True)

        self.show()

    def send(self):
        msg = self.userInput.text()
        if msg:
            self.display_text(">>> {}\n".format(msg))
            ensure_future(self.run(msg))
            self.userInput.setText("")

    def display_text(self, msg):
        if not msg.endswith("\n"):
            msg += "\n"
        cursor = self.userOutput.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.userOutput.setTextCursor(cursor)
        self.userOutput.insertPlainText(msg)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.send()

    def get_syntax_error(self, e):
        return '{0.text}{1:>{0.offset}}\n{2}: {0}'.format(e, '^', type(e).__name__)

    async def run(self, msg):
        msg = msg.replace("\\n", "\n")
        app = self.app
        client = self.app.client
        gui = self.app.gui
        executor = exec
        if msg.count('\n') == 0:
            # single statement, potentially 'eval'
            try:
                code = compile(msg, '<repl>', 'eval')
            except SyntaxError:
                pass
            else:
                executor = eval

        if executor is exec:
            try:
                code = compile(msg, '<repl>', 'exec')
            except SyntaxError as e:
                self.display_text(self.get_syntax_error(e))
                return

        fmt = None
        stdout = StringIO()

        try:
            with redirect_stdout(stdout):
                result = executor(code)
                if isawaitable(result):
                    result = await result

        except Exception as e:
            value = stdout.getvalue()
            fmt = '{}{}'.format(value, format_exc())
        else:
            value = stdout.getvalue()
            if result is not None:
                fmt = '{}{}'.format(value, result)
            elif value:
                fmt = '{}'.format(value)

        if fmt is not None:
            if len(fmt) > 2000:
                self.display_text('Content too big to be printed.')
            else:
                self.display_text(fmt)
