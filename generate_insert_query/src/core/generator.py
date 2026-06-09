import os

# ==========================================
# SQL 형식으로 포장해서 파일로 저장
# ==========================================
def escape_string(val):
    if val is None:
        return ""
    return val.replace("'", "''")

def generate_sql(unique_folders, output_path, run_mode):
    """파싱된 폴더 데이터를 바탕으로 SQL 파일을 생성합니다."""
    print("-" * 50)
    print("SQL 파일 생성을 시작합니다...")

    # 출력 폴더가 존재하지 않으면 자동으로 생성
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("-- fmsFolderInfo 테이블 대량 INSERT 스크립트\n")
        f.write(f"-- 생성 모드: {run_mode}\n")

        f.write("BEGIN TRANSACTION;\n\n")

        f.write(f"-- {output_path}\n")
        for bus_home, folder_nm in sorted(unique_folders):
            esc_bus = escape_string(bus_home)
            esc_folder = escape_string(folder_nm)

            query = f"INSERT INTO fmsFolderInfo (BusFolderHome, FolderNm) VALUES ('{esc_bus}', '{esc_folder}');\n"
            f.write(query)

        f.write("\nCOMMIT;\n")

    print(f"\n[완료] 총 {len(unique_folders)}개의 고유 폴더 INSERT 쿼리가 저장되었습니다!")
    print(f"저장 위치: {output_path}")