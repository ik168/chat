# chat
安装需求

apt-get install redis-server

pip3 install redis python-redis gunicorn gevent

如果执行上述安装报错，尝试下面两项

apt-get install build-essential

apt-get install python3-dev

开启redis

redis-server&

使用 gunicorn 启动

gunicorn --worker-class=gevent -t 9999 redischat:app -b 0.0.0.0:3000

开启 debug 输出

gunicorn --log-level debug --worker-class=gevent -t 999 redis_chat:app

把 gunicorn 输出写入到 gunicorn.log 文件中

gunicorn --log-level debug --access-logfile gunicorn.log --worker-class=gevent -t 999 redis_chat:app

redis安全相关问题

nano /etc/redis/redis.conf

如果实际路径不一样，可以用以下指令查找

find / -name redis.conf

在conf找到 bind 127.0.0.1 这行，把前面的注释去掉，保存

开启redis的方式改为

redis-server /etc/redis/redis.conf &

supervisor安装

apt-get install supervisor

supervisor配置

cd /etc/supervisor/conf.d

nano chat.conf

输入以下内容
```
[program:chat]
comand=/usr/local/bin/gunicorn wsgi --worker-class=gevent -t 9999 --bind 0.0.0.0:8000 --pid /tmp/chat.pid
directory=/root/chat
autostart=true
```
保存退出
