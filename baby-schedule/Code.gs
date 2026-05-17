// ===================================================
// 赤ちゃんスケジュール通知 - Google Apps Script
// ===================================================
// 【編集ポイント】ここを変えるだけでカスタマイズできます

const CONFIG = {
  // 買い物の曜日 (0=日, 1=月, 2=火, 3=水, 4=木, 5=金, 6=土)
  SHOPPING_DAYS: [1, 4], // 月・木

  // 授乳時間リスト（3時間おき）
  FEEDING_HOURS: [7, 10, 13, 16, 19, 22, 1, 4],
};

// ===================================================
// メイン関数（毎時自動実行）
// ===================================================
function sendScheduledNotifications() {
  const now = new Date();
  const hour = now.getHours();
  const minute = now.getMinutes();
  const day = now.getDay(); // 0=日〜6=土

  // 毎時0〜9分の間にのみ実行（重複送信防止）
  if (minute >= 10) return;

  getMessages(hour, day).forEach(msg => sendSlack(msg));
}

function getMessages(hour, day) {
  const msgs = [];

  // 授乳リマインダー
  if (CONFIG.FEEDING_HOURS.includes(hour)) {
    msgs.push(`🍼 *授乳の時間です！* (${hour}:00)\n前回から3時間経ちました。`);
  }

  // 時間別タスク
  const tasks = {
    7:  ['🌅 *おはようございます！*\n今日も3人で頑張りましょう！'],
    8:  [
          '🍳 *【パパ】朝食の準備をお願いします！*',
          '🗑️ *【パパ】ゴミ出しをお願いします！*',
        ],
    9:  ['👔 *【パパ】洗濯物を干してください！*'],
    13: ['🍱 *昼食の時間です！*'],
    14: ['😴 *【ママ】昼寝タイムです！*\nパパが娘ちゃんを担当します。ゆっくり休んでね。'],
    17: ['🍽️ *【パパ】夕食の準備をお願いします！*'],
    19: ['🍽️ *夕食の時間です！*'],
    20: ['🛁 *【パパ】娘ちゃんのお風呂タイムです！*'],
    22: ['🌙 *就寝準備を始めましょう。*'],
    0:  ['💤 *お疲れ様でした！おやすみなさい。*\n深夜の授乳があります。無理せず2人で交代で！'],
  };

  // 買い物リマインダー（設定曜日のみ）
  if (CONFIG.SHOPPING_DAYS.includes(day) && hour === 11) {
    msgs.push('🛒 *買い物の日です！*\nスーパーへ行きましょう。買い物リストを確認してね。');
  }

  if (tasks[hour]) {
    msgs.push(...tasks[hour]);
  }

  return msgs;
}

// ===================================================
// Slack送信
// ===================================================
function sendSlack(text) {
  const url = PropertiesService.getScriptProperties().getProperty('SLACK_WEBHOOK_URL');

  if (!url) {
    Logger.log('⚠️ SLACK_WEBHOOK_URLが未設定です。スクリプトプロパティに設定してください。');
    return;
  }

  UrlFetchApp.fetch(url, {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify({ text: text }),
    muteHttpExceptions: true,
  });
}

// ===================================================
// セットアップ（初回だけ手動で実行してください）
// ===================================================
function setupTrigger() {
  // 既存トリガーをリセット
  ScriptApp.getProjectTriggers().forEach(t => ScriptApp.deleteTrigger(t));

  // 毎時実行トリガーを設定
  ScriptApp.newTrigger('sendScheduledNotifications')
    .timeBased()
    .everyHours(1)
    .create();

  Logger.log('✅ トリガー設定完了！毎時間チェックが始まります。');
}

// ===================================================
// テスト送信（動作確認用）
// ===================================================
function testSend() {
  sendSlack('✅ *テスト送信成功！*\nスケジュール通知の準備ができました！🎉');
}
