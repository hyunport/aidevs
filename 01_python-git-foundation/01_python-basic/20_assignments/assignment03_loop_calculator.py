while True:
    # 1. 첫 번째 숫자를 입력받습니다.
    num1_input = input("첫 번째 숫자를 입력하세요 (종료하려면 'q' 입력): ")
    
    # 2. 첫 번째 입력값이 q이면 프로그램을 종료합니다. (break 사용)
    if num1_input == 'q':
        print("프로그램을 종료합니다.")
        break
        
    # 3. 두 번째 숫자를 입력받습니다.
    num2_input = input("두 번째 숫자를 입력하세요: ")
    
    # 4. 연산자를 입력받습니다.
    operator = input("연산자(+, -, *, /)를 입력하세요: ")
    
    # 계산을 위해 입력받은 문자열을 숫자(실수형)로 변환합니다.
    num1 = float(num1_input)
    num2 = float(num2_input)
    
    # 5. [추가 요구사항] 잘못된 연산자를 입력하면 안내 문장을 출력하고 처음으로 돌아갑니다.
    if operator not in ['+', '-', '*', '/']:
        print("[오류] 잘못된 연산자입니다. 처음부터 다시 입력해주세요.\n")
        continue  # (continue 사용)
        
    # 6. [요구사항] 0으로 나누는 경우 안내 문장을 출력하고 처음으로 돌아갑니다.
    if operator == '/' and num2 == 0:
        print("[오류] 0으로 나눌 수 없습니다. 처음부터 다시 입력해주세요.\n")
        continue  # (continue 사용)
        
    # 7. 연산자에 따른 계산 결과 출력
    if operator == '+':
        result = num1 + num2
    elif operator == '-':
        result = num1 - num2
    elif operator == '*':
        result = num1 * num2
    elif operator == '/':
        result = num1 / num2
        
    print(f"👉 계산 결과: {result}\n")
    # 8. 계산 후 while True에 의해 자동으로 다음 계산을 시작합니다.