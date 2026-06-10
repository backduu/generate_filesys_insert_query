import os

# ==========================================
# 파일을 읽어서 유효한 폴더 경로만 추출하고 중복을 제거
# ==========================================
def parse_file(txt_file):
    """단일 파일을 파싱하여 고유 폴더 세트를 반환합니다."""
    unique_folders = set()
    print(f" -> 파싱 중: {os.path.basename(txt_file)}")
    try:
        with open(txt_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"    [경고] 파일 읽기 실패: {txt_file}, 에러: {e}")
        return unique_folders

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 윈도우 경로 변환
        line = line.replace('\\', '/')
        parts = [p for p in line.split('/') if p]

        # 마지막 요소가 파일이면 제거
        if '.' in parts[-1]:
            parts.pop()

        # 이제 parts에 남은 경로 요소들의 길이를 기준으로 처리
        if len(parts) < 1:
            continue

        # 드라이브 문자(':')가 포함되어 있는지 확인
        has_drive = ':' in parts[0]

        if has_drive:
            # 드라이브가 있으면 [드라이브, 사업폴더, ...] 형태 -> 인덱스 1 사용
            if len(parts) < 2: continue
            bus_home = parts[1]
            folder_nm = "/" + "/".join(parts[2:]) if len(parts) > 2 else "/"
        else:
            # 드라이브가 없으면 [사업폴더, ...] 형태 -> 인덱스 0 사용
            bus_home = parts[0]
            folder_nm = "/" + "/".join(parts[1:]) if len(parts) > 1 else "/"

        unique_folders.add((bus_home, folder_nm))

    return unique_folders

def extract_unique_folders(file_paths):
    """여러 파일을 파싱하여 전체의 고유 폴더 세트를 합쳐서 반환합니다 (기존 호환성 유지)."""
    all_unique_folders = set()
    for txt_file in file_paths:
        all_unique_folders.update(parse_file(txt_file))
    return all_unique_folders

# ==========================================
# 🆕 새 함수: 세부정보가 포함된 텍스트에서 '파일 정보'만 추출
# ==========================================
def extract_file_records(file_paths):
    file_records = []

    for txt_file in file_paths:
        print(f" -> [파일 정보] 파싱 중: {os.path.basename(txt_file)}")
        try:
            with open(txt_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"    [경고] 파일 읽기 실패: {txt_file}, 에러: {e}")
            continue

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 탭(\t)을 기준으로 데이터 분할
            cols = line.split('\t')
            
            # 최소 경로, 용량, 날짜 데이터가 있어야 함
            if len(cols) < 3:
                continue

            path_str = cols[0].replace('\\', '/')
            size_str = cols[1].strip()
            date_str = cols[2].strip()

            # 💡 핵심: 용량 컬럼이 <폴더>이면 건너뜀 (순수 파일만 골라냄!)
            if size_str == "<폴더>":
                continue

            # 쉼표(,)가 포함된 용량 문자열을 정수형(Int)으로 변환
            # KB 단위를 Byte로 변환하여 DB의 INTEGER 범위를 넘을 수 있으므로 주의 필요
            # 그러나 fmsFileInfo의 FileCapa는 INTEGER로 정의됨 (PostgreSQL INTEGER: -2,147,483,648 to 2,147,483,647)
            # 만약 파일 크기가 2GB를 넘으면 오류 발생 가능.
            try:
                file_capa = int(size_str.replace(',', ''))
                # INTEGER 범위를 넘어가면 최대값으로 제한 (또는 0으로 처리)
                if file_capa > 2147483647:
                    file_capa = 2147483647
            except ValueError:
                file_capa = 0

            # 경로 파싱
            parts = [p for p in path_str.split('/') if p]
            if len(parts) < 2:
                continue

            has_drive = ':' in parts[0]

            if has_drive:
                if len(parts) < 3: continue # [e:, 2025_Ulsan, 파일명] 최소 3개
                bus_home = parts[1]
                file_nm = parts[-1]
                folder_nm = "/" + "/".join(parts[2:-1]) if len(parts) > 3 else "/"
            else:
                if len(parts) < 2: continue
                bus_home = parts[0]
                file_nm = parts[-1]
                folder_nm = "/" + "/".join(parts[1:-1]) if len(parts) > 2 else "/"

            # 날짜 데이터 정제 (예: '2025-11-24 10:10' -> '2025-11-24')
            file_crt_dt = date_str[:10]

            # 리스트에 파일 정보 튜플 추가
            file_records.append((bus_home, folder_nm, file_nm, file_capa, file_crt_dt))

    return file_records
