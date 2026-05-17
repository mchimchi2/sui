# 赤ちゃんスケジュール通知 セットアップ手順

## 全体の流れ（合計約20分）

```
Step 1: Slackワークスペース作成（5分）
Step 2: Incoming Webhook URL取得（5分）
Step 3: Google Apps Scriptにコードを貼り付け（5分）
Step 4: Webhook URLを登録してテスト送信（5分）
```

---

## Step 1: Slackセットアップ

1. https://slack.com/intl/ja-jp/ にアクセスして「無料で試す」
2. ワークスペース名を決める（例：`our-family`）
3. チャンネル名を決める（例：`#baby-schedule`）
4. 夫婦2人だけをメンバーにする
5. スマホにもSlackアプリをインストールして通知をONにする

---

## Step 2: Incoming Webhook URLを取得

1. https://api.slack.com/apps にアクセス
2. 「Create New App」→「From scratch」
3. App Name: `BabyScheduleBot`、ワークスペースを選択して「Create」
4. 左メニュー「Incoming Webhooks」→ トグルをONにする
5. 「Add New Webhook to Workspace」→ `#baby-schedule` チャンネルを選択
6. 表示された `https://hooks.slack.com/services/...` のURLをコピー

---

## Step 3: Google Apps Scriptにコードを貼り付け

1. https://script.google.com にアクセス（Googleアカウントでログイン）
2. 「新しいプロジェクト」をクリック
3. プロジェクト名を `BabySchedule` に変更
4. デフォルトのコードをすべて削除
5. このリポジトリの `Code.gs` の中身をすべてコピー＆ペースト
6. 保存（Ctrl+S）

---

## Step 4: Webhook URLを登録してテスト

1. GASエディタの上部メニュー「プロジェクトの設定」（歯車アイコン）
2. 「スクリプトプロパティ」→「プロパティを追加」
3. プロパティ名: `SLACK_WEBHOOK_URL`
4. 値: Step 2でコピーしたWebhook URL
5. 「保存」

### テスト送信
1. GASエディタで関数を `testSend` に切り替えて「実行」
2. Slackに「✅ テスト送信成功！」が届けばOK

### トリガー設定（本番稼働）
1. 関数を `setupTrigger` に切り替えて「実行」
2. 「承認が必要です」と出たら許可する
3. 完了！毎時間自動でチェックが走ります

---

## スケジュールの編集方法

`Code.gs` の上部の `CONFIG` を変えるだけです：

```javascript
const CONFIG = {
  SHOPPING_DAYS: [1, 4],        // 月・木 → 例えば火・金にするなら [2, 5]
  FEEDING_HOURS: [7, 10, 13, 16, 19, 22, 1, 4], // 授乳時間
};
```

時間別のメッセージも `tasks` オブジェクトで自由に追加・削除できます。
