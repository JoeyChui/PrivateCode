def jvli(s1, s2):
    result = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            result += 1
    return result

s1 = "ababba"
s2 = "ba"

allsum = 0 # 距离的和

start = 0 # 头指针
length = len(s2)

zichuannumber = len(s1) - len(s2) + 1

for i in range(zichuannumber):
    allsum += jvli(s1[start : start + length], s2)
    start += 1
print(allsum)
# print(jvli(s1, s2))
