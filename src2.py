


def readfile(filename):
    with open(filename, "r") as file:
        alpha = file.readline().strip()
        number = int(file.readline().strip())
        kb = []
        for i in range(number):
            kb.append(file.readline().strip())

    file.close()
    return alpha, kb

def writefile(filename, buffer):
    
    with open(filename,"a") as file:
        file.write(str(len(buffer))+"\n")
        for i in list(buffer):
            formatted_content = ' OR '.join(
                [elem if elem.startswith('-') else f"{elem}" for elem in i])
            file.writelines(str(formatted_content)+'\n')
         
def negativeAlpha(alpha):
    if '-' not in alpha:
        return [(f"-{alpha}")]
    else:
        return [alpha.replace('-','')]
    
def resolve(ci, cj):
    resolvents = []
    for literal in ci:
        if '-' in literal:
            if literal.replace("-", "") in cj:
                resolvent = sorted(set(ci) | set(cj))
                resolvent.remove(literal)
                resolvent.remove(literal.replace("-", ""))
                resolvents.append(
                    (resolvent))
        else:
            if f'-{literal}' in cj:
                resolvent = sorted(set(ci) | set(cj))
                resolvent.remove(literal)
                resolvent.remove(f'-{literal}')
                resolvents.append((resolvent))

    return resolvents

def is_sample(src, check:list):
    i=0
    while i < len(check):
        if check[i] in src:
            check.remove(check[i])
        else:
            i=i+1
    
    return check
            
        
        

def PL_resolution(kb, alpha,fileNumber):
    KB = kb + negativeAlpha(alpha)
    clauses = ([(clause.split(' OR ')) for clause in KB])
    buffer = list()
    while True:
        new_clauses = []
        pairs = [(clauses[i], clauses[j])
                 for i in range(len(clauses)) for j in range(i + 1, len(clauses))]
        for (ci, cj) in pairs:
            resolvent = resolve(ci, cj)
            for i in resolvent:
                if not i:
                    result = True
                    return result,buffer
                #return True
            if len(resolvent) != 0:
                new_clauses.extend(resolvent)
                

        if len(is_sample(clauses,new_clauses)) == 0:
            result = False
            return result,buffer

        buffer.extend(new_clauses)
        clauses.extend(new_clauses)
        writefile(f"output{fileNumber}.txt",buffer)
        buffer.clear()



def main():
    for i in range(1, 7):
        alpha, kb = readfile(f"input{i}.txt")
        with open(f"output{i}.txt", "w") as file:
            file.write("")
            file.close()
        result,buffer = PL_resolution(kb, alpha,i)
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
