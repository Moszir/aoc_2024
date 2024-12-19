from functools import cache
ps, ds = (l.split(b) for l, b in zip([l for l in open("input.txt").read().strip().split('\n\n')], [', ', '\n']))
@cache
def ways(d):
    return sum(ways(d[len(p):]) for p in ps if d.startswith(p)) if d else 1
print(sum(1 for d in ds if ways(d) > 0), sum((ways(d) for d in ds)))
