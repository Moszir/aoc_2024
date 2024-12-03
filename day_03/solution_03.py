import re


lines = open('input.txt').read().strip()

def mul(s):
    r = re.match(r'mul\((\d{1,3}),(\d{1,3})\)', s)
    return int(r.group(1)) * int(r.group(2)) if r is not None else 0

print(sum(mul(lines[i:]) for i in range(len(lines))))

x = 0
on = True
for i in range(len(lines)):
    l = lines[i:]
    if l.startswith('do()'):
        on = True
    elif l.startswith("don't()"):
        on = False
    if on:
        x += mul(l)
print(x)
