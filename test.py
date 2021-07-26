def sort_numlist(nums:list):
    sorted_list = []
    for num in nums:
        def check(sorted_list=sorted_list, num=num):
            for x in sorted_list:
                last = len(sorted_list)-1
                if num <= x:
                    return (True, sorted_list.index(x))
                elif num >= sorted_list[last] and x == sorted_list[last]:
                    return (False, sorted_list.index(x))


        get_back = check() if len(sorted_list) != 0 else (0, 0)
        to_insert, idx = get_back[0], get_back[1]

        if len(sorted_list) == 0:
            sorted_list.append(num)

        elif to_insert:
            sorted_list.insert(idx, num)
        elif not to_insert:
            sorted_list.append(num)

    return sorted_list

def mode(nums:list):
    modes = []
    nums = sort_numlist(nums)

    for num in nums:
        count = 0
        for element in nums:
            if num == element:
                count += 1

                if len(modes) !=0:
                    for mode in modes:
                        m = [m[0] for m in modes]
                        if count >= mode[1]:
                            if num in m:
                                modes[m.index(num)][1] = count
                                for e in modes:
                                    if count > e[1]:
                                        modes.remove(e)
                            elif [num, count] in modes:
                                pass
                            else:
                                modes.append([num, count])
                else:
                    modes.append([num, count])

    return modes

def randlist():
    import random
    result = [] 
    for x in range(1000):
        result.append(random.randint(1, 1000))

    return result

def add(*nums):
    sum = 0
    for num in nums:
        sum+=num
    return sum
    
def sub(*nums):
    diff = 0
    for num in nums:
        diff-=num
    return diff

def mult(*nums):
    product = 1
    for num in nums:
        product*=num
    return product

def div(*nums):
    quo = 1
    for num in nums:
        quo/=num
    return quo

# Allowed Chars:
#   0, 1 ... 9, %, ^, *, x, (, ), ., +, -, /

def solve(expr:str):
    # Step 1: Change it into python understandable. (change '*' and 'x')

    expr = expr.replace('^', '**')
    expr = expr.replace('x', '*')

    print(eval(expr))
        
# print(sort_numlist([1, 3, 4, 2, 5]))
test_list = randlist()
print(sort_numlist(test_list))
print(mode(test_list))
