### 주의사항
1. python version : ^3.11 -> 파이썬 버전은 3.11이상을 사용하셔야 합니다.
2. 환경 변수 파일 .env 파일을 만들어주셔야 합니다.


### 데이터 베이스로 mysql 사용 안내 및 이유
db_user: str | None = os.environ.get("MYSQL_USER")
db_password: str | None = os.environ.get("MYSQL_PASSWORD")
db_host: str | None = os.environ.get("MYSQL_HOST")
db_port: str | None = os.environ.get("MYSQL_PORT")
db_name: str | None = os.environ.get("MYSQL_DATABASE")

sqlite를 사용할 경우를 고려해서 최대한 유사한 형식으로 동작하는 디비를 선택. 단, 범용성을 위해서 다른 디비를 붙일 수 있도록 위와 같이 환경 변수를 이용하는 방식으로 세팅