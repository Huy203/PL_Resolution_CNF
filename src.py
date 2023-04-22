def readfile(filename):
    with open(filename, "r") as file:
        alpha = file.readline().strip()
        number = int(file.readline().strip())
        kb = []
        for i in range(number):
            kb.append(file.readline().strip())

    file.close()
    return alpha, kb

def writefile(filename, buffer, number):
    
    with open(filename,"a") as file:
        file.write(str(number)+"\n")
        for i in list(buffer):
            formatted_content = ' OR '.join(
                [elem if elem.startswith('-') else f"{elem}" for elem in i])
            file.writelines(str(formatted_content)+'\n')
         

def resolve(ci, cj):
    resolvents = []

    for literal in ci:
        if '-' in literal:
            if literal.replace("-", "") in cj:
                resolvent = sorted(set(ci) | set(cj))
                resolvent.remove(literal)
                resolvent.remove(literal.replace("-", ""))
                resolvents.append(frozenset(resolvent))
        else:
            if f'-{literal}' in cj:
                resolvent = sorted(set(ci) | set(cj))
                resolvent.remove(literal)
                resolvent.remove(f'-{literal}')
                resolvents.append(frozenset(resolvent))
    return resolvents


def PL_resolution(kb, alpha, file_num):
    KB = kb + [('-'+alpha)]
    clauses = [frozenset(clause.split(' OR ')) for clause in KB]
    result = False
    while True:
        new_clauses = set()
        pairs = [(clauses[i], clauses[j])
                 for i in range(len(clauses)) for j in range(i + 1, len(clauses))]
        for (ci, cj) in pairs:
            resolvent = resolve(ci, cj)
            if not resolvent:
                result = True
                break
                #return True
            new_clauses=new_clauses.union(set(resolvent))
        if new_clauses.issubset(set(clauses)):
            
            return False
        number = 0
        buffer = []
        for clause in new_clauses:
            if clause not in clauses:
                number+=1
                buffer.append(clause)
                clauses.append(clause)
        writefile(f"output{file_num}.txt", buffer, number)



def main():
    for i in range(1, 6):
        alpha, kb = readfile(f"input{i}.txt")
        with open(f"output{i}.txt", "w") as file:
            file.write("")
            file.close()
        result = PL_resolution(kb, alpha, i)
        with open(f"output{i}.txt", "a") as file:
            if result:
                print("YES")
                file.write("YES")

            else:
                print("NO")
                file.write("NO")

        # file.close()
    return 0


if __name__ == "__main__":
    main()
