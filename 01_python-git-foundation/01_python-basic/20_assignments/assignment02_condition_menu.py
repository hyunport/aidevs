print("<항목>")
print("1번: 점수 등급 계산")
print("2번: 숫자 양수/0/음수 판별")
print("3번: 사용자 역할 안내")
print("****그 외에는 알 수 없습니다.****")

number = input("궁금하신 번호를 입력해 주세요:")

match number:
    case "1":

        level = input("점수가 몇점인가요?")
        input_level = int(level)

        if input_level >= 90:
            print("A")
        elif input_level >= 80:
            print("B")
        elif input_level >= 70:
            print("C")
        else:
            print("D")

    case "2":

        count = input("판단할 숫자가 무엇인가요?")
        count1 = int(float(count))

        if count1 > 0:
            print("양수 입니다.")
        elif count1 == 0:
            print("숫자가 없습니다.")
        elif count1 < 0:
            print("음수 입니다.")
        else:
            print("숫자가 아닙니다.")
    
    case "3":
        print("역할에 대해 설명 드리겠습니다.")
        print("admin")
        print("member")
        print("guest")

        name = input("위 항목 중 어떤 역할을 담당하고 있으신가요")

        if name == "admin":
            print("관리자입니다.")
        elif name == "member":
            print("일반 사용자입니다.")
        elif name == "guest":
            print("게스트입니다.")
        else:
            print("알 수 없는 역할입니다.")

print("END...")