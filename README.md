UserState
========
用户数据表格包括

保护结束时间， 攻击结束时间， 在线时间

客户端负责设定这些时间

保护结束时间
----
受到多次攻击 一定概率进入保护模式 设定保护时间 startShield

用户攻击其它人 保护时间清零 clearShield

保护时间到

攻击结束时间
----
findAMatch 寻找攻击对象 对象的attackTime 自动设定10s后失效

updateAttackTime 在攻击阶段 每10s种 激活一次 

攻击时间到自动 结束

在线时间
----
玩家登录时 设定登录失效时间+10s

updateOnlineTime 游戏过程中定时 需要更新在线状态

搜索例子
----
1. findAMatch uid score scoreOff 搜索在[score-scoreOff, score+scoreOff] 区间段的用户
2. 客户端记录每次搜索的用户的积分 下次搜索尽量避开已经包含之前用户的积分的 区间段

流程
----
1. findAMatch 搜索一个对手
2. 客户端不断更新对手的attackTime updateAttackTime
3. 客户端攻击该对手
4. 如果攻击胜利 一定概率设定对手的 shieldTime 
5. 用户登录获取attackTime 如果超时则设定 onlineTime 
6. 用户在线中 一定时间更新一次onlineTime


