# gunicorn.conf.py for FastAPI
import multiprocessing
from gevent import monkey

monkey.patch_all()
bind = '0.0.0.0:9000'  # 绑定监听ip和端口号
debug = False
# workers = multiprocessing.cpu_count() * 2 + 1 # 同时执行的进程数，推荐为当前CPU个数*2+1
workers = 4 # 同时执行的进程数，推荐为当前CPU个数*2+1
backlog = 2048  # 等待服务客户的数量，最大为2048，即最大挂起的连接数
worker_class = "uvicorn.workers.UvicornWorker"  # 支持异步的工作进程
max_requests = 1000  # 默认的最大客户端并发数量
daemon = True # 是否后台运行， 是否以守护进程方式运行
reload = False  # 当代码有修改时，自动重启workers。适用于开发环境。
pidfile = 'gunicorn.pid'  # 设置pid文件的文件名
loglevel = 'info'  # debug error warning error critical
accesslog = 'logs/gunicorn.log'  # 设置访问日志
errorlog = 'logs/gunicorn.err.log'  # 设置问题记录日志
