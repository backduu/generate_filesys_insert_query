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
    print("🚀 FMS 폴더 자동화 스크립트를 시작합니다.")
    print(f"🔹 현재 설정된 모드: {settings.RUN_MODE}")

    files_to_read = []

    # 단일화 대상 파일
    if settings.RUN_MODE == "SINGLE":
        target_file = os.path.join(settings.INPUT_DIR, settings.INPUT_TXT_FILE)
        if not os.path.exists(target_file):
            print(f"[오류] '{target_file}' 파일을 찾을 수 없습니다.")
            return
        files_to_read.append(target_file)
    # 다중화 대상 파일들
    elif settings.RUN_MODE == "MULTI":
        files_to_read = glob.glob(os.path.join(settings.INPUT_DIR, "*.txt"))
        if not files_to_read:
            print(f"[오류] '{settings.INPUT_DIR}' 경로에 .txt 파일이 없습니다.")
            return
    else:
        print("[오류] RUN_MODE는 'SINGLE' 또는 'MULTI'여야 합니다.")
        return

    print(f"총 {len(files_to_read)}개의 대상 파일을 찾았습니다.\n")

    # 파싱 모듈 호출
    unique_folders = parser.extract_unique_folders(files_to_read)

    if not unique_folders:
        print("추출할 폴더 정보가 없어 종료합니다.")
        return

    # SQL 생성 모듈 호출
    output_file_path = os.path.join(settings.OUTPUT_DIR, settings.OUTPUT_SQL_FILE)
    generator.generate_sql(unique_folders, output_file_path, settings.RUN_MODE)

if __name__ == "__main__":
    main()