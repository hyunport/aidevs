print("start...")

import sys

while True:
    print("Menu start")
    cmd = input("input cmd")
    print(f"입력하신 정보는 {cmd}")
    if (cmd == "q"):
        print("bye...")
        sys.exit()      
print("end...")