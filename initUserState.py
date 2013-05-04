#coding:utf8
import MySQLdb
import random 
myCon = MySQLdb.connect(host='localhost', passwd='badperson3', db='UserMatch', user='root', charset='utf8')

for i in xrange(0, 100):
    sql = 'insert into UserState (uid, shieldTime, attackTime, onlineTime, score) values(%d, %d, %d, %d, %d)' % (i, 0, 0, 0, random.randint(0, 1000))
    myCon.query(sql)

#测试保护状态的用户数据 
#攻击状态用户数据
#在线状态用户数据
myCon.commit()
myCon.close()
