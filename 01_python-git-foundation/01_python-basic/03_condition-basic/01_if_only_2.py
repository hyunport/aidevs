# 숫자를 입력 받는다(1~10)
# 숫자가 아니면 프로그램 종료
# 숫자이면 출력

import sys
# number = int(import("1~10 중 하나를 입려해주세요."))


print("start..")

input_set = (input("숫자 입력해(1~10)"))
input_number = int(input_set)
# if(input_number < 1):
#     sys.exit()


if(input_number < 1 or input_number > 10):
    sys.exit()

print(f"입력 숫자는 {input_number}")
print("End..")


# if(input_number > 10):
#     sys.exit()