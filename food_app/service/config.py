import yaml
from typing import Optional, Union
from food_app.service.exceptions import BadConfig
from food_app.models.config import Config, PapaJohns

config = None


def get_config(
    config_name: str = 'config.yml', root: str = 'food_app', part: Optional[str] = None
) -> Union[Config, PapaJohns]:
    global config
    if config is None:
        with open(config_name, 'r') as stream:
            try:
                config = yaml.safe_load(stream)
            except yaml.YAMLError as ex:
                raise BadConfig(f'Got error when loading config: {ex}')
    result = Config(**config.get(root))
    if part is not None:
        return result.__getattribute__(part)
    return result
