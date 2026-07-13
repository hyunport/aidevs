
# print("이름을 입력하세요:", input())  # 사용자로부터 입력을 받습니다.
# name = input()  # 사용자로부터 이름을 입력받습니다.
# print("나이를 입력하세요:", input())  # 사용자로부터 입력을 받습니다.
# age = int(input())  # 사용자로부터 나이를 입력받습니다.
# print("관심 있는 기술을 입력받습니다.:", input())  # 사용자로부터 입력을 받습니다.
# tech = input()  # 사용자로부터 관심 있는 기술을 입력받습니다.
# print("하루 학습 가능 시간을 입력하세요:", input())  # 사용자로부터 입력을 받습니다.
# study_time = float(input())  # float는 소수점을 포함한 숫자를 나타내는 자료형입니다. 사용자로부터 하루 학습 가능 시간을 입력받습니다.
# print("입력받은 값의 자료형을 출력합니다.")
# print(f"이름: {name}, 자료형: {type(name)}")
# print(f"나이: {age}, 자료형: {type(age)}")
# print(f"관심 있는 기술: {tech}, 자료형: {type(tech)}")
# print(f"하루 학습 가능 시간: {study_time}, 자료형: {type(study_time)}")


###1. 이름을 입력받습니다.
###2. 나이를 입력받습니다.
###3. 관심 있는 기술을 입력받습니다.
###4. 하루 학습 가능 시간을 입력받습니다.
###5. 입력받은 값을 변수에 저장합니다.
###6. 나이는 int로 변환합니다.
###7. 하루 학습 가능 시간은 float으로 변환합니다.
###8. type()으로 각 변수의 자료형을 출력합니다.
###9. f-string으로 자기소개 문장을 출력합니다.



print("start")
name:str = input("이름 입력?")
age:int = int(input("나이 입력?"))
print(f"이름{name} 나이{age-10}")

print("end")
