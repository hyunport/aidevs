# 금요일 과제 함수 형태로 변경한 코드입니다
def input_natural_number():
    while True:
        number_input = input("자연수를 입력하세요(q: 종료): ").strip().lower()

        if number_input == "q":
            print("프로그램을 종료합니다.")
            return None

        is_natural_number = number_input != ""
        for char in number_input:
            if char not in "0123456789":
                is_natural_number = False

        if is_natural_number:
            number = int(number_input)
            if number > 0:
                print(f"입력한 자연수는 {number}입니다.")
                return number

        print("1 이상의 자연수를 다시 입력해주세요.")

input_natural_number()