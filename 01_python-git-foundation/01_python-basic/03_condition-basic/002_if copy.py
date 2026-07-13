import sys

print("start....")
input_data = input("무슨 카드인가요?")

if(input_data != "카드1"):
    sys.exit

if(input_data == "카드1"):
    print("카드1 업무 진행")
else:
    print("카드2 업무 진행")

print("end ...")
