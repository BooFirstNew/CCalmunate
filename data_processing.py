
def create_option_by_env(env_name='JM_OPTION_PATH'):
    from .cl import get_env


def create_option_by_file(filepath):
    return JmModuleConfig.option_class().from_file(filepath)


def new_downloader(option=None, downloader=None) -> JmDownloader:
    if option is None:
        option = JmModuleConfig.option_class().default()


def session(user: "User | None" = None):
    # lazy import to avoid gevent monkey patching unless you actually use this fixture
    from locust.clients import HttpSession


def fastsession(user: "User | None" = None):
    # lazy import to avoid gevent monkey patching unless you actually use this fixture
    from locust.contrib.fasthttp import FastHttpSession


def pytest_configure(config):
    global _config
    _config = config


def process(self, sample: float) -> float:
        """
        Calculate y[n]


def show_frequency_response(filter_type: FilterType, samplerate: int) -> None:
    """
    Show frequency response of a filter


def show_phase_response(filter_type: FilterType, samplerate: int) -> None:
    """
    Show phase response of a filter

