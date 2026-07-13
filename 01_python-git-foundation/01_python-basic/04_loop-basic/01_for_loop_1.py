# 1 ~ 5 까지의 합과 평균을 구하시오.

datas_number:list = [1,2,3,4,5]
print(type(datas_number))

total_number:int = 0

for data in datas_number:
    total_number += data

print(total_number)
print(total_number/len(datas_number))