from dataclasses import dataclass
from environs import Env


@dataclass
class BotSettings:
    token: str
    ban_list: list[int]


@dataclass
class LogSettings:
    level: str
    format: str
    style: str


@dataclass
class Config:
    bot: BotSettings
    log: LogSettings


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        BotSettings(
            token=env("BOT_TOKEN"), ban_list=env.list("BOT_BAN_LIST", subcast=int)
        ),
        LogSettings(
            level=env("LOG_LEVEL"), format=env("LOG_FORMAT"), style=env("LOG_STYLE")
        ),
    )
