import random
def sort(ori: list[int | float]) -> list[int | float]:
    ele = [x for x in ori]
    random.shuffle(ele)

    original = ele[:]
    better = ele[:]
    for _ in range(1000):
        cal_better = 0
        cal_original = 0
        for i in range(len(better)):
            cal_better += i * (better[i] - 6) 
        random.shuffle(original)
        for i in range(len(original)):
            cal_original += i * (original[i] - 6)
        if cal_original > cal_better:
            better = original[:]
        else:
            pass
    return better

if __name__ == '__main__':
    print(sort([7, 10, 11, 12, 13, 14, 17, 18, 20, 21, 22, 24, 27, 28, 32, 34]))
    
    
        
    