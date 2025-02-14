# 버전
- python: 3.11.6
- mysql: 8.1.0
- Poetry: 1.6.1

# 필요 환경 변수
아래의 환경 변수를 프로젝트 레벨('app' 폴더 상위 디렉토리)에서 .env 파일 내에 존재해야 합니다.

- MYSQL_USER: MySQL 유저 아이디
- MYSQL_PASSWORD: MySQL 유저 비밀번호
- MYSQL_HOST: MySQL 호스트
- MYSQL_PORT: MySQL 포트
- MYSQL_DATABASE: MySQL 데이터베이스 이름
- ENVIRONMENT: 환경 ['production', 'develop']
- SECRET_KEY: 임의의 문자열

별도로 사용행하는 디비 안내가 없었기 때문에 무료로 제공해 많은 사람들이 사용하기 좋고, sqlite3 쓸 때를 대비해서 최대한 유사하게 동작하기 좋은 MySQL을 디비로 선택함. 사용자의 컴퓨터에는 해당 데이터베이스가 설치되어 있어야 합니다.

# 서버 구동법
1. 프로젝트 Pull
```bash
git pull origin https://github.com/DJ-Yang/ydj_Quiz.git
```
2. 프로젝트로 이동
```bash
cd ydj_Quiz
```
3. 가상환경 실행
```bash
poetry shell
```
4. 패키지 설치
```bash
poetry install
```
5. 환경 변수 작성
> 상단의 필요 환경 변수 섹션 참조
6. 데이터베이스 스키마 적용
```bash
alembic upgrade head
```
7. 서버 실행
```bash
uvicorn app.main:app --reload
```
8. 문서 접속
> http://localhost:8000/docs


# 고민 사항
## 데이터 수정시
데이터 수정할 경우 기존에 제출했던 정답지를 기준으로 재 채점을 하는 방식으로 해야하나 싶었는데, 보기 자체가 변할 수도 있다고 판단함.(그에 대한 별도의 밸리데이션 안내가 없음) 안전성을 위해 제출 자체를 무효화 시키는 방식으로 변경.