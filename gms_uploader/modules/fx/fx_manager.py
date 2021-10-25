import importlib
from importlib.util import spec_from_loader, module_from_spec
from importlib.machinery import SourceFileLoader
from pathlib import Path


class FxManager:
    def __init__(self, plugin_path: Path):

        self.plugin_path = plugin_path

    def get_plugin_names(self):
        plugin_names = []
        for item in self.plugin_path.glob('*'):
            if item.is_dir():
                plugin_names.append(item.name)

        return plugin_names



    def get_fx_plugin_names(self):
        return self.fx_plugins.keys()

    def get_fx_plugin(self, name):
        if name != 'None':
            return importlib.import_module('fx_plugin', "fx." + name)

        return None

    def load_fx(self, plugin_name, plugin_path):
        loader = SourceFileLoader(plugin_name, plugin_path)
        spec = spec_from_loader(plugin_name, loader)
        plugin_module = module_from_spec(spec)
        spec.loader.exec_module(plugin_module)










