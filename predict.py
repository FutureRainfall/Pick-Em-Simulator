def compare_lists(a: list, b: list) -> tuple[int, list]:
    '''
    a、b两个列表的元素，若a中元素在b中，则将这个a中元素的字体变绿，同时计一次预测正确，否则维持原样
    '''
    correct = 0
    result = []
    for item in a:
        if item in b:
            result.append('[green1]' + item)
            correct += 1
        else:
            result.append(item)
    return correct, result

def check_input(numbers: set[int], used_numbers: set[int], count: int, msg: str) -> list[int]:
    '''
    numbers - 要输入的数字
    used_numbers - 已经输入过的数字
    count - 输入个数
    msg - 提示信息
    '''
    
    # 输出提示信息
    inputs = input(msg)

    # 用户输入数字，用空格分隔
    nums = [int(x) for x in inputs.split()]

    # 输入次数错误，返回None
    if len(nums) != count:
        return None

    # 输入数字已在used_numbers中（重复输入），返回None
    if len(set(nums) & used_numbers) > 0:
        return None

    # 输入数字不在numbers中（超出限制），返回None
    if not all(x in numbers for x in nums):
        return None

    # 输入无误，返回输入的数字列表
    return nums

numbers = set(range(1, 17))
used_numbers = set()

def predict(participants: list[str]) -> list[str]:
    '''
    预测函数，participants为所有参赛队伍
    '''
    
    p = []
    pre = []
    
    # 三次竞猜，分别是2个3-0组，6个3-1和3-2组，2个0-3组
    for i in range(3):
        while True:
            if i == 0:
                count = 2
                msg = f'请预测 {count} 个3-0晋级队伍的序号，以空格相隔：'
            elif i == 1:
                count = 6
                msg = f'请预测 {count} 个3-1或3-2晋级队伍的序号，且不能与之前重复：'
            else:
                count = 2
                msg = f'请预测 {count} 个0-3淘汰队伍的序号，且不能与之前重复：'

            nums = check_input(numbers, used_numbers, count, msg)
            
            if nums is None:
                print('输入错误，请重新输入')
            else:
                # 将预测的队伍加入pre列表
                p = [participants[x-1] for x in nums]
                for o in p:
                    pre.append(o)
                break
        
        # 输出预测的队伍
        print(' '.join(p))
        
        # 将输入的数字添加到已输入数字集合中
        used_numbers.update(nums)
    return pre
