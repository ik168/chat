import flask
from flask import request
import redis
import time
import json

# 连接上本机的 redis 服务器
# 所以要先打开 redis 服务器
red = redis.Redis(host='localhost', port=6379, db=0)
print('redis', red)

app = flask.Flask(__name__)
app.secret_key = 'key'

# 发布聊天广播的 redis 频道
chat_channel = 'chat'


def stream():
    '''
    监听 redis 广播并 sse 到客户端
    '''
    # 对每一个用户 创建一个[发布订阅]对象
    pubsub = red.pubsub()
    # 订阅广播频道
    pubsub.subscribe(chat_channel)
    # 监听订阅的广播
    for message in pubsub.listen():
        print(message)
        if message['type'] == 'message':
            data = message['data'].decode('utf-8')
            # 用 sse 返回给前端
            yield 'data: {}\n\n'.format(data)


@app.route('/chat/subscribe')
def subscribe():
    return flask.Response(stream(), mimetype="text/event-stream")


@app.route('/chat/')
def index_view():
    return flask.render_template('index.html')


def current_time():
    return int(time.time())


@app.route('/chat/chat/add', methods=['POST'])
def chat_add():
    msg = request.get_json()
    name = msg.get('name', '')
    if name == '':
        name = '<匿名>'
    content = msg.get('content', '')
    channel = msg.get('channel', '')
    r = {
        'name': name,
        'content': content,
        'channel': channel,
        'created_time': current_time(),
    }
    message = json.dumps(r, ensure_ascii=False)
    print('debug', message)
    # 用 redis 发布消息
    red.publish(chat_channel, message)
    return 'OK'


if __name__ == '__main__':
    config = dict(
        debug=True,
    )
    app.run(**config)
