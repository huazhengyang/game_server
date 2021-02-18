# gate server note

1. 网关处理客户端心跳消息，每隔几次心跳透传给sceneserver
2. 网关保存客户端连接，还包括玩家连接的session，方便发布到消息队列和将场景服务返回的消息转发给客户端