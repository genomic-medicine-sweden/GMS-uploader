from PySide6.QtWidgets import QStyledItemDelegate, QLineEdit, QComboBox, QCompleter, QStyle, \
    QStyleOptionButton, QApplication, QItemDelegate
from PySide6.QtCore import Qt, QEvent, QPoint, QRect
from PySide6.QtGui import QIntValidator
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
        self.max_delta = relativedelta(years=1, months=0, days=0)

        # possible date matches

        # year-month-day
        self.p1 = re.compile('(\d\d\d\d)-(\d\d)-(\d\d)$')
        # year-month-day
        self.p2 = re.compile('(\d\d)-(\d\d)-(\d\d)$')
        # year-month-day
        self.p3 = re.compile('(\d\d)(\d\d)(\d\d)$')
        # month-day
        self.p4 = re.compile('(\d\d)(\d\d)$')
        # day
        self.p5 = re.compile('(\d\d)$')

    def setModelData(self, editor, model, index):
        text = editor.text().strip()

        y, m, d = None, None, None

        m1 = self.p1.match(text)
        m2 = self.p2.match(text)
        m3 = self.p3.match(text)
        m4 = self.p4.match(text)
        m5 = self.p5.match(text)

        if m1 is not None:
            # extract year, month, day
            y, m, d = m3.groups()
        elif m2 is not None:
            # extract year, month, day
            y, m, d = m3.groups()
            y = "20" + y
        elif m3 is not None:
            # extract year, month, day
            y, m, d = m3.groups()
            y = "20" + y
        elif m4 is not None:
            # extract month, day
            # set current year
            m, d = m4.groups()
            y = self.curr_year
        elif m5 is not None:
            # extract day
            # set current month, year
            d = m5.group(1)
            y = self.curr_year
            m = self.curr_month

        if y and m and d:
            print(y)
            print(m)
            print(d)
            date_obj = self.date_validate(y, m, d)
            if date_obj:
                model.setData(index, date_obj.strftime("%Y-%m-%d"), Qt.EditRole)

    def date_validate(self, y, m, d):
        try:
            date_obj = date(int(y), int(m), int(d))
        except ValueError as e:
            return False

        if self.today < date_obj:
            return False

        delta = relativedelta(self.today - date_obj)

        delta_delta = delta - self.max_delta
        print(delta_delta)

        return date_obj


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
        print(self.items)

    def createEditor(self, parent, option, index):
        editor = QComboBox(parent)
        # editor.currentIndexChanged.connect(self.commit_editor)
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
