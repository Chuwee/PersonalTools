dic = {
    "A" : 4,
    "B" : 8,
    "E" : 3,
    "G" : 6,
    "I" : 1,
    "O" : 0,
    "S" : 5,
    "T" : 7,
}

def main():
    a = input("")
    la = len(a)
    ca = a.upper()
    na = ""
    for c in ca:
        if c in dic:
            na+=str(dic[c])
    ina=int(na)
    p=a[0] + str(la) + na + str(ina+la) + str(ina*la) + a[2]
    print(p)
    t = input("Yes?")
    if t == "Y":
        return
    else:
        p+=a
    print(p)

main()