import importlib
from importlib.util import spec_from_loader, module_from_spec
from importlib.machinery import SourceFileLoader
from pathlib import Path
import sys


class FxManager:
    def __init__(self, path: Path):
        self.plugin_path = path

    def get_fx_names(self):
        plugin_names = []
        for item in self.plugin_path.glob('*'):
            if item.is_dir():
                plugin_names.append(item.name)

        return plugin_names

    def load_fx(self, name):
        try:
            mod = importlib.import_module(f'fx.{name}.plugin')
            return mod.FX()
        except:
            return None


        # mod.FX.say_hey()
        # plugin = importlib.import_module('fx.analytix.plugin')


        # package = Path(self.plugin_path, name)
        # print(package, 'plugin.py')
        # spec = importlib.util.spec_from_file_location(name, self.plugin_path)
        # print(spec)
        # module = importlib.util.module_from_spec(spec)
        # spec.loader.exec_module(module)










