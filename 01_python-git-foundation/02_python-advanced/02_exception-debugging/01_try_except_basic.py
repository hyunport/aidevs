r"""try/except 기본 예제입니다.

실행 위치:
    C:\aidev\01_python-git-foundation

실행 명령:
    python .\02_python-advanced\02_exception-debugging\01_try_except_basic.py

이 예제의 목표:
    문자열을 숫자로 바꿀 때 발생할 수 있는 ValueError를 처리합니다.
"""


def to_int_or_default(value: str) -> int:
    """문자열을 int로 바꾸고, 실패하면 기본값을 반환합니다."""
    try:
        result = int(value)
    except: # 문제가 발생을 할 했을 때 여기로 데이터가 들어옴. 오류를 처리하는 방식.
        return None
    return result

    # try:
    #     return int(value)
    # except ValueError:
    #     print(f"'{value}'는 숫자로 바꿀 수 없습니다. 기본값 {default}을 사용합니다.")
    #     return default

def dvided(num1:int, num2:int) -> float:
    # 오류 방지를 위한 예외 코드: 0으로는 나눌 수 없는 오류에 대한 문제.
    try:
        result = num1 / num2
    except:
        return None
    return result

    # if num2 == 0:
    #     return None
    # return num1 / num2


def main() -> None:
    values = ["10", "abc", "30"]

    for value in values:
        number = to_int_or_default(value)
        print("변환 결과:", number)

    result = dvided(10,5)
    print(result)

main()
