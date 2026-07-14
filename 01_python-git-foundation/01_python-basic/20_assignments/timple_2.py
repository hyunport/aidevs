# # 금요일 과제 함수 형태로 변경한 코드입니다
# def input_natural_number():
#     while True:
#         number_input = input("자연수를 입력하세요(q: 종료): ").strip().lower()

#         if number_input == "q":
#             print("프로그램을 종료합니다.")
#             return None

#         is_natural_number = number_input != ""
#         for char in number_input:
#             if char not in "0123456789":
#                 is_natural_number = False

#         if is_natural_number:
#             number = int(number_input)
#             if number > 0:
#                 print(f"입력한 자연수는 {number}입니다.")
#                 return number

#         print("1 이상의 자연수를 다시 입력해주세요.")

# input_natural_number()



# 자연수를 알려주는 함수를 만든다.
def auto_cheak():
    # 입력받은 데이터를 가공한다.
    input_data = input("자연수를 입력해 주세요. (q: 종료): ").strip().lower()
    
    # 반복할 내용을 작성한다.
    while True:
        # q를 누르면 프로그램이 종료됩니다.
        if input_data == "q":
            print("프로그램이 종료 됩니다.")
        return None
    
        # 자연수인지 확인하는 작업을 만듭니다.
        number_input_data = input_data != ""
        for cheak in input_data:
            if cheak not in "0123456789":
                number_input_data = False

        
#         is_natural_number = number_input != ""
#         for char in number_input:
#             if char not in "0123456789":
#                 is_natural_number = False

#         if is_natural_number:
#             number = int(number_input)
#             if number > 0:
#                 print(f"입력한 자연수는 {number}입니다.")
#                 return number

#         print("1 이상의 자연수를 다시 입력해주세요.")

# input_natural_number()
















