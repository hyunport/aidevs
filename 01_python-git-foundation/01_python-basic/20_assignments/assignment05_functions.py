students = [
    {"name": "Jean", "score": 95},
    {"name": "Mina", "score": 82},
    {"name": "Jun", "score": 58},
    {"name": "son", "score":90},
    {"name": "kim", "score": 35},
    {"name": "lee", "score": 30},
]

# 1. 학생들의 평균점수를 출력 한다.
# calculate_average(students:list) -> float:

def calculate_average(students: list) -> float:
    if not students:
        return 0.0
    return sum(students) / len(students)



# 2. 학생의 학점(9, 8, 7, 6)과 패스여부(60)를 출력 한다.
# filter_passed_students(student:dict) -> tuple(str, bool):

def filter_passed_students(student: dict) -> tuple:
    score = student["score"]

    if score >= 90:
        grade = 9
    elif score >= 80:
        grade = 8
    elif score >= 70:
        grade = 7
    else:
        grade = 6

    passed = score >= 60
    return grade, passed

# 3. 모든 학생의 평균점수보다 낮은 학생들을 조회 하세요.
# filter_passed_students(students:list) -> tuple:

def calculate_average(students: list) -> float:
    if not students:
        return 0.0

    total = 0
    for student in students:
        total += student["score"]

    return total / len(students)

def filter_below_average_students(students: list) -> tuple:
    average = calculate_average(students)
    below_average_students = []

    for student in students:
        if student["score"] < average:
            below_average_students.append(student)

    return tuple(below_average_students)

result = filter_below_average_students(students)
print(result)