import psycopg2
from src.config import settings

def execute_sql_file(file_path):
    """
    SQL 파일을 읽어서 DB에서 실행
    """
    conn = None
    try:
        # DB 연결
        conn = psycopg2.connect(**settings.DB_CONFIG)
        cur = conn.cursor()
        
        print(f"SQL 파일 읽는 중: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            sql_commands = f.read()
            
        if not sql_commands.strip():
            print(f"SQL 파일이 비어 있습니다: {file_path}")
            return

        print(f"🚀 SQL 명령 실행 중...")
        # ocean_web 스키마를 search_path에 추가하여 테이블을 찾을 수 있게 함
        cur.execute("SET search_path TO ocean_web, public;")
        cur.execute(sql_commands)
        
        # 변경사항 반영
        conn.commit()
        print(f"성공적으로 실행되었습니다: {file_path}")
        
        cur.close()
    except Exception as e:
        print(f"SQL 실행 중 오류 발생: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

def update_bus_info():
    """
    fmsFolderInfo에 들어갈 데이터를 바탕으로 fmsBusInfo 테이블을 먼저 업데이트
    """
    import os
    from src.core import parser
    import glob

    # 입력 파일들 수집
    files_to_read = glob.glob(os.path.join(settings.INPUT_DIR, "*.txt"))
    if not files_to_read:
        return

    # 폴더 정보 파싱 (BusFolderHome 추출용)
    folder_target_files = [f for f in files_to_read if "(경로와 세부정보 포함)" not in os.path.basename(f)]
    unique_folders = parser.extract_unique_folders(folder_target_files)
    
    # 중복 제거된 BusFolderHome 목록 (BusNm은 BusFolderHome과 동일하게 설정하거나 앞부분 추출)
    bus_homes = set(bus_home for bus_home, _ in unique_folders)
    
    conn = None
    try:
        conn = psycopg2.connect(**settings.DB_CONFIG)
        cur = conn.cursor()
        
        # 스키마 목록 확인 및 테이블 확인
        cur.execute("SELECT schema_name FROM information_schema.schemata;")
        schemas = cur.fetchall()
        print(f"🔍 사용 가능한 스키마: {[s[0] for s in schemas]}")
        
        cur.execute("SELECT table_schema, table_name FROM information_schema.tables WHERE table_name ILIKE 'fms%';")
        tables = cur.fetchall()
        print(f"🔍 fms 관련 테이블: {tables}")

        for bus_home in bus_homes:
            # 존재하지 않으면 삽입 (ocean_web 스키마 명시)
            query = """
            INSERT INTO ocean_web."fmsBusInfo" ("BusFolderHome", "BusNm") 
            VALUES (%s, %s)
            ON CONFLICT ("BusFolderHome") DO NOTHING;
            """
            cur.execute(query, (bus_home, bus_home))
            
        conn.commit()
        print(f"fmsBusInfo 업데이트 완료 ({len(bus_homes)}건 처리)")
        cur.close()
    except Exception as e:
        print(f"fmsBusInfo 업데이트 중 오류 발생: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

def process_db_insertion():
    """
    output 폴더의 SQL 파일들을 DB에 삽입
    """
    import os
    
    # fmsBusInfo 삽입 (폴더 정보를 기반으로 추출)
    #print("\n--- fmsBusInfo 데이터 업데이트 시작 ---")
    #update_bus_info()
    
    # Folder Info 삽입 (fmsFolderInfo)
    folder_sql_path = os.path.join(settings.OUTPUT_DIR, settings.OUTPUT_SQL_FILE)
    if os.path.exists(folder_sql_path):
        print("\n--- fmsFolderInfo 데이터 삽입 시작 ---")
        execute_sql_file(folder_sql_path)
    else:
        print(f"파일을 찾을 수 없습니다: {folder_sql_path}")

    # File Info 삽입 (fmsFileInfo)
    file_sql_path = os.path.join(settings.OUTPUT_DIR, settings.OUTPUT_FILE_SQL)
    if os.path.exists(file_sql_path):
        print("\n--- fmsFileInfo 데이터 삽입 시작 ---")
        execute_sql_file(file_sql_path)
    else:
        print(f"파일을 찾을 수 없습니다: {file_sql_path}")
