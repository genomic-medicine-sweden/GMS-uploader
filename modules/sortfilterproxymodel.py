from PySide6.QtCore import Qt, QSortFilterProxyModel


class MultiSortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, *args, **kwargs):
        QSortFilterProxyModel.__init__(self, *args, **kwargs)
        self.multifilters = {}
        self.checkedfilter = False

    def setCheckedFilter(self):
        self.checkedfilter = True
        self.invalidateFilter()

    def clearCheckedFilter(self):
        self.checkedfilter = False
        self.invalidateFilter()

    def setFilterByColumns(self, columns, regex):
        for column in columns:
            self.multifilters[column] = regex
            self.invalidateFilter()

    def clearFilters(self):
        self.multifilters = {}
        self.invalidateFilter()

    def multifilterrow(self, source_row, source_parent):
        results = []
        for key, regex in self.multifilters.items():
            text = ''
            index = self.sourceModel().index(source_row, key, source_parent)
            if index.isValid():
                text = str(self.sourceModel().data(index, Qt.DisplayRole))
                if text is None:
                    text = ''

            if regex.match(text).hasMatch():
                results.append(True)
            else:
                results.append(False)

        return any(results)

    def checkedfilterrow(self, source_row, source_parent):
        index = self.sourceModel().index(source_row, 0, source_parent)
        if index.isValid():
            text = str(self.sourceModel().data(index, Qt.DisplayRole))
            if text is None:
                text = "0"

            if text == "1":
                return True

        return False

    def filterAcceptsRow(self, source_row, source_parent):
        mres = True
        if self.multifilters:
            mres = self.multifilterrow(source_row, source_parent)

        cres = True
        if self.checkedfilter:
            cres = self.checkedfilterrow(source_row, source_parent)

        if mres and cres:
            return True
        else:
            return False

    def dropMarkedRows(self):
        indexes = []
        for row in range(self.rowCount()):
            index = self.index(row, 0)
            if self.data(index, role=Qt.DisplayRole) == "1":
                indexes.append(index)

        for index in reversed(sorted(indexes)):
            self.removeRow(index.row())


class MarkedFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, *args, **kwargs):
        QSortFilterProxyModel.__init__(self, *args, **kwargs)
        self.filter = False

    def setFilter(self):
        self.filter = True
        self.invalidateFilter()

    def clearFilter(self):
        self.filter = False
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        index = self.sourceModel().index(source_row, 0, source_parent)
        value = self.sourceModel().data(index, Qt.DisplayRole)

        if self.filter and value == 1:
            return True

        elif not self.filter:
            return True

        return False


