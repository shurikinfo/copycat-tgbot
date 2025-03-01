from typing import Any, Dict


class Config(Dict[str, Any]):
    """Конфигурация приложения"""

    def __init__(self) -> None:
        self.is_loaded = False
        super().__init__()

    def load(self, config: Dict[str, Any]) -> None:
        self.update(config)
        self.is_loaded = True

    def load_from_module(self, module_import_path: str) -> None:
        """Заполнить app.config словарём настроек"""
        _, tail = module_import_path.split(".", 1)
        conf_module = __import__(module_import_path, fromlist=[tail])
        self.load(conf_module.__dict__)
