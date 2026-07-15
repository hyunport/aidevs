# 프로젝트 이름

이 프로젝트가 무엇을 하는지 한두 문장으로 설명합니다.

## 목표

- 목표 1
- 목표 2
- 목표 3

## 실행 방법

```powershell
python main.py
```

## 테스트 방법

```powershell
python -m pytest
```

## 학습 기록

- 배운 점
- 어려웠던 점
- 다음에 개선할 점
````

## 2. 제목 쓰기

Markdown에서는 `#`으로 제목을 만듭니다.

```markdown
# 가장 큰 제목
## 중간 제목
### 작은 제목
```

README에서는 보통 `#` 제목은 한 번만 사용합니다.

## 3. 목록 쓰기

```markdown
- Python 파일 작성
- 테스트 실행
- GitHub에 push
```

숫자 순서가 중요하면 번호 목록을 사용합니다.

```markdown
1. VS Code에서 파일을 수정합니다.
2. Source Control에서 변경 내용을 확인합니다.
3. Commit합니다.
4. GitHub에 Push합니다.
```

## 4. 코드 블록 쓰기

명령어는 코드 블록으로 씁니다.

````markdown
```powershell
python main.py
python -m pytest
```
````

Python 코드는 이렇게 씁니다.

````markdown
```python
def add(a: int, b: int) -> int:
    return a + b
```
````

## 5. 표 쓰기

```markdown
| 항목 | 설명 |
| --- | --- |
| main.py | 프로그램 실행 파일 |
| test_main.py | 테스트 파일 |
| README.md | 프로젝트 설명 문서 |
```

GitHub에서는 아래처럼 보입니다.

| 항목 | 설명 |
| --- | --- |
| main.py | 프로그램 실행 파일 |
| test_main.py | 테스트 파일 |
| README.md | 프로젝트 설명 문서 |

## 6. 링크 넣기

```markdown
[GitHub](https://github.com)
```

같은 프로젝트 안의 파일로 연결할 수도 있습니다.

```markdown
[테스트 파일](./test_main.py)
```
[테스트 파일](./imges)
