import os

# ==========================================
# 파일을 읽어서 유효한 폴더 경로만 추출하고 중복을 제거
# ==========================================
def extract_unique_folders(file_paths):
    unique_folders = set()

    for txt_file in file_paths:
        print(f" -> 파싱 중: {os.path.basename(txt_file)}")
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

            # 윈도우 경로를 안전한 슬래시로 변환
            line = line.replace('\\', '/')
            parts = [p for p in line.split('/') if p]

            # 파싱된 요소가 최소 2개(드라이브명/폴더명)는 되어야 함
            if len(parts) < 2:
                # 데이터가 깨진 경우 로그를 남기고 건너뜁니다.
                continue

            # 파일명 제거 로직
            # 마지막 요소에 '.'이 포함되어 있으면 파일로 간주하고 제거
            if '.' in parts[-1]:
                parts.pop()
                # 팝 이후에 길이가 다시 2 미만이 되면 유효하지 않은 경로임
                if len(parts) < 2:
                    continue

            bus_home = parts[1]
            folder_nm = "/" + "/".join(parts[2:]) if len(parts) > 2 else "/"

            unique_folders.add((bus_home, folder_nm))

    return unique_folders
