# fastapi-authenticated

FastAPI の JWT 認証の試し

## 準備

```bash
> poetry install
> pre-commit install
```

## alembic

```bash
# migration scriptの作成
> poetry run alembic revision --autogenerate -m "create table"
# migrationの適用
> poetry run alembic upgrade head
# 一つ前に戻す
> alembic downgrade -1
```

## sqlite

```bash
# sqliteに接続(テスト用はtest.db)
sqlite3 app.db
```
