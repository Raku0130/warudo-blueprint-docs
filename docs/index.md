# Warudo Blueprint Spec (Unofficial)

これは Warudo の Blueprint ノード仕様をコミュニティで整理・公開するためのドキュメント雛形です。

- 収録形式: YAML（`/data/nodes/**.yaml`）
- 生成: `scripts/gen_nodes.py` → Markdown（`/docs/nodes/**.md`）
- バリデーション: `scripts/validate.py`（JSON Schema）

ローカルプレビュー:  
```
pip install -r requirements.txt # 既に導入済みなら不要
python scripts/validate.py
python scripts/gen_nodes.py
mkdocs serve
```

