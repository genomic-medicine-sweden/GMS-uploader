import yaml
import pkgutil
import pandas as pd
from pathlib import Path


class FX:
    def __init__(self):
        self.conf = yaml.safe_load(pkgutil.get_data(__name__, "conf.yaml"))

    def load_from_csv(self, path: Path):

        df = pd.read_csv(path, sep=';')
        df2 = df.dropna(subset=['Prov ID'])

        print(df2)

    def say_hey(self):
        print('hey')


if __name__ == '__main__':
    fx = FX()

