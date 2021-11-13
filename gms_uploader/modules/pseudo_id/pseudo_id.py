from pathlib import Path
# from ..settings.settings import Settings
# from ..dialogs.dialogs import MsgError
import pandas as pd


class PseudoIDManager:
    """ Class for setting, getting pseudo_id filepaths and getting pseudo_id value  """
    def __init__(self): #, conf: dict):
        # self._settings = Settings(conf)
        # self._conf = conf
        # self._l2c = conf['tr']['lab_to_code']

        self._df_cols = ['pseudo_id', 'internal_lab_id', 'pid_num', 'lab_code', 'submitter', 'timestamp']
        self._submitter = None
        self._lab_code = None
        self._file = None
        self._df = None
        self._first_pid = None

        self._set_file()
        self._set_lab_code()
        self._read_csv()
        self._mk_first_pid()
        self._set_submitter()

    def ready(self):
        """
        Checks if all required settings have been entered.
        :return: bool
        """
        return all([self._submitter, self._lab_code, self._file, self._df])

    def _set_submitter(self):
        # lab = self._settings.get_value('select_single', 'lab')
        # if lab is not None:
        #     pass

        self._submitter = "Pär Larsson"

    def _validate_lids(self, lids: list) -> bool:
        """
        Validates a list of internal_lab_ids
        :param lids: list of internal_lab_ids
        :return: bool
        """
        res = []
        for lid in lids:
            res.append(self._is_valid_lid(lid))

        if all(res):
            return True
        else:
            return False

    def _validate_pidlids(self, pidlids: list) -> bool:
        """
        Validates a list of tuples with internal_lab_id and pseudo_id by checking against previous
        :param lids: list of internal_lab_ids
        :return: bool
        """
        res = []
        for pidlid in pidlids:
            pid, lid = pidlid
            res.append(self._is_valid_lid(lid))
            res.append(self._is_valid_pid(pid))

        if all(res):
            return True
        else:
            return False

    def _is_valid_lid(self, lid: str) -> bool:
        if self._df is None:
            return False

        if lid in self._df['internal_lab_id'].values:
            return False

        return True

    def _is_valid_pid(self, pid: str) -> bool:
        if pid in self._df['pseudo_id'].values:
            return False

        return True

    def write_pidlids_to_csv(self, pidlids: list):
        """

        :param pidlids: list of pseudo_id and internal_lab_id tuples (pseudo_id, internal_lab_id)
        :return:
        """

        rows = []

        for pidlid in pidlids:
            pid, lid = pidlid
            pid_num = self._pid_to_num(pid)
            lab_code = self._pid_to_lab_code(pid)

            row = {'lab_code': lab_code,
                   'pid_num': pid_num,
                   'pseudo_id': pid,
                   'internal_lab_id': lid,
                   'submitter': self._submitter,
                   'timestamp': str(pd.Timestamp.now())}

            rows.append(row)

        print(rows)

        print("in write", self._df)

        if self._df is not None:
            self._df = self._df.append(rows, ignore_index=True)
            print(self._df)
            self._df.to_csv(self._file, index=False)

    def generate_pids_from_lids(self, lids: list) -> list:
        """
        Validates list of lids to ensure uniqueness, then generates equal number of unique pids
        :param lids: list of internal_lab_ids
        :return: list of generated pids
        """

        if not isinstance(lids, list):
            return []

        if not self._validate_lids(lids):
            print("failed lid validation")
            return []

        size = len(lids)

        if self._df is None or size == 0:
            return []

        if self._lab_code is None:
            return []

        pids = []

        if self._df.empty:
            first_num = 1
            last_num = first_num + size

            for i in range(first_num, last_num):
                pids.append(self._mk_pid(i))

        else:
            last_row = self._df.iloc[-1]

            first_num = last_row['pid_num'] + 1
            last_num = first_num + size

            for i in range(first_num, last_num):
                pids.append(self._mk_pid(i))

        return pids

    def get_first_pid(self):
        return self._first_pid

    def _mk_first_pid(self):
        if self._df is None:
            return

        if self._lab_code is None:
            return

        if self._df.empty:
            self._first_pid = self._mk_pid(1)
        else:
            last_row = self._df.iloc[-1]
            num = last_row['pid_num'] + 1
            self._first_pid = self._mk_pid(num)

    def _mk_pid(self, num: int) -> str:
        num_str = self._int_zfill(num)
        return f"{self._lab_code}-{num_str}"

    def _set_file(self):
        # file = self._settings.get_value('entered_value', 'pseudo_id_filepath')
        # if file is not None:
        #     self._file = Path(file)
        f = 'D:/data/test.csv'
        print(f)

        if self._is_valid_filepath(f):
            self._file = Path(f)

    def _set_lab_code(self):
        # lab = self._settings.get_value('select_single', 'lab')
        # if lab is not None:
        #     pass

        self._lab_code = "SE720"

    @staticmethod
    def _pid_to_lab_code(pid: str) -> str:
        lab_code, _ = pid.split('-')
        return lab_code

    @staticmethod
    def _pid_to_num(pid: str) -> int:
        _, no_str = pid.split('-')
        return int(no_str)

    def _create_csv(self):
        if self._file is None:
            return

        if self._file.is_file():
            return

        if self._file.parent.is_dir():
            _df = pd.DataFrame(columns=self._df_cols)
            _df.to_csv(self._file, index=False)

    @staticmethod
    def _is_valid_filepath(file: str) -> bool:
        try:
            fobj = Path(file)
            if fobj.parent.is_dir():
                return True
            else:
                return False
        except:
            return False

    def _read_csv(self):
        """ read the csv into a pandas df, perform various validity checks"""

        if self._file is None:
            self._df = None
            return

        if not self._file.is_file():
            self._create_csv()

        try:
            self._df = pd.read_csv(self._file)
            if set(self._df.columns) != set(self._df_cols):
                print("pseudo_id file is incompatible")
                self._df = None
                return
        except:
            self._df = None
            return

        lab_code_set = set(self._df['lab_code'])

        if len(lab_code_set) > 1:
            self._df = None
            return

        if len(lab_code_set) == 1 and self._lab_code not in lab_code_set:
            self._df = None
            return

        if not self._df['pid_num'].is_monotonic_increasing:
            self._df = None
            return

    def _write_csv(self):
        if self._df is not None:
            self._df.to_csv(self._file, index=False, columns=self._df_cols)

    def _int_zfill(self, value: int) -> str:
        number_str = str(value)
        return number_str.zfill(8)


if __name__ == '__main__':

    pidm = PseudoIDManager()
    print(pidm.get_first_pid())

    lids = [
        'test5',
        'test6',
        'test7',
        'test8'
    ]

    pids = pidm.generate_pids_from_lids(lids)
    print(pids)

    pidlids = list(zip(pids, lids))

    print(pidlids)

    pidm.write_pidlids_to_csv(pidlids)

