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

# 3. 모든 학생의 평균점수보다 낮은 학생들을 조회 하세요.
# filter_passed_students(students:list) -> tuple: