#!/usr/bin/env bash
set -o errexit

# 依存関係をインストール
pip install -r requirements.txt

# 環境変数を設定
export DJANGO_SETTINGS_MODULE=iurmira_corp.settings

# 静的ファイルを収集
python manage.py collectstatic --no-input --clear

# マイグレーション
python manage.py migrate --no-input