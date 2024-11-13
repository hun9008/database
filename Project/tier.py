import csv

# 데이터 정의
data = [
    ["tier", "max_copies"],
    ["Gold", 10],
    ["Silver", 5],
    ["Bronze", 3],
    ["Iron", 0]
]

# TSV 파일 생성
with open('tier.tsv', 'w', newline='') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerows(data)