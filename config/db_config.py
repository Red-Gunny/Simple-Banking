# config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///my_database.db'  # SQLite 데이터베이스 파일 경로
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 성능을 위해 False로 설정
    SQLALCHEMY_POOL_SIZE = 10  # 기본 커넥션 풀의 크기
    SQLALCHEMY_MAX_OVERFLOW = 5  # 기본 풀 크기를 초과하여 생성할 수 있는 커넥션 수
    SQLALCHEMY_POOL_TIMEOUT = 30  # 커넥션 대기 시간 (초)
    SQLALCHEMY_POOL_RECYCLE = 1800  # 커넥션 재사용 시간 (초)