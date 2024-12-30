import pandas as pd
import re
import os

# 설정
map_name = "Ice Carbon Diablo X"
input_file_path = os.path.join("tracks", f"{map_name}.txt")
save_file_path = os.path.join("records", f"{map_name}.csv")

# 데이터 저장을 위한 딕셔너리 초기화
# 키: 날짜, 값: 퍼센트 카운트 딕셔너리
sessions_dict = {}

# 정규 표현식 패턴 정의
session_pattern = re.compile(r'^Session:\s*$')  # 'Session:'만 있는 라인
date_pattern = re.compile(r'^(\d{2}/\d{2}/\d{4})$')  # 날짜 형식
percent_pattern = re.compile(r'^(\d{1,3})%\s*x(\d+)$')  # 퍼센트 기록 패턴

# 현재 세션 정보를 저장할 변수
current_session = None
flag_next_line_is_date = False

# 파일 읽기
try:
    with open(input_file_path, 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, 1):
            line = line.strip()
            if not line:
                continue  # 빈 줄은 무시

            # 날짜를 다음 줄에서 읽어야 하는 상태인지 확인
            if flag_next_line_is_date:
                date_match = date_pattern.match(line)
                if date_match:
                    current_session = date_match.group(1)
                    if current_session not in sessions_dict:
                        sessions_dict[current_session] = {}
                    flag_next_line_is_date = False
                else:
                    print(f"경고: 'Session:' 다음에 날짜가 예상되었으나, '{line}' 형식과 일치하지 않습니다. (라인 {line_num})")
                    flag_next_line_is_date = False
                continue

            # 'Session:' 라인인지 확인
            session_match = session_pattern.match(line)
            if session_match:
                # 다음 줄에서 날짜를 읽어야 함
                flag_next_line_is_date = True
                continue

            # 퍼센트 기록인지 확인
            percent_match = percent_pattern.match(line)
            if percent_match and current_session is not None:
                percent = int(percent_match.group(1))
                count = int(percent_match.group(2))
                # 해당 퍼센트의 카운트 누적
                if percent in sessions_dict[current_session]:
                    sessions_dict[current_session][percent] += count
                else:
                    sessions_dict[current_session][percent] = count
            else:
                print(f"경고: 퍼센트 기록을 해석할 수 없는 라인입니다: '{line}' (라인 {line_num})")

    # 파일 읽기 완료 후 데이터 확인
    if not sessions_dict:
        print("경고: 어떠한 세션 데이터도 발견되지 않았습니다.")
except FileNotFoundError:
    print(f"오류: 파일을 찾을 수 없습니다: {input_file_path}")
    exit(1)
except Exception as e:
    print(f"예기치 않은 오류가 발생했습니다: {e}")
    exit(1)

# 데이터프레임으로 변환을 위한 리스트 초기화
data_rows = []

# 0부터 100까지 퍼센트를 칼럼으로 설정
percent_range = range(0, 101)

for date, percent_counts in sessions_dict.items():
    row = {'Date': date}
    for p in percent_range:
        row[p] = percent_counts.get(p, 0)
    data_rows.append(row)

# 데이터프레임 생성
df = pd.DataFrame(data_rows)

# 'Date'를 첫 번째 컬럼으로, 나머지 퍼센트 컬럼을 0~100 순으로 정렬
columns_order = ['Date'] + list(percent_range)
df = df.reindex(columns=columns_order)

# CSV로 저장
os.makedirs(os.path.dirname(save_file_path), exist_ok=True)
df.to_csv(save_file_path, index=False)

print(f"CSV 파일이 성공적으로 저장되었습니다: {save_file_path}")
