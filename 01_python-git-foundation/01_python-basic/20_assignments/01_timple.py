# while True:
#     user_input = input("양의 정수를 입력하세요 (종료하려면 'q' 입력): ")

#     if user_input == 'q':
#         print("프로그램을 종료합니다.")
#         break

#     if int(user_input) > 0:
#         print(f"🟢 입력한 양의 정수: {user_input}")
#     else:
#         print("🙅 땡! 양의 정수를 입력하세요.")


##자연수만 받는 입력 받는 코드를 작성하세요.

while True:
    number_input = input("자연수를 입력하세요(q: 종료): ").strip().lower()

    # q를 입력하면 프로그램 종료
    if number_input == "q":
        print("프로그램을 종료합니다.")
        break

    is_natural_number = True

    # 아무것도 입력하지 않은 경우
    if number_input == "":
        is_natural_number = False

    # 입력값을 한 글자씩 검사
    for char in number_input:
        if char not in "0123456789":
            is_natural_number = False

    # 모든 글자가 숫자인 경우에만 정수로 변환
    if is_natural_number:
        number = int(number_input)

        if number > 0:
            print(f"입력한 자연수는 {number}입니다.")

    print("1 이상의 자연수를 다시 입력해주세요.")