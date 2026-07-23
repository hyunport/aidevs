-- 01_notes-api-with-supabase 예제에서 사용하는 테이블입니다.
--
-- 이 예제의 목표:
-- 1. FastAPI 구조를 router/schema/service로 나눕니다.
-- 2. service 계층에서 Supabase 테이블을 CRUD합니다.
-- 3. 인증/RLS 없이 가장 단순한 DB 연결 흐름부터 확인합니다.

create table if not exists ex90_notes (
  -- id는 각 노트를 구분하는 고유값입니다.
  -- gen_random_uuid()는 Supabase/PostgreSQL이 자동으로 uuid를 만들어 줍니다.
  id uuid primary key default gen_random_uuid(),

  -- title/content는 사용자가 입력하는 필수 텍스트입니다.
  title text not null,
  content text not null,

  -- created_at은 row가 만들어진 시간을 자동 기록합니다.
  created_at timestamp not null default now()
);

-- ex90_notes 테이블에서 사용할 샘플 데이터입니다.
-- id와 created_at은 기본값으로 자동 생성됩니다.
insert into ex90_notes (title, content)
values
  ('첫 번째 노트', 'Supabase 프로젝트를 생성하고 기본 설정을 확인했습니다.'),
  ('두 번째 노트', 'PostgreSQL 테이블 생성 방법을 학습했습니다.'),
  ('세 번째 노트', 'FastAPI 프로젝트의 기본 구조를 정리했습니다.'),
  ('네 번째 노트', '환경 변수에 Supabase URL과 API 키를 등록했습니다.'),
  ('다섯 번째 노트', '노트 목록을 조회하는 API를 구현했습니다.'),
  ('여섯 번째 노트', '새로운 노트를 추가하는 API를 구현했습니다.'),
  ('일곱 번째 노트', '노트 내용을 수정하는 API를 구현했습니다.'),
  ('여덟 번째 노트', '노트를 삭제하는 API를 구현했습니다.'),
  ('아홉 번째 노트', 'API 요청과 응답 형식을 테스트했습니다.'),
  ('열 번째 노트', '프로젝트 실습 내용을 최종 정리했습니다.');
