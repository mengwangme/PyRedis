# PyRedis

* Basic implementation of Redis in Python.
* Works using gevent for non blocking IO
* Handles RESP compliant commands

#### ENV

python==3.6.5
gevent==1.3.5
greenlet==0.4.13

#### structure

```
pyredis
├── Dockerfile
├── README.md
├── pyredis
├── requirements.txt
├── setup.py
├── src
│   ├── __init__.py
│   ├── command_handler.py
│   ├── command_parser.py
│   ├── daemon.py
│   ├── memory.py
│   ├── pyredis.py
│   └── server.py
└── tests
    ├── __init__.py
    ├── test_command_handler.py
    └── test_command_parser.py
```

#### 实验步骤

#### Step 0

下载依赖包

```
$ Install dependencies with pip install -r requirements.txt
```
    
#### Step 1

测试

```
$ python -m unittest discover -s tests/ -p 'test_*.py'
```

#### Step 2

**注意**：去除了src/文件夹中py文件的import src. 部分，才运行成功

You can now control daemon with:

```
$ python src/pyredis.py start

$ python src/pyredis.py stop

$ python src/pyredis.py restart
```


#### Step 3

作为PIP包下载

Install as a PIP package

1. `python install wheel`
2. First build a wheel ```python setup.py bdist_wheel```
3. Install the wheel ```python setup.py install```...now ```pyredis start/stop/restart``` is available on your path

To do a daemon install (after you have installed the pip package)

+ 1.Copy the init.d script to /etc/init.d
+ 2.Run ```sudo service start pyredis```

#### Step 4

建立/运行docker容器

Build/run as a docker container

+ 1.```$ docker build -t redis ```
+ 2.```$ docker run -dit --name redis -p 6379:6379 redis```

For any install or run method you should be able to run redis-cli on the host machine and it will connect to 127.0.0.1:6379 where you can issue commands
