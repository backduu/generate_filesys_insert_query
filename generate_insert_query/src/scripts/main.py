import os
import sys
import glob

# 프로젝트 최상위 폴더(루트)를 찾아 sys.path에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(src_dir)

# src 폴더가 아닌 프로젝트 최상위 폴더를 경로에 추가합니다.
if project_root not in sys.path:
    sys.path.append(project_root)

from src.config import settings
from src.core import parser, generator

def main():
    print("FMS 자동화 스크립트를 시작합니다.")
    print(f"🔹 현재 설정된 모드: {settings.RUN_MODE}")

    files_to_read = []

    # 대상 파일 수집
    if settings.RUN_MODE == "SINGLE":
        target_file = os.path.join(settings.INPUT_DIR, settings.INPUT_TXT_FILE)
        if not os.path.exists(target_file):
            print(f"[오류] '{target_file}' 파일을 찾을 수 없습니다.")
            return
        files_to_read.append(target_file)
    elif settings.RUN_MODE == "MULTI":
        files_to_read = glob.glob(os.path.join(settings.INPUT_DIR, "*.txt"))
        if not files_to_read:
            print(f"[오류] '{settings.INPUT_DIR}' 경로에 .txt 파일이 없습니다.")
            return

    print(f"총 {len(files_to_read)}개의 텍스트 파일을 찾았습니다.\n")

    # 파일명에 따라 처리 대상을 분리
    folder_target_files = []
    file_target_files = []

    for f in files_to_read:
        if "(경로와 세부정보 포함)" in os.path.basename(f):
            file_target_files.append(f)
        else:
            folder_target_files.append(f)

    # 폴더 정보 파싱 및 SQL 생성
    if folder_target_files:
        print("\n[STEP 1] 폴더 정보 처리 시작")
        unique_folders = parser.extract_unique_folders(folder_target_files)
        if unique_folders:
            out_folder_sql = os.path.join(settings.OUTPUT_DIR, settings.OUTPUT_SQL_FILE)
            generator.generate_sql(unique_folders, out_folder_sql, settings.RUN_MODE)

    # 파일 정보 파싱 및 SQL 생성
    if file_target_files:
        print("\n[STEP 2] 파일 정보 처리 시작")
        file_records = parser.extract_file_records(file_target_files)
        if file_records:
            out_file_sql = os.path.join(settings.OUTPUT_DIR, settings.OUTPUT_FILE_SQL)
            generator.generate_file_sql(file_records, out_file_sql, settings.RUN_MODE)

    print("\n모든 작업이 완료되었습니다.")

if __name__ == "__main__":
    main()