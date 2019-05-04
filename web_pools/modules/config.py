import os

# MAIN
project_name = "EVO file hosting"
project_scheme = "https"
project_domain = "evofiles.club"
project_config = os.path.dirname(__file__)
project_root = os.path.normpath(os.path.join(project_config, os.pardir, os.pardir))
cookie_secret = b'\xd2\x14\x19\x04tD\xb8\x9f.TO\xdd\xd0\xa7\x1f0x\x91Or\x99\xb5B)\xad\x08\x9b\xe7Y\xc1 \xfa'

def check_path(*args):
    path = os.path.join(*args)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


# FILES
path_level = 3
project_files = check_path(project_root,"files")
project_tmp = check_path(project_root,"tmp")
default_expiry = 100


# DATABASE
db = os.path.join(project_root, "web_pools", "db", "fhost.db")


# LOGS
project_logs = check_path(os.path.join(project_root,"logs", "project"))

LOGGING = dict(
    version = 1,
    disable_existing_loggers = False,
    formatters = {
        "format1" : {
            "format":"%(asctime)s.%(msecs)-3d %(name)s %(levelname)-5s in '%(module)s.py' at line %(lineno)d: %(message)s",
            "datefmt":"%Y-%m-%d %H:%M:%S"
        },
        "format2": {
            "format": "%(asctime)s.%(msecs)-3d %(message)s",
            "datefmt": "%H:%M:%S"

        }

    },
    handlers = {
        "console" : {
            "level" : "DEBUG",
            "class" : "logging.StreamHandler",
            "formatter" : "format2",
            "stream" : "ext://sys.stdout"
            },
        "main": {
            "level": "WARNING",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "format1",
            "filename": os.path.join(project_logs, "main.log"),
            "encoding": "utf8",
            "mode": "a",
            "maxBytes": 100000,
            "backupCount": 5
        },
        "aioserver": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "format1",
            "filename": os.path.join(check_path(project_logs, "aioserver"), "aioserver.log"),
            "encoding": "utf8",
            "mode": "a",
            "maxBytes": 100000,
            "backupCount": 5
        },
    },
    loggers = {
        "" : {
                "level" : "DEBUG",
                "handlers" : ["console", "main"]
            },
        "aioserver": {
            "level": "DEBUG",
            "handlers": ["aioserver", ]
        },
    }
)

