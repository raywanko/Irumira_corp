# 株式会社イルミラ コーポレートサイト

## 📸 画像の設定方法

### ヒーロー画像（トップページ背景）
1. 画像を用意（推奨サイズ: 横1920px × 縦1080px以上）
2. ファイル名を `hero-bg.jpg` に変更
3. 以下の場所に配置:
   ```
   main/static/images/hero/hero-bg.jpg
   ```

### ロゴ画像
1. ロゴ画像を用意（推奨: PNG形式、透過背景）
2. ファイル名を `logo.png` に変更
3. 以下の場所に配置:
   ```
   main/static/images/logo.png
   ```

### 社長の写真
1. 社長の写真を用意
2. ファイル名を `president.jpg` に変更
3. 以下の場所に配置:
   ```
   main/static/images/president.jpg
   ```
4. `main/templates/main/message.html` の該当箇所を修正:
   ```html
   <div class="president-image">
       <img src="{% static 'images/president.jpg' %}" alt="代表取締役社長">
   </div>
   ```

## 🗺️ Googleマップの設定方法

### ステップ1: Googleマップで場所を検索
1. [Google Maps](https://www.google.com/maps) を開く
2. 会社の住所を検索: `愛知県名古屋市中区錦3-19-20`

### ステップ2: 埋め込みコードを取得
1. 検索結果で「共有」ボタンをクリック
2. 「地図を埋め込む」タブを選択
3. サイズを選択（中または大推奨）
4. 表示されたHTMLコードをコピー

### ステップ3: サイトに埋め込む
1. `main/templates/main/index.html` を開く
2. 以下の部分を探す:
   ```html
   <iframe 
       src="ここにGoogleマップのURLを貼り付け"
       class="google-map-iframe"
       ...
   </iframe>
   ```
3. `src="..."` の中身を、コピーしたコードの `src` 属性の値に置き換える

### 例:
```html
<iframe 
    src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d..."
    class="google-map-iframe"
    allowfullscreen="" 
    loading="lazy" 
    referrerpolicy="no-referrer-when-downgrade"
    title="株式会社イルミラの地図">
</iframe>
```

## 🚀 セットアップ手順

1. プロジェクトフォルダへ移動:
   ```bash
   cd iurmira_corp
   ```

2. 仮想環境の作成:
   ```bash
   python -m venv venv
   ```

3. 仮想環境の有効化:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

4. Djangoのインストール:
   ```bash
   pip install django
   ```

5. データベースの初期化:
   ```bash
   python manage.py migrate
   ```

6. 開発サーバーの起動:
   ```bash
   python manage.py runserver
   ```

7. ブラウザで確認:
   ```
   http://127.0.0.1:8000/
   ```

## 📱 モバイル対応

このサイトは完全にモバイル対応しています。スマートフォンやタブレットでも快適に閲覧できます。

### 確認方法
1. 開発サーバーを起動
2. スマートフォンで同じWi-Fiに接続
3. ブラウザで `http://[PCのIPアドレス]:8000/` にアクセス

または、PCのブラウザで開発者ツール（F12）を開き、デバイスツールバー（Ctrl+Shift+M）でモバイル表示を確認できます。

## 📁 ファイル構造

```
iurmira_corp/
├── main/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── script.js
│   │   └── images/
│   │       ├── hero/
│   │       │   └── hero-bg.jpg  ← ヒーロー画像をここに
│   │       ├── logo.png         ← ロゴをここに
│   │       └── president.jpg    ← 社長写真をここに
│   └── templates/
│       └── main/
│           ├── index.html       ← トップページ
│           ├── message.html     ← 社長挨拶
│           └── ...
└── manage.py
```

## 🎨 カスタマイズ

### 色の変更
`main/static/css/style.css` でメインカラーを変更できます:
```css
/* 現在: 青緑グラデーション */
background: linear-gradient(135deg, #00f5ff, #00ff88);

/* 変更例: 赤紫グラデーション */
background: linear-gradient(135deg, #ff6b6b, #ee5a6f);
```

## 📞 サポート

質問や問題がある場合は、システム管理者にお問い合わせください。
