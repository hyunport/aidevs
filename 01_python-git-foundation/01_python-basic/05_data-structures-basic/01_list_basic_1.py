numbers: list[int] = [1, 2, 3, 4, 5]

# # 1. 출력
print("numbers:", numbers)

# 2. 마지막에 6을 추가
numbers.append(6)

# 3. 전체 합과 평균을 출력
sum_number = 0
count_even = 0
for n in numbers:
    if n % 2 == 0:
        sum_number += n
        count_even += 1

average_number = sum_number / count_even
print(f"평균: {average_number} 과 합계: {sum_number}")

# for문으로 작성해본다.
for n in numbers:
    sum_number += n

print("합계:", sum_number)

average_number = sum_number / len(numbers)
print(f"평균: {average_number} 과 합계: {sum_number}")


# 평소에 사용하는 것
total = sum(numbers)
average = total / len(numbers)
print("합계:", total)
print("평균:", average)