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

            # 윈도우 경로 변환
            line = line.replace('\\', '/')
            parts = [p for p in line.split('/') if p]

            # 경로가 드라이브(e:)로 시작하는지 체크

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
