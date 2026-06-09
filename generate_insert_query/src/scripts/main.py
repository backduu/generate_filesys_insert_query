import os

# ==========================================
# 설정 정보
# ==========================================
INPUT_TXT_FILE = "C:\\Users\\kmuu0\\Desktop\\업무관련내용(부산연계)\\working\\2025년 관할해역 해양기본조사(울산부근) 폴더 및 파일 목록.txt"


# 결과 파일 .sql 형식
OUTPUT_SQL_FILE = os.path.dirname(INPUT_TXT_FILE) + "\\output.sql"

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

    for i, line in enumerate(lines):
        line = line.strip()
        if not line: continue
        line = line.replace('\\', '/')
        parts = [p for p in line.split('/') if p]
        if len(parts) < 2: continue
        if '.' in parts[-1]: parts.pop()

        bus_home = parts[1]
        folder_nm = "/" + "/".join(parts[2:]) if len(parts) > 2 else "/"
        unique_folders.add((bus_home, folder_nm))

        if i < 5:
            print(f"원본: {line.strip()} -> 해석결과: {bus_home}, {folder_nm}")

# ==========================================
# SQL 파일 작성
# ==========================================
    with open(OUTPUT_SQL_FILE, 'w', encoding='utf-8') as f:
        f.write("-- fmsFolderInfo 테이블 대량 INSERT 스크립트\n")
        f.write("BEGIN TRANSACTION;\n\n")

        # 정렬해서 보기 좋게 INSERT 문 생성
        for bus_home, folder_nm in sorted(unique_folders):
            esc_bus = escape_string(bus_home)
            esc_folder = escape_string(folder_nm)

            query = f"INSERT INTO fmsFolderInfo (BusFolderHome, FolderNm) VALUES ('{esc_bus}', '{esc_folder}');\n"
            f.write(query)

        f.write("\nCOMMIT;\n")

    print(f"\n[완료] 총 {len(unique_folders)}개의 고유 폴더 INSERT 쿼리가 '{OUTPUT_SQL_FILE}'에 생성되었습니다!")

if __name__ == "__main__":
    generate_folder_inserts()