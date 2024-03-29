import random
import Sort_As as s

# 战队排名列表
team_dict = {'Cloud9': 9, 'ENCE': 10, 'HEROIC': 11, 'Eternal Fire': 13, 'Apeks': 14, 'FURIA': 16, 
        'SAW': 17, 'TheMongolz': 20, '9 Pandas': 21, 'Imperial': 26, 'KOI': 27, 'ECSTATIC': 28, 
        'Legacy': 30, 'paiN': 31, 'AMKAL': 32, 'Lynn Vision': 40}


class PK():
    def __init__(self, t: list[list[str]]) -> None:
        self.Team = t

    # 比赛
    def round(self, team: list[list[str]]) -> tuple[list[str], list[str]]:
        
        win_group = []
        loss_group = []
        team_sort = []
        rank = []
        
        # 排名列表
        for value in team_dict.values():
            rank.append(value)
        
        # 将战队根据排名高低（近似看作实力）进行概率排序
        rank_sort = s.sort(rank)
        
        for x in rank_sort:
            for key, value in team_dict.items():
                if value == x:
                    team_sort.append(key)
        
        # 对阵双方排名靠前的一方更有可能获胜
        for x in team:
            if team_sort.index(x[0]) < team_sort.index(x[1]):
                winner = x[0]
                loser = x[1]
            else:
                winner = x[1]
                loser = x[0]
            
            win_group.append(winner)
            loss_group.append(loser)
        
        random.shuffle(win_group)
        random.shuffle(loss_group)
            
        return win_group, loss_group

    # 输出为表格时行的长度对齐函数
    def fill(self, array: list[str]) -> list[str]:
        a = array
        length = len(array)
        for _ in range(6-length):
            a.append('')
        return a

if __name__ == '__main__':
    teams = [['Cloud9', 'ECSTATIC'], ['Eternal Fire', 'TheMongolz'], ['ENCE', 'Imperial'], 
        ['Apeks', 'paiN'], ['HEROIC', 'Lynn Vision'], ['9 Pandas', 'AMKAL'], ['SAW', 'KOI'], 
        ['FURIA', 'Legacy']]
    pk = PK(teams)
    win, lose = pk.round(teams)
    print(win, lose)