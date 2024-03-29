import random
import os
import PK
import predict
from rich.console import Console
from rich.table import Table

console = Console()
participants = []
rankings = []

# 首轮对战情况
teams = [['Cloud9', 'ECSTATIC'], ['Eternal Fire', 'TheMongolz'], ['ENCE', 'Imperial'], ['Apeks', 'paiN'], 
    ['HEROIC', 'Lynn Vision'], ['9 Pandas', 'AMKAL'], ['SAW', 'KOI'], ['FURIA', 'Legacy']]

# 导入战队排名字典
team_dict = PK.team_dict

# 战队胜负分系统
score = {}
for key in team_dict.keys():
    score[key] = 0

# 战队列表和排名列表分开
for key, value in team_dict.items():
    participants.append(key)
    rankings.append(value)

# 根据胜负分分组函数
def decide_by(a: list[str]) -> list[list[str]]:
    groups = []
    ranked = []
    
    # 将所有队伍按照胜负分进行排序
    rank = sorted(score.items(), key=lambda x: x[1], reverse=False)
    for x in rank:
        ranked.append(x[0])
    
    # 将被分组的各支队伍与排好序的列表进行比较，分高的最先被挑出来，完成排序
    groups_temp = [x for x in ranked if x in a]
    ranked.clear()
    
    # 将高分队伍和低分队伍成对加入列表
    for i in range(int(len(groups_temp)/2)):
        ranked.append(groups_temp[i])
        ranked.append(groups_temp[len(groups_temp)-i-1])
    for i in range(0, len(ranked), 2):
        
    #每两个进行对战
        groups.append([ranked[i], ranked[i+1]])
    return groups

# 随机分组函数
def decide(a: list[str]) -> list[list[str]]:
    groups = []
    random.shuffle(a)
    
    # 随机两个队伍对战
    for i in range(0, len(a), 2):
        groups.append([a[i], a[i+1]])
    return groups


print('参赛队伍：')
team_list = []
for i in range(16):
    team_list.append([i+1, participants[i], rankings[i]])

team_table = Table()

team_table.add_column('序号')
team_table.add_column('战队')
team_table.add_column('世界排名')
for x in range(len(participants)):
    team_table.add_row(str(x+1), participants[x], '#' + str(rankings[x]))

console.print(team_table)

print('\n第一轮对阵情况：')
for x in teams:
    print('{0}.{1} - {2}.{3}'.format(participants.index(x[0])+1, x[0], participants.index(x[1])+1, x[1]))
print('')

# 开始竞猜
pre = predict.predict(participants)
pre30 = pre[:2]
pre3132 = pre[2:8]
pre03 = pre[8:]
pre_sum = [pre30, pre3132, pre03]


# 开始比赛
pk = PK.PK(teams)

# 第一轮

# 16队产生8支1-0和8支0-1
step10, step01 = pk.round(teams)

# 胜者胜负分加一
for x in step10:
    score[x] += 1
#负者胜负分减一
for x in step01:
    score[x] -= 1


# 第二轮

# 随机分组
step10 = decide(step10)
step01 = decide(step01)

# 产生4支2-0，8支11-0，4支0-2
step20, step11_1 = pk.round(step10)
step11_2, step02 = pk.round(step01)
step11 = step11_1 + step11_2

# 胜负分计算
for x in step20 + step11_2:
    score[x] += 1
for x in step11_1 + step02:
    score[x] -= 1

# 第三轮

# 根据胜负分进行分组
step20 = decide_by(step20)
step02 = decide_by(step02)
step11 = decide_by(step11)

# 产生2支3-0晋级，6支2-1，6支1-2，2支0-3淘汰
a30, step21_1 = pk.round(step20)
step21_2, step12_1 = pk.round(step11)
step12_2, a03 = pk.round(step02)
step21 = step21_1 + step21_2
step12 = step12_1 + step12_2

for x in step21_2 + step12_2: 
    score[x] += 1
for x in step12_1 + step21_1:
    score[x] -= 1

# 第四轮，产生3支3-1晋级、6支2-2、3支1-3淘汰
step21 = decide_by(step21)
step12 = decide_by(step12)

a31, step22_1 = pk.round(step21)
step22_2, a13 = pk.round(step12)
step22 = step22_1 + step22_2

for x in step22_2:
    score[x] += 1
for x in step22_1:
    score[x] -= 1
    
# 第五轮，产生3支3-2晋级、3支2-3淘汰
step22 = decide_by(step22)
a32, a23 = pk.round(step22)


a3132 = a31 + a32
a1323 = a13 + a23

a_sum = [a30, a3132, a03]

# 统计预测正确的个数，并将预测正确的项字体颜色改为绿色
correct30, pre30 = predict.compare_lists(pre30, a30)
correct3132, pre3132 = predict.compare_lists(pre3132, a3132)
correct03, pre03 = predict.compare_lists(pre03, a03)
summary = correct30 + correct3132 + correct03

# 输出竞猜结果
a30 = pk.fill(a30)
a03 = pk.fill(a03)
pre30 = pk.fill(pre30)
pre03 = pk.fill(pre03)
print('比赛结果：')
table1 = Table()
table2 = Table()
table1.add_column('3:0晋级')
table1.add_column('3:1/3:2晋级')
table1.add_column('1:3/2:3淘汰')
table1.add_column('0:3淘汰')
for i in range(6):
    table1.add_row(a30[i], a3132[i], a1323[i], a03[i])

console.print(table1)

table2.add_column('3:0晋级')
table2.add_column('3:1/3:2晋级')
table2.add_column('0:3淘汰')
for i in range(6):
    table2.add_row(pre30[i], pre3132[i], pre03[i])
print('你的预测：')
console.print(table2)

correct = '[red1]' + str(summary) if summary < 5 else '[green1]' + str(summary)
console.print(f'预测正确的个数是：{correct}')
if summary < 5:
    console.print('[red1]你币无！')
else:
    console.print('[green1]你币有！')

os.system('pause')