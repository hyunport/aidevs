"""실행 폴더의 환경 변수를 공용 모듈보다 먼저 읽습니다."""

from pathlib import Path

from dotenv import load_dotenv


def load_local_env() -> None:
    load_dotenv(Path(__file__).resolve().with_name(".env"), override=False)

