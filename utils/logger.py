import logging
import logging.config
import os
from logging.handlers import TimedRotatingFileHandler

# 判断是否为调试模式
debug_flag = 0


# 自定义过滤器
class RequireDebugTrue(logging.Filter):
    def filter(self, record):
        return debug_flag


# 日志配置函数
def logger_config(env):
    # 根据环境设置日志文件路径
    if env == "dev":
        path = r'E:\my_works\WuShiMiDong\ChineseTextClassificationBert\logs\dev'  # 开发环境日志路径
    else:
        path = r'E:\my_works\WuShiMiDong\ChineseTextClassificationBert\logs\prod'  # 生产环境日志路径

    BASE_DIR = path
    LOG_FORMAT = '%(asctime)s %(levelname)s [%(filename)s:%(lineno)d]: %(message)s'

    # 日志配置字典
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_true': {
                '()': RequireDebugTrue,
            }
        },
        'formatters': {
            'standard': {
                'format': LOG_FORMAT,
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG' if debug_flag else 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'filters': ['require_debug_true', ]
            },
            'file_handler': {
                'level': 'INFO',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'formatter': 'standard',
                'filename': os.path.join(BASE_DIR, 'app.log'),
                'when': 'midnight',  # 每天轮换
                'backupCount': 30,  # 保存30天的日志
                # 'when': 'W0',  # 每周一轮换
                # 'backupCount': 4,  # 保留4周的日志
                'encoding': 'utf8',
            },
            'error_file_handler': {
                'level': 'ERROR',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'formatter': 'standard',
                'filename': os.path.join(BASE_DIR, 'error.log'),
                'when': 'midnight',
                'backupCount': 30,
                # 'when': 'W0',  # 每周一轮换
                # 'backupCount': 4,  # 保留4周的日志
                'encoding': 'utf8',
            },

            # 训练日记记录
            'training_file_handler': {
                'level': 'INFO',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'formatter': 'standard',
                'filename': os.path.join(path, 'training_log.log'),
                'when': 'midnight',
                'backupCount': 30,
                # 'when': 'W0',  # 每周一轮换
                # 'backupCount': 4,  # 保留4周的日志
                'encoding': 'utf8',
            },
        },

        'loggers': {
            'app_logger': {
                'handlers': ['console', 'file_handler', 'error_file_handler'],
                # 'handlers': ['file_handler', 'error_file_handler'],
                'level': 'INFO',
                'propagate': False,
            },

            'training_logger': {
                'handlers': ['training_file_handler'],
                'level': 'INFO',
                'propagate': False,
            },
        }
    }

    return logging_config
