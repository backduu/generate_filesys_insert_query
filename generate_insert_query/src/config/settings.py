import os

# ==========================================
# 사용자 설정
# ==========================================
# 실행 모드: "SINGLE" (단일 파일) 또는 "MULTI" (다중 파일)
RUN_MODE = "MULTI"

# [SINGLE 모드용] 단일 대상 파일명
INPUT_TXT_FILE = "folder_list.txt"

# 결과물 SQL 파일명
OUTPUT_SQL_FILE = "insert_folders.sql"
OUTPUT_FILE_SQL = "insert_files.sql"

# ==========================================
# 경로 자동 설정 **** 수정 금지 *****
# ==========================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# data/input 및 data/output 절대 경로
INPUT_DIR = os.path.join(BASE_DIR, "data", "input")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "output")

# ==========================================
# DB 설정
# ==========================================
DB_CONFIG = {
    "host": "toisgis.iptime.org",
    "database": "ofsdb",
    "port": "15432",
    "user": "ocean_web",
    "password": "ocean#$bada"
}