lines = open('input.txt').read().strip().split('\n')
xs = [list(map(int, line.split())) for line in lines]

def ok(x):
    return ((x==sorted(x) or x==sorted(x,reverse=True))
        and all(abs(x[i]-x[i+1]) <= 3 and x[i] != x[i+1] for i in range(len(x)-1)))

print(sum(1 for x in xs if ok(x)))

def aok(x):
    return any((ok(x[:j] + x[j+1:]) for j in range(len(x))))

print(sum(1 for x in xs if aok(x)))
