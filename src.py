# Read input from file input
def readfile(filename):
    with open(filename, "r") as file:
        alpha = file.readline().strip()
        number = int(file.readline().strip())
        kb = []
        for i in range(number):
            kb.append(file.readline().strip())

    return alpha, kb

# Write buffer to file output
def writefile(filename, buffer):
    with open(filename, "a") as file:
        file.write(str(len(buffer))+"\n")
        for i in list(buffer):
            formatted_content = ' OR '.join(
                [elem if elem.startswith('-') else f"{elem}" for elem in i])
            file.writelines(str(formatted_content)+'\n')

# Negative of alpha for adding to KB
def negativeAlpha(alpha):
    new = []
    if 'OR' in alpha:
        clauses = alpha.split(' OR ')
        for clause in clauses:
            if '-' not in clause:
                new.append([(f"-{clause}")])
            else:
                new.append([clause.replace('-', '')])
    else:
        if '-' not in alpha:
            new.append([(f"-{alpha}")])
        else:
            new.append([alpha.replace('-', '')])
    return new

# Checking the result that is useless.
# Ex: (-A OR A OR C) -> (C)
def isUseless(src):
    for literal in src:
        if '-' in literal and literal.replace("-", "") in src:
            src.remove(literal)
            src.remove(literal.replace("-", ""))
        else:
            if f'-{literal}' in src:
                src.remove(literal)
                src.remove(f'-{literal}')

# checks if a clause is a sample of another clause and removes it if it is
def isSample(src, new, buffer):
    i = 0
    while i < len(new):
        if new[i] in src:
            new.remove(new[i])
        else:
            addClause(src, buffer, new[i])
            i = i+1

# add a clause to the buffer
def addClause(src, buffer, clause):
    buffer.append(clause)
    src.append(clause)
def resolve(ci, cj):
    resolvents = []
    for literal in ci:
        if '-' in literal:
            if literal.replace("-", "") in cj:
                resolvent = sorted(set(ci) | set(cj))
                resolvent.remove(literal)
                resolvent.remove(literal.replace("-", ""))
                isUseless(resolvent)
                resolvents.append((resolvent))
        else:
            if f'-{literal}' in cj:
                resolvent = sorted(set(ci) | set(cj))
                resolvent.remove(literal)
                resolvent.remove(f'-{literal}')
                isUseless(resolvent)
                resolvents.append((resolvent))

    return resolvents

# function that solve problem Entailing
def PL_resolution(kb, alpha, fileNumber):
    clauses = ([(clause.split(' OR ')) for clause in kb])
    clauses.extend(negativeAlpha(alpha))
    buffer = list()
    while True:
        new_clauses = []
        pairs = [(clauses[i], clauses[j])
                 for i in range(len(clauses)) for j in range(i + 1, len(clauses))]
        for (ci, cj) in pairs:
            resolvent = resolve(ci, cj)
            for i in resolvent:
                if not i:
                    return True, buffer
            if len(resolvent) != 0:
                new_clauses.extend(resolvent)
        isSample(clauses, new_clauses, buffer)
        if len(new_clauses) == 0:
            return False, buffer

        writefile(f"output{fileNumber}.txt", buffer)
        buffer.clear()


def main():
    for i in range(1, 6):
        alpha, kb = readfile(f"input{i}.txt")
        with open(f"output{i}.txt", "w") as file:
            file.write("")
            file.close()
        result, buffer = PL_resolution(kb, alpha, i)
        with open(f"output{i}.txt", "a") as file:
            if result:
                print("YES")
                file.write("{}\nYES")

            else:
                print("NO")
                file.write(f"{len(buffer)}\nNO")

    return 0


if __name__ == "__main__":
    main()
