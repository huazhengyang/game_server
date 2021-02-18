# Common components
1. 全局业务基础库，库中的所有代码仅供其他服务使用，最好不要在这里实例化任何对象
2. 所有规则全部在配置文件中，库中只提供出口，增加字段需要自己实现，但是要注意对其他代码的影响，影响较大的要上浮到具体业务中实现

# 包说明
1. entity.database 各个数据库操作，user room table等
2. entity.game  游戏插件基础模块
3. entity.roomrule  房间规则
4. entity.pokerrule 扑克玩法规则
5. entity.scene  场景实例，room table match

6.utils.config 基础库配置管理和解析