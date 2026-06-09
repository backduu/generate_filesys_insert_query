import os

# ==========================================
# 파일을 읽어서 유효한 폴더 경로만 추출하고 중복을 제거
# ==========================================
def extract_unique_folders(file_paths):
    unique_folders = set()

    for txt_file in file_paths:
        print(f" -> 파싱 중: {os.path.basename(txt_file)}")
        with open(txt_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 윈도우 경로를 안전한 슬래시로 변환
            line = line.replace('\\', '/')
            parts = [p for p in line.split('/') if p]

            # 유효성 검사
            if len(parts) < 2:
                continue

            # 마지막 요소가 파일이면 제거 (확장자 존재 여부로 판단)
            if '.' in parts[-1]:
                parts.pop()

            bus_home = parts[1]
            folder_nm = "/" + "/".join(parts[2:]) if len(parts) > 2 else "/"

            # 중복 제거를 위해 Set에 추가
            unique_folders.add((bus_home, folder_nm))

    return unique_folders
