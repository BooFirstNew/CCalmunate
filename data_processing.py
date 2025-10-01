
def create_option_by_env(env_name='JM_OPTION_PATH'):
    from .cl import get_env


def create_option_by_file(filepath):
    return JmModuleConfig.option_class().from_file(filepath)


def new_downloader(option=None, downloader=None) -> JmDownloader:
    if option is None:
        option = JmModuleConfig.option_class().default()

