# 버전
- python: 3.11.6
- mysql: 8.1.0

# 필요 환경 변수
- MYSQL_USER: MySQL 유저 아이디
- MYSQL_PASSWORD: MySQL 유저 비밀번호
- MYSQL_HOST: MySQL 호스트
- MYSQL_PORT: MySQL 포트
- MYSQL_DATABASE: MySQL 데이터베이스 이름
- ENVIRONMENT: 환경 ['production', 'develop']
- SECRET_KEY: 임의의 문자열

별도로 사용행하는 디비 안내가 없었기 때문에 무료로 제공해 많은 사람들이 사용하기 좋고, sqlite3 쓸 때를 대비해서 최대한 유사하게 동작하기 좋은 MySQL을 디비로 선택함. 사용자의 컴퓨터에는 해당 데이터베이스가 설치되어 있어야 합니다.

# 고민 사항
## 데이터 수정시
데이터 수정할 경우 기존에 제출했던 정답지를 기준으로 재 채점을 하는 방식으로 해야하나 싶었는데, 보기 자체가 변할 수도 있다고 판단함.(그에 대한 별도의 밸리데이션 안내가 없음) 안전성을 위해 제출 자체를 무효화 시키는 방식으로 변경.