import logging
import logging.config
import os

# 判断是否为调试模式
debug_flag = True


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
    LOG_FORMAT = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s'

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
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'filters': ['require_debug_true', ]
            },
            'info_file_handler': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'standard',
                'filename': os.path.join(BASE_DIR, 'info.log'),
                'maxBytes': 1024 * 1024 * 5,
                'backupCount': 5,
                'encoding': 'utf8',
            },
            'warning_file_handler': {
                'level': 'WARNING',
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'standard',
                'filename': os.path.join(BASE_DIR, 'warning.log'),
                'maxBytes': 1024 * 1024 * 5,
                'backupCount': 5,
                'encoding': 'utf8',
            },
            'error_file_handler': {
                'level': 'ERROR',
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'standard',
                'filename': os.path.join(BASE_DIR, 'error.log'),
                'maxBytes': 1024 * 1024 * 5,
                'backupCount': 5,
                'encoding': 'utf8',
            },
        },
        'loggers': {
            '': {
                'handlers': ['console', 'info_file_handler', 'warning_file_handler', 'error_file_handler'],
                'level': 'DEBUG',
                'propagate': True,
            },
        }
    }

    return logging_config
