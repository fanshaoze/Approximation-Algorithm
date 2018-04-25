import random
from pulp import *


def generate_Fset(xgroup):
    xset = xgroup.copy()
    xgroup = xgroup.copy()
    result = [set(random.sample(xset, 20))]
    set0 = result[0]
    set1 = xset.difference(set0)
    while len(xset) >= 20:
        subset = set()
        n = random.randint(1, 20)
        x = random.randint(1, n)
        subset = subset.union(random.sample(set1, x))
        subset = subset.union(random.sample(set0, n - x))
        result.append(subset)
        set0 = set0.union(subset)
        xset = xset.difference(set0)
    result.append(xset)
    for i in range(len(xgroup) - len(result)):
        result.append(set(random.sample(xgroup, random.randint(1, 100))))
    print result
    print len(result)
    return result


def greedy(x, f):
    u = x
    c = []
    while len(u) > 0:
        max_cover_size = 0
        max_index = 0
        for index, s in enumerate(f):
            # union max
            cover_size = len(s.intersection(u))
            if cover_size > max_cover_size:
                max_cover_size = cover_size
                max_index = index
        c.append(f[max_index])
        u = u.difference(f[max_index])
    print(c)
    print(len(c))


def linear_set_cover(x, s):
    element = []  # sum of xi
    prob = LpProblem("test1", LpMinimize)
    for i in range(len(s)):
        element.append(LpVariable("x" + str(i), 0, 1))
        # prob += LpVariable("x"+str(i), 0, 1)
    vars = element[0]
    for i in range(0, len(s)):
        vars += element[i]
    prob += vars
    # prob += sum(element[i] for i in range(0,len(s)))
    for i in x:
        tempset = []  # the si selected
        for j in range(0, len(s)):
            if i in s[j]:
                tempset.append(j)
        sumvar = element[tempset[0]]
        for num in range(1, len(tempset)):
            sumvar += element[tempset[num]]
        prob += sumvar >= 1
        # prob += sum(element[tempset[num]] for num in range(0,len(tempset))) >= 1
    prob.writeLP("test1.lp")
    prob.solve()
    # Print the value of the variables at the optimum
    #for v in prob.variables():
    #    print v.name, "=", v.varValue
    conresult = prob.variables()
    result = []
    f = 0
    for i in x:
        freqsum = 0
        for j in range(0, len(s)):
            if i in s[j]:
                freqsum += 1;
        if freqsum > f:
            f = freqsum
    freq = float(1.0 / f)
    for i in range(len(conresult)):
        if conresult[i].varValue > freq:
            result.append(s[i])
    print result
    print len(result)
    return result
    # Print the value of the objective
    # print "objective=", value(prob.objective)


x_group = set()
for i in range(1000):
    x_group.add(i)
print x_group
Fset = generate_Fset(x_group)
greedy(x_group, Fset)
linear_set_cover(x_group, Fset)
