from enum import Enum


class Output(str, Enum):
    # COMMA_DELIMITED = "comma-delimited"
    NEW_LINE_DELIMITED = "new-line-delimited"
    JSON = "json"
    TOML = "toml"
