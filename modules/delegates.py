from PySide6.QtWidgets import QStyledItemDelegate, QLineEdit, QComboBox, QCompleter, QStyle, \
    QStyleOptionButton, QApplication, QItemDelegate
from PySide6.QtCore import Qt, QEvent, QPoint, QRect
from PySide6.QtGui import QIntValidator
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
import re


class AgeDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        editor.setText(index.data(Qt.EditRole))
        return editor

    def setEditorData(self, editor, index):
        super(QStyledItemDelegate, self).setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        try:
            value = int(editor.text())
            if 0 <= value <= 120:
                model.setData(index, editor.text(), Qt.EditRole)
            else:
                model.setData(index, "", Qt.EditRole)
        except:
            model.setData(index, "", Qt.EditRole)


class DateAutoCorrectDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(DateAutoCorrectDelegate, self).__init__(parent)
        self.today = date.today()
        self.curr_month = self.today.month
        self.curr_year = self.today.year
        self.now = datetime.now()
        self.two_years_ago = self.now - relativedelta(years=2)

        self.format1 = "%Y-%m-%d"
        self.format2 = "%y-%m-%d"
        self.format3 = "%y%m%d"
        self.format4 = "%m-%d"
        self.format5 = "%m%d"
        self.format6 = "%d"

    def setModelData(self, editor, model, index):
        date_text = editor.text().strip()
        date_obj = None

        if not date_obj:
            try:
                date_obj = datetime.strptime(date_text, self.format1)
            except:
                pass

        if not date_obj:
            try:
                date_obj = datetime.strptime(date_text, self.format2)
            except:
                pass

        if not date_obj:
            try:
                date_obj = datetime.strptime(date_text, self.format3)
            except:
                pass

        if not date_obj:
            try:
                date_obj = datetime.strptime(date_text, self.format4)
                date_obj = date_obj.replace(year=self.curr_year)
            except:
                pass

        if not date_obj:
            try:
                date_obj = datetime.strptime(date_text, self.format5)
                date_obj = date_obj.replace(year=self.curr_year)
            except:
                pass

        if not date_obj:
            try:
                date_obj = datetime.strptime(date_text, self.format6)
                date_obj = date_obj.replace(year=self.curr_year, month=self.curr_month)
            except:
                pass

        if date_obj:
            print(date_obj.strftime("%Y-%m-%d"))

            if self.two_years_ago <= date_obj <= self.now:
                print("setting date")
                model.setData(index, date_obj.strftime("%Y-%m-%d"), Qt.EditRole)
                return True

        return False


class CompleterDelegate(QStyledItemDelegate):
    def __init__(self, parent=None, completerSetupFunction=None):
        super(CompleterDelegate, self).__init__(parent)
        self._completerSetupFunction = completerSetupFunction

    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        self._completerSetupFunction(editor, index)
        return editor

    def setEditorData(self, editor, index):
        super(CompleterDelegate, self).setEditorData(editor, index)

    def closeEditor(self, editor, hint=None):
        super(CompleterDelegate, self).closeEditor(editor, hint)

    def commitData(self, editor):
        super(CompleterDelegate, self).commitData(editor)


class ComboBoxDelegate(QStyledItemDelegate):
    def __init__(self, items, parent=None):
        super(ComboBoxDelegate, self).__init__(parent)
        self.items = items

    def createEditor(self, parent, option, index):
        editor = QComboBox(parent)
        editor.addItems(self.items)
        return editor

    def commit_editor(self):
        self.commitData.emit(self.sender())

    def setEditorData(self, editor, index):
        super(ComboBoxDelegate, self).setEditorData(editor, index)

    def closeEditor(self, editor, hint=None):
        super(ComboBoxDelegate, self).closeEditor(editor, hint)

    def commitData(self, editor):
        super(ComboBoxDelegate, self).commitData(editor)


class CheckBoxDelegate(QItemDelegate):
    """
    A delegate that places a fully functioning QCheckBox cell of the column to which it's applied.
    """
    def __init__(self, parent):
        QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        """
        Important, otherwise an editor is created if the user clicks in this cell.
        """
        return None

    def paint(self, painter, option, index):
        """
        Paint a checkbox without the label.
        """
        self.drawCheck(painter, option, option.rect, Qt.Unchecked if int(index.data()) == 0 else Qt.Checked)

    def editorEvent(self, event, model, option, index):
        '''
        Change the data in the model and the state of the checkbox
        if the user presses the left mousebutton and this cell is editable. Otherwise do nothing.
        '''
        if not int(index.flags() & Qt.ItemIsEditable) > 0:
            return False

        if event.type() == QEvent.MouseButtonRelease and event.button() == Qt.LeftButton:
            # Change the checkbox-state
            self.setModelData(None, model, index)
            return True

        return False

    def setModelData(self, editor, model, index):
        '''
        The user wanted to change the old state in the opposite.
        '''
        model.setData(index, 1 if int(index.data()) == 0 else 0, Qt.EditRole)
