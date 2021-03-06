from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt, Signal, QRect, QPoint, QEvent, QAbstractTableModel
from PySide6.QtWidgets import QStyledItemDelegate, QLineEdit, QComboBox


class PandasModel(QAbstractTableModel):
    def __init__(self, data, colprops, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._data = data
        self._col_props = colprops
        self._col_names = list(self._data.columns)

    def isempty(self, row):
        totlen = 0
        for item in row:
            totlen += len(item)
        if totlen == 0:
            return False
        else:
            return True

    def update_view(self):
#        self.dataChanged.emit(top_left_index, bottom_right_index)
        self.beginResetModel()

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
            if role == Qt.EditRole:
                return str(self._data.iloc[index.row(), index.column()])

        return None

    def setData(self, index, value, role) -> bool:

        if not index.isValid():
            return False
        # if role != Qt.EditRole:
        #     return False
        row = index.row()
        if row < 0 or row >= len(self._data.values):
            return False
        column = index.column()
        if column < 0 or column >= self._data.columns.size:
            return False

        self._data.iat[row, column] = value

        self.dataChanged.emit(index, index)

        return True

    def emit_changed(self):
        i1 = self.index(0, 0)
        i2 = self.index(self.rowCount() - 1, 0)
        self.dataChanged.emit(i1, i2)

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[section]
        if orientation == Qt.Horizontal and role == Qt.ToolTipRole:
            col_name = self._data.columns[section]
            # if 'tooltip' in self._fields_dict['model_fields'][col_name]:
            #     return self._fields_dict['model_fields'][col_name]['tooltip']

        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return section+1
        return None

    def flags(self, mi):
        """Reimplemented to set editable and movable status."""

        col_name = self._col_names[mi.column()]

        flags = (
                Qt.ItemIsSelectable
                | Qt.ItemIsEnabled
                | Qt.ItemIsDropEnabled
            )

        if self._col_props[col_name]['edit']:
            flags |= Qt.ItemIsEditable

        if self._col_props[col_name]['checkable']:
            flags |= Qt.ItemIsUserCheckable

        return flags

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        labels = list(self._data.index.values)

        self.beginRemoveRows(parent, position, position+rows-1)
        for r in range(position, position + rows):
            print(r, labels[r])
            self._data.drop(labels[r], inplace=True)
        self.endRemoveRows()

        return True

    def dropMarkedRows(self):
        indexes = []
        for row in range(self.rowCount()):
            index = self.index(row, 0)
            if self.data(index, role=Qt.DisplayRole) == "1":
                indexes.append(index)

        for index in reversed(sorted(indexes)):
            self.removeRows(index.row(), 1)
