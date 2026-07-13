student: list[dict[str, object]] = [
    {
    "name": "Jean",
    "score": 95,
    },
    {
    "name": "mina",
    "score": 65,
    },
    {
    "name": "Jess",
    "score": 70,
    },
]

# 학생들 정보를 출력 합니다. for 반복문을 사용하여 학생들의 이름과 점수를 출력하세요.
for student_info in student:
    print(f"이름: {student_info['name']}, 점수: {student_info['score']}")

# 학생들 성적의 합과 평균을 출력 하시오.
total_score = 0
for student_info in student:
    total_score += student_info['score']
average_score = total_score / len(student)
print(f"합계: {total_score}, 성적 평균: {average_score}" )

for student_info in student:
    print(f"이름: {student_info['name']}, 점수: {student_info['score']}")

# 학생들 성적의 합과 평균을 출력 하시오.
total_score = 0
for student_info in student:
    total_score += student_info['score']
average_score = total_score / len(student)
print(f"합계: {total_score}, 성적 평균: {average_score}" )