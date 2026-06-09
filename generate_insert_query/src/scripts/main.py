import os

# ==========================================
# 설정 정보
# ==========================================
INPUT_TXT_FILE = "2025년 관할해역 해양기본조사(울산부근) 폴더 및 파일 목록.txt"


# 결과 파일 .sql 형식
OUTPUT_SQL_FILE = "output.sql"

def escape_string(val):
    if val is None:
        return ""
    return val.replace("'", "''")


# ==========================================
# 텍스트 파싱 및 SQL 생성 로직
# ==========================================
def generate_folder_inserts():
    if not os.path.exists(INPUT_TXT_FILE):
        print(f"[오류] '{INPUT_TXT_FILE}' 파일을 찾을 수 없습니다. 파일명을 확인해주세요.")
        return

    # 중복된 폴더 쿼리 생성을 막기 위한 집합(Set)
    unique_folders = set()

    with open(INPUT_TXT_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 윈도우 경로(\)를 안전한 슬래시(/)로 통일
        line = line.replace('\\', '/')

        # 슬래시(/)를 기준으로 분리하고 빈 문자열 제거
        # 예: ['e:', '2025_Ulsan', '01_SBE', '01_RAW']
        parts = [p for p in line.split('/') if p]

        # 최소한 드라이브명과 사업폴더명은 있어야 진행 (예: e:/2025_Ulsan)
        if len(parts) < 2:
            continue

        # 마지막 요소가 파일인지 확인 (확장자 '.' 포함 여부로 판단)
        if '.' in parts[-1]:
            parts.pop() # 파일명을 제거하여 폴더 경로만 남김

        # 사업폴더명 추출
        bus_home = parts[1] # '2025_Ulsan'

        # 폴더 경로명 조립
        if len(parts) > 2:
            folder_nm = "/" + "/".join(parts[2:])
        else:
            folder_nm = "/" # 최상위 루트 폴더인 경우

        # 튜플 형태로 Set에 추가 (자동으로 중복 제거됨)
        unique_folders.add((bus_home, folder_nm))

        print(f"\n[완료] 총 {len(unique_folders)}개의 고유 폴더 INSERT 쿼리가 '{OUTPUT_SQL_FILE}'에 생성되었습니다!")
if __name__ == "__main__":
    generate_folder_inserts()