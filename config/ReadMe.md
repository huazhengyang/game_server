# 配置文件夹  
配置文件命名说明，以game id命名文件,前100个gameid为预留，从101开始
101 德州SNR  
102 百家乐

4000 sdk  
4001 hall  
4002 gate  
4003 center

RainStorm 框架配置

server_type  什么类型的服务器，scene(game), scene(hall)等
每个进程的服务都是单例的服务，但是center、manager只能启动一个，其他服务可以启动多个支持动态平行扩展


