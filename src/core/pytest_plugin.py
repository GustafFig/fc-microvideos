
import os
from typing import List

import pytest
from colorama import Fore, Style

def pytest_addoption(parser: pytest.Parser):
    parser.addoption(
        "--env",
        action="store",
        default="test",
        help="Environment to run tests againts from .env name"
    )

@pytest.hookimpl(tryfirst=True)
def pytest_load_initial_conftests(
    early_config: pytest.Config,  # pylint: disable=unused-argument
    parser: pytest.Parser,
    args: List[str],
):
    parser_args = parser.parse_known_args(args)
    env = parser_args.env
    os.environ.setdefault('APP_ENV', env)
    print(
        f"{Fore.BLUE}\n\n**** Running tests using .env.{env} ****\n\n{Style.RESET_ALL}"
    )

