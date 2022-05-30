import yaml
from typing import Optional, Union
from food_app.service.exceptions import BadConfig
from food_app.models.config import Config, PapaJohns, SuperApp

config = None


def get_config(
    root: str, config_name: str = 'config.yml', part: Optional[str] = None
) -> Union[Config, PapaJohns, SuperApp]:
    global config
    if config is None:
        with open(config_name, 'r') as stream:
            try:
                config = yaml.safe_load(stream)
            except yaml.YAMLError as ex:
                raise BadConfig(f'Got error when loading config: {ex}')
    result = Config(**config).__getattribute__(root)
    if part is not None:
        return result.__getattribute__(part)
    return result
