# redis消息队列设计

## 基础

基于aioredis，使用redis的发布订阅模式，实现消息队列



## 设计

1. 所有服务器只订阅自己serverid的频道，比如：001号网关服的serverid为gate001，订阅的频道就是gate001，在redis中为channel:gate001

2. observer观察者服务器，维护了一个publish的列表，比如gate的publish列表为：

   ```json
   {
     'gate': [
       'hall',
       'game',
       'observer'
     ],
     'hall': [
       'gate',
       'observer'
     ],
     'game': [
       'gate',
       'observer'
     ]
   }
   ```
   
3. 所有服务器启动后会向观察者服务器发送心跳并注册，每次心跳观察者服务器会将最新的publish列表发送给注册服务

4. 上面的设计已经实现，但是过于复杂，现在简单的设计方式为，gate在connection中记录了，玩家连接的是哪个服务器频道，hall001或者game001等，接到玩家的消息后，直接pub到对应的频道中。

## 技术实现

使用aioredis异步redis客户端提供的pub/sub来实现

### 订阅

订阅类的实现：

```python
    @run_in_loop
    async def subscribe(self, channel_name):
        self._channel_name = channel_name
        rslog.info('subscribe channel: {}'.format(channel_name))
        try:
            channels = await self._db_connect.db_connection.subscribe(self.channel_name)
            self._channel = channels[0]
        except Exception as e:
            rslog.error("subscribe exception channel: {}, error info: {}".format(self._channel_name, e.__str__()))
            raise e
        await self.listen_channel()

    async def listen_channel(self):
        while True:
            await self._channel.wait_message()
            try:
                msg_str = await self._channel.get(encoding='utf-8')
            except aioredis.errors.ChannelClosedError:
                rslog.error("Redis channel was closed. Stopped listening. channel name: {}".format(self._channel_name))
                return
            if msg_str:
                # 解析消息并调用接口处理消息
                rslog.info("Message in {}: {}".format(self._channel.name, msg_str))
                msg = MsgPack()
                msg.unpack(msg_str)

                # 派发消息
                fun_method = partial(Handler.cmd_dispatch, msg)
                IOLoop.current().add_callback(fun_method)
```

注意看最后的派发消息，将派发消息的函数放进ioloop中执行，这是因为，消息队列的订阅函数本身就是个协程，如果派发函数中阻塞则整个协程也会阻塞，知道当前的阻塞处理完后，才会再去频道中获取消息，这样就变成了串行，初始化订阅频道的代码如下：

```python
# 设置订阅频道
DaoBase.redis_conn_pool['subscribe'].subscribe(server_type + server_id)
```

这个函数使用了run_in_loop装饰器，这个装饰器的作用是将修饰的函数放在IOLoop中执行。

消息队列的订阅函数本身就是协程，和tornado的tcpserver处理消息还是不一样的，tcpserver处理消息不是在协程内部，应该是一个消息一个协程，所以消息处理如果阻塞了，不会阻塞所有消息处理流程，但是消息队列的订阅会阻塞它去频道中获取消息，因为它是个协程。

### 发布

发布的实现：发布消息前会查询频道是否在可发布列表中，现在测试用暂时注释掉了

```python
   @property
    def channel(self) -> list:
        return self._channel

    def is_channel_exists(self, channel_name: str) -> bool:
        return channel_name in self._channel

    def add_channel(self, channel_name: str) -> NoReturn:
        if not self.is_channel_exists(channel_name):
            self._channel.append(channel_name)

    def remove_channel(self, channel_name: str) -> NoReturn:
        if self.is_channel_exists(channel_name):
            self._channel.remove(channel_name)

    async def pub_msg(self, channel_name, msg) -> Union[Awaitable or NoReturn]:
        if not self.is_channel_exists(channel_name):
            raise MsgChannelNotExistsException(channel_name)
        await self._db_connect.db_connection.publish(channel_name, msg)

    async def pub_msg_json(self, channel_name, msg) -> Union[Awaitable or NoReturn]:
        if not self.is_channel_exists(channel_name):
            raise MsgChannelNotExistsException(channel_name)
        await self._db_connect.db_connection.publish_json(channel_name, msg)

    async def pub_msg_all(self, msg) -> NoReturn:
        if not self._channel:
            return

        for channel in self._channel:
            await self.pub_msg(channel, msg)
```

