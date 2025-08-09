import spacy
import sys
import os
import pandas as pd
from collections import Counter

if len(sys.argv) != 3:
    print("Usage: python count_lemmas_progress.py <input_dir> <output_csv>")
    sys.exit(1)

input_dir = sys.argv[1]
output_csv = sys.argv[2]


nlp = spacy.load("en_core_web_sm")
#限定詞、前置詞、等位接続詞、従位接続詞、代名詞、助詞、助動詞という機能語を除外
FUNCTION_POS = {'DET', 'ADP', 'CCONJ', 'SCONJ', 'PRON', 'PART', 'AUX'}

freq = Counter()
files = [f for f in os.listdir(input_dir) if f.endswith(".txt")]
total_files = len(files)

for file_idx, file_name in enumerate(files, start=1):
    file_path = os.path.join(input_dir, file_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    text_len = len(text)
    print(f"[{file_idx}/{total_files}] Processing {file_name} ({text_len:,} chars)")

    # 10万文字ずつ処理
    for chunk_idx, start in enumerate(range(0, text_len, 100000), start=1):
        chunk = text[start:start+100000]
        doc = nlp(chunk)
        lemmas = [
            token.lemma_.lower()
            for token in doc
            if not token.is_stop
            and token.pos_ not in FUNCTION_POS
            and token.is_alpha
        ]
        freq.update(lemmas)
        print(f" Chunk {chunk_idx} processed ({len(chunk):,} chars)")

    print(f" Done: {file_name}")

# 上位50語をCSVに
df = pd.DataFrame(freq.items(), columns=["lemma", "count"])
df = df.sort_values("count", ascending=False).head(50)
df.to_csv(output_csv, index=False, encoding='utf-8')

print(f"\n Top 50 lemmas saved to {output_csv}")
