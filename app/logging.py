import json
import logging
import logging.config
import os
import json_log_formatter

LOGGING_SETUP_FILE = "/logging.json"

log_formatter = json_log_formatter.JSONFormatter()

current_file_path = os.path.abspath(__file__)

# 로그 디렉토리 생성 (없으면 자동 생성)
log_dir = os.path.join(os.path.dirname(current_file_path), "log")
os.makedirs(log_dir, exist_ok=True)  # 디렉토리가 없으면 생성

default_log_file = os.path.join(log_dir, "logfile.log")

# 기본 로깅 설정
DEFAULT_LOGGING_CONFIG = {
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "app.logging.CustomisedJSONFormatter"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "level": "INFO",
            "stream": "ext://sys.stdout"
        },
        "null": {
            "class": "logging.NullHandler"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "json",
            "filename": default_log_file,  # 절대 경로 사용
            "maxBytes": 10485760,
            "backupCount": 20,
            "encoding": "utf8"
        }
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "propagate": False
        },
        "uvicorn": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False
        },
        "uvicorn.error": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False
        },
        "uvicorn.access": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False
        }
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO"
    },
    "version": 1
}


def setup_logging(
    default_path=os.path.join(os.path.dirname(current_file_path), LOGGING_SETUP_FILE.lstrip("/")),
    default_level=logging.INFO,
    env_key="LOG_CFG"
):
    """
    Setup logging configuration
    """
    path = os.getenv(env_key, default_path)

    # 파일이 없으면 자동 생성
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)  # 디렉토리 자동 생성
        with open(path, "w") as f:
            json.dump(DEFAULT_LOGGING_CONFIG, f, indent=4)
        print(f"Default logging configuration file created at {path}")

    # 로깅 설정 적용
    with open(path, "rt") as f:
        config = json.load(f)
    logging.config.dictConfig(config)


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return super().default(obj)
        except TypeError:
            return f"<Non-serializable: {type(obj).__name__}>"


class CustomisedJSONFormatter(json_log_formatter.JSONFormatter):
    def to_json(self, record):
        if isinstance(record, logging.LogRecord):
            log_record = self.json_record(
                message=record.getMessage(),
                extra={},
                record=record
            )
        elif isinstance(record, dict):
            log_record = record
        else:
            log_record = {"message": str(record)}

        return json.dumps(log_record, ensure_ascii=False, cls=CustomEncoder)

    def json_record(self, message: str, extra: dict, record: logging.LogRecord) -> dict:
        extra["message"] = message
        extra["time"] = self.formatTime(record, self.datefmt)
        extra["level"] = record.levelname
        extra["name"] = record.name

        if record.exc_info:
            extra["exc_info"] = self.formatException(record.exc_info)

        return extra


class SpecificFileFilter(logging.Filter):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def filter(self, record):
        return self.filename in record.pathname
