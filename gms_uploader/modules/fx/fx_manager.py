import importlib
from pathlib import Path


class FxManager:
    def __init__(self, path: Path):
        self.fx_plugins = {'None': {'module': None, 'config': None}}

        for folder in path.glob('*'):
            print(folder)
            folder_name = folder.name
            print(folder_name)
            module = Path(folder, 'fx_plugin.py')
            config = Path(folder, 'fx_plugin.yaml')

            self.fx_plugins[folder_name] = {'module': module, 'config': config}

    def get_fx_plugin_names(self):
        return self.fx_plugins.keys()

    def get_fx_plugin(self, name):
        if name != 'None':
            return importlib.import_module('fx_plugin', "fx." + name)

        return None
        










