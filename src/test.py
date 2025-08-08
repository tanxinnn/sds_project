# BERTを使った文のトークン化とベクトル化の例
sentences = ["The government announced new regulations on the environment. "
,"Many industries opposed the new law."]

from transformers import BertTokenizer

# BERTのトークナイザー（uncasedかcasedは選択に応じて）
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# 1文だけ例として処理
sentence = sentences[0]
encoded = tokenizer(sentence, return_tensors='pt')

print("Tokens:", tokenizer.convert_ids_to_tokens(encoded['input_ids'][0]))
print("Input IDs:", encoded['input_ids'])
print("Attention Mask:", encoded['attention_mask'])

import torch
from transformers import BertModel

# BERTモデル（出力にhidden statesを含める）
model = BertModel.from_pretrained('bert-base-uncased', output_hidden_states=True)
model.eval()  # 推論モード（Dropout無効）

with torch.no_grad():  # 勾配不要
    outputs = model(**encoded)
    hidden_states = outputs.hidden_states  # 13個（embedding層 + 12層）

# 各層の出力： [13 (層数), batch_size, seq_len, hidden_dim]
print(f"Total Layers: {len(hidden_states)}")
print(f"Shape of last layer: {hidden_states[-1].shape}")  # [1, seq_len, 768]

# 最終層のトークンベクトルを取り出す（バッチ次元を削除）
token_embeddings = hidden_states[-1][0]  # shape: [seq_len, hidden_dim]

# 特定のトークン（例：'government'）のベクトルを見る
tokens = tokenizer.convert_ids_to_tokens(encoded['input_ids'][0])
for idx, token in enumerate(tokens):
    if token == "government":
        print(f"Embedding for 'government': {token_embeddings[idx]}")

'''Tokens: ['[CLS]', 'the', 'government', 'announced', 'new', 'regulations', 'on', 'the', 'environment', '.', '[SEP]']
Input IDs: tensor([[ 101, 1996, 2231, 2623, 2047, 7040, 2006, 1996, 4044, 1012,  102]])
Attention Mask: tensor([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
Total Layers: 13
Shape of last layer: torch.Size([1, 11, 768])
Embedding for 'government': tensor([-5.0079e-01, -6.0758e-01, -2.8713e-02,  7.5617e-02, -2.2288e-01,...])'''