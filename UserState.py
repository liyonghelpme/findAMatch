#coding:utf8
import time
import random

beginTime=(2013,1,1,0,0,0,0,0,0)
def getTime():
    curTime = int(time.mktime(time.localtime())-time.mktime(beginTime))
    return curTime

#寻找一个攻击对象
#保护结束时间  自动超时 服务器业余逻辑设置
#攻击结束时间  需要攻击方释放 设置攻击开始时间 = 0 或者 自动超时
#在线结束时间  需要客户端心跳定时更新时间

def startShield(myCon, uid, passTime):
    curTime = getTime()+passTime
    sql = 'update UserState set shieldTime = %d where uid = %d' % (curTime, uid)
    myCon.query(sql)
    myCon.commit()

def clearShield(myCon, uid):
    sql = 'update UserState set shieldTime = 0 where uid = %d' % (uid)
    myCon.query(sql)
    myCon.commit()

def updateOnlineTime(myCon, uid, passTime):
    curTime = getTime()+passTime
    sql = 'update UserState set onlineTime = %d where uid = %d' % (curTime, uid)
    myCon.query(sql)
    myCon.commit()


#持续攻击该用户
def updateAttackTime(myCon, uid, passTime):
    curTime = getTime()+passTime
    sql = 'update UserState set attackTime = %d where uid = %d' % (curTime, uid)
    myCon.query(sql)
    myCon.commit()
    


#返回用户之后自动startAttack
#获得区间 最小 最大 用户id
#积分值 -10 +10 这个积分变化的区间由业务逻辑决定
#没有处于保护状态 没有被攻击 没有在线
#攻击者 需要定时更新对方被攻击时间

#避免uid 中有空隙 这样可能找不到新的挑战对象
#返回用户id
#如何避免重复的用户？

#客户端控制scoreOff 来增加随机性
#客户端调整score 来控制搜索的基础范围

#客户端主要 逻辑是如何设定 score 和 scoreOff
#不同区段积分避免重复
def findAMatch(myCon, uid, score, scoreOff):
    curTime = getTime()
    print "==================", uid, score, scoreOff
    while scoreOff < 20000: # 积分最大相差范围
        minScore = score-scoreOff
        maxScore = score+scoreOff

        #得到搜索的范围uid 
        sql = 'select max(uid), min(uid) from UserState where score >= %d and score <= %d ' % (minScore, maxScore)
        myCon.query(sql)
        res = myCon.store_result().fetch_row(0, 0)
        print "findAMatch NUM", uid, score, len(res), scoreOff
        #直接得到返回用户
        if len(res) > 0:
            maxUid = res[0][0]
            minUid = res[0][1]
            if maxUid != None and minUid != None:
                cut = random.randint(minUid, maxUid)
                sql = 'select uid from UserState where uid >= %d and uid != %d and shieldTime <= %d and attackTime <= %d and onlineTime <= %d  and score >= %d and score <= %d limit 1' % (cut, uid, curTime, curTime, curTime, minScore, maxScore)
                myCon.query(sql)
                
                user = myCon.store_result().fetch_row(0, 0)
                print "User ", len(user)
                if len(user) > 0:
                    otherId = user[0][0]
                    sql = 'update UserState set attackTime = %d where uid = %d' % (curTime+10, otherId)#需要客户端10s内发送一次心跳信号更新被攻击时间
                    myCon.query(sql)
                    return otherId
        scoreOff *= 2 
    return -1
            



if __name__ == '__main__':
    def Test():
        import MySQLdb
        myCon = MySQLdb.connect(host='localhost', passwd='badperson3', db='UserMatch', user='root', charset='utf8')
        uid = findAMatch(myCon, 0, random.randint(100, 200), 10)
        print "---find", uid
        updateAttackTime(myCon, uid , 10) #每次延迟攻击结束时间10s钟
        #time.sleep(1)
        updateAttackTime(myCon, uid, 10) #每次延迟攻击结束时间10s钟


        startShield(myCon, uid, 24*3600) #保护一天
        
        uid2 = findAMatch(myCon, 0, random.randint(300, 400), 10)
        print '---find2 ', uid2
        uid2 = findAMatch(myCon, 0, random.randint(500, 600), 10)
        print '---find3 ', uid2
        
        clearShield(myCon, uid) #攻击别人清理保护时间
        uid3 = findAMatch(myCon, uid, random.randint(700, 800), 10)
        print '---find4', uid3
        updateAttackTime(myCon, uid, 20) #根据网络速度决定更新时间

        updateOnlineTime(myCon, uid, 10)

        myCon.close()


    Test()

