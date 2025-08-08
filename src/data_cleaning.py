import re
import sys
import os

if len(sys.argv) != 3:
    print("Usage: python clean_texts_regex_v2.py <input_dir> <output_dir>")
    sys.exit(1)

input_dir = sys.argv[1]
output_dir = sys.argv[2]
os.makedirs(output_dir, exist_ok=True)

# 文の区切り記号（句点・疑問符・感嘆符など）
SENT_SPLIT_PATTERN = re.compile(r'(?<=[。．！？!?\.])\s+')

for file_name in os.listdir(input_dir):
    if not file_name.endswith(".txt"):
        continue

    input_path = os.path.join(input_dir, file_name)
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    cleaned_lines = []

    for line in lines:
        # ステップ1: 行頭の @@数字 を削除、行末空白を削除（改行は維持しない）
        line = re.sub(r'^@@\d+\s*', '', line).rstrip()

        # ステップ2: 文単位に分割
        sentences = SENT_SPLIT_PATTERN.split(line)

        # ステップ3: 文ごとのフィルタリング
        filtered_sents = []
        for sent in sentences:
            sent = sent.strip()
            if '@' in sent:
                continue  # @を含む文は削除
            sent = sent.replace('<p>', '')  # <p> は削除（文自体は残す）
            filtered_sents.append(sent)

        # ステップ4: フィルタ済みの文をスペースで結合して1行に戻す
        cleaned_line = ' '.join(filtered_sents)
        cleaned_lines.append(cleaned_line)

    # ステップ5: 改行を保持して出力ファイルに書き出し
    cleaned_text = '\n'.join(cleaned_lines)

    # ファイル名に _cleaned を追加
    base, ext = os.path.splitext(file_name)
    output_file_name = f"{base}_cleaned{ext}"
    output_path = os.path.join(output_dir, output_file_name)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_text)

    print(f"Cleaned: {file_name} → {output_file_name}")