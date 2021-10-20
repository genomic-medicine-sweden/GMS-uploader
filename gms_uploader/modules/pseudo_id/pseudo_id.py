from pathlib import Path
from ..settings.settings import Settings


class PseudoID:
    """ Class for setting, getting pseudo_id filepaths and getting pseudo_id value  """
    def __init__(self, conf):
        self._settings = Settings(conf)
        self.conf = conf
        self.l2c = self.conf['tr']['lab_to_code']

    def get_filepath(self):
        return self._settings.get_value('entered_value_button', 'pseudo_id_filepath')

    def set_filepath(self, value):
        self._settings.set_value('entered_value', 'pseudo_id_filepath', value)

    def _zfill_int(self, value: int) -> str:
        number_str = str(value)
        return number_str.zfill(8)

    def get_pid(self) -> str or bool:
        pseudo_id_filepath = self._settings.get_value('entered_value', 'pseudo_id_filepath')
        if not Path(pseudo_id_filepath).is_file():
            return None

        lab = self._settings.get_value('select_single', 'lab')
        last_pid_num = self._get_last_pid_num()

        if not lab:
            return None

        if not last_pid_num:
            last_pid_num = 0

        new_pid_num = last_pid_num + 1

        return self.l2c[lab] + "-" + self._zfill_int(new_pid_num)

    def _get_last_pid_num(self) -> int:
        fp = Path(self.get_filepath())

        if not fp.is_file():
            return False

        lines = fp.read_text(enconding='utf-8').splitlines()

        if not lines:
            return False

        return int(lines[-1].split('-')[-1])
