import psycopg2
from psycopg2 import extras
from src.config import settings

def execute_values_bulk(table_name, columns, data_list, page_size=10000):
    """
    psycopg2.extras.execute_values를 사용하여 대량 데이터를 효율적으로 삽입
    """
    if not data_list:
        print(f"{table_name}에 삽입할 데이터가 없습니다.")
        return

    conn = None
    try:
        conn = psycopg2.connect(**settings.DB_CONFIG)
        cur = conn.cursor()
        
        # ocean_web 스키마 설정
        cur.execute("SET search_path TO ocean_web, public;")
        
        # 컬럼명을 큰따옴표로 감싸서 대소문자 구분 문제 해결
        quoted_columns = [f'"{col}"' for col in columns]
        column_str = ", ".join(quoted_columns)
        
        query = f'INSERT INTO ocean_web."{table_name}" ({column_str}) VALUES %s ON CONFLICT DO NOTHING'

        total_count = len(data_list)
        print(f"{table_name} 대량 삽입 시작 (총 {total_count}건, 페이지 크기: {page_size})...")
        
        # execute_values 실행
        extras.execute_values(cur, query, data_list, page_size=page_size)
        
        conn.commit()
        print(f"{table_name} 삽입 완료!")
        cur.close()
    except Exception as e:
        print(f"{table_name} 삽입 중 오류 발생: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

def update_bus_info(bus_homes_list):
    """
    fmsBusInfo 테이블 업데이트 (execute_values 사용)
    """
    if not bus_homes_list:
        return

    # execute_values용 튜플 리스트 생성
    data = [(bus_home, bus_home) for bus_home in bus_homes_list]
    
    conn = None
    try:
        conn = psycopg2.connect(**settings.DB_CONFIG)
        cur = conn.cursor()
        
        # ocean_web 스키마 설정
        cur.execute("SET search_path TO ocean_web, public;")
        
        query = """
        INSERT INTO "fmsBusInfo" ("BusFolderHome", "BusNm") 
        VALUES %s
        ON CONFLICT ("BusFolderHome") DO NOTHING;
        """
        
        print(f"fmsBusInfo 업데이트 시작 ({len(data)}건)...")
        extras.execute_values(cur, query, data)
        
        conn.commit()
        print(f"fmsBusInfo 업데이트 완료!")
        cur.close()
    except Exception as e:
        print(f"fmsBusInfo 업데이트 중 오류 발생: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

def process_db_insertion_v2(bus_homes, folder_data, file_data):
    """
    리스트 데이터를 받아서 대량 삽입 프로세스 실행
    """
    print("\n--- [DB 단계] 데이터베이스 대량 삽입 시작 ---")
    
    # fmsBusInfo 업데이트
    # 현재 삽입 필요 없음. 26.06.10
    #update_bus_info(bus_homes)
    
    # fmsFolderInfo 삽입
    # folder_data: [(bus_home, folder_nm), ...]
    if folder_data:
        print("\n--- fmsFolderInfo 데이터 삽입 시작 ---")
        execute_values_bulk("fmsFolderInfo", ["BusFolderHome", "FolderNm"], folder_data)
        
    # fmsFileInfo 삽입
    # file_data: [(bus_home, folder_nm, file_nm, file_capa, file_crt_dt), ...]
    if file_data:
        print("\n--- fmsFileInfo 데이터 삽입 시작 ---")
        # 컬럼 순서 주의: parser에서 반환하는 순서에 맞춰야 함
        # parser.py: (bus_home, folder_nm, file_nm, file_capa, file_crt_dt)
        # DB 컬럼: FileNm, FileCapa, FileCrtDT, BusFolderHome, FolderNm
        
        # 데이터 재정렬 (순서 일치시키기)
        reordered_file_data = [
            (file_nm, file_capa, file_crt_dt, bus_home, folder_nm)
            for bus_home, folder_nm, file_nm, file_capa, file_crt_dt in file_data
        ]
        
        columns = ["FileNm", "FileCapa", "FileCrtDT", "BusFolderHome", "FolderNm"]
        execute_values_bulk("fmsFileInfo", columns, reordered_file_data)
