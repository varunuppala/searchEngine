def sum1(n):
    s = 0
    for i in str(n):
        s+=int(i)
    return s



def sum(n):
    c = 0
    s = 0
    while n > 0:
        curr = n %10
        if c%2 == 0:
            s = s + curr
        else:
            s += sum1(curr*2)
        c +=1
        n = n//10
    return s

print(sum(int(input("enter number"))))
