// =====================================================================
// 大手電力10社 電力単価マスタデータ
// ---------------------------------------------------------------------
// 【毎月の更新手順】
//  1. 各社の燃料費調整単価(毎月改定)を fuelAdjustment に入力し、
//     fuelAdjustmentMonth を対象月に変更する
//  2. 基本料金・電力量料金の改定があった行は該当単価を修正する
//  3. 更新した行の updated を更新日(YYYY-MM-DD)に変更する
//  4. 再エネ賦課金は毎年5月に全社一律で改定 → renewableLevy を更新
//
//  ※ ブラウザの編集モードから修正して「JSONエクスポート」でも可。
//  ※ 単価はすべて税込・円。
//  ※ 初期値は構築時点の参考値です。必ず各社公式ページ(sourceUrl)で
//     確認のうえ更新してください。
// =====================================================================

const RATE_DATA = {
  // 再生可能エネルギー発電促進賦課金(全社共通・円/kWh・毎年5月改定)
  renewableLevy: {
    price: 3.98,
    fiscalYear: "2025年度",
    updated: "2025-05-01",
    note: "毎年5月に経済産業省が改定を公表",
  },

  // 急速充電器は高圧受電が基本のため、各社の高圧標準プランを掲載。
  // 低圧(50kW未満の充電器等)のプランを追加する場合は行を追加してください。
  companies: [
    {
      company: "北海道電力",
      plan: "高圧電力",
      voltage: "高圧",
      basicRate: 2266.0,        // 基本料金 円/kW・月
      energyRateSummer: 17.53,  // 電力量料金 夏季(7〜9月) 円/kWh
      energyRateOther: 16.02,   // 電力量料金 その他季 円/kWh
      fuelAdjustment: null,     // 燃料費調整単価 円/kWh(毎月更新・要入力)
      fuelAdjustmentMonth: "",
      sourceUrl: "https://www.hepco.co.jp/business/business/price_plan/",
      updated: "2026-07-09",
      note: "参考値・要確認",
    },
    {
      company: "東北電力",
      plan: "高圧電力",
      voltage: "高圧",
      basicRate: 1980.0,
      energyRateSummer: 17.05,
      energyRateOther: 15.84,
      fuelAdjustment: null,
      fuelAdjustmentMonth: "",
      sourceUrl: "https://www.tohoku-epco.co.jp/pricemenu/biz/",
      updated: "2026-07-09",
      note: "参考値・要確認",
    },
    {
      company: "東京電力エナジーパートナー",
      plan: "業務用電力(高圧)",
      voltage: "高圧",
      basicRate: 2038.3,
      energyRateSummer: 17.37,
      energyRateOther: 16.31,
      fuelAdjustment: null,
      fuelAdjustmentMonth: "",
      sourceUrl: "https://www.tepco.co.jp/ep/corporate/plan_h/",
      updated: "2026-07-09",
      note: "参考値・要確認",
    },
    {
      company: "中部電力ミライズ",
      plan: "高圧電力",
      voltage: "高圧",
      basicRate: 1870.0,
      energyRateSummer: 16.91,
      energyRateOther: 15.80,
      fuelAdjustment: null,
      fuelAdjustmentMonth: "",
      sourceUrl: "https://miraiz.chuden.co.jp/business/electrify/",
      updated: "2026-07-09",
      note: "参考値・要確認",
    },
    {
      company: "北陸電力",
      plan: "高圧電力",
      voltage: "高圧",
      basicRate: 1760.0,
      energyRateSummer: 15.52,
      energyRateOther: 14.41,
      fuelAdjustment: null,
      fuelAdjustmentMonth: "",
      sourceUrl: "https://www.rikuden.co.jp/kaisha_ryokin/",
      updated: "2026-07-09",
      note: "参考値・要確認",
    },
    {
      company: "関西電力",
      plan: "高圧電力AS",
      voltage: "高圧",
      basicRate: 2090.0,
      energyRateSummer: 16.54,
      energyRateOther: 15.43,
      fuelAdjustment: null,
      fuelAdjustmentMonth: "",
      sourceUrl: "https://kepco.jp/corporate/ryokin/",
      updated: "2026-07-09",
      note: "参考値・要確認",
    },
    {
      company: "中国電力",
      plan: "高圧電力",
      voltage: "高圧",
      basicRate: 1925.0,
      energyRateSummer: 17.16,
      energyRateOther: 16.05,
      fuelAdjustment: null,
      fuelAdjustmentMonth: "",
      sourceUrl: "https://www.energia.co.jp/biz/",
      updated: "2026-07-09",
      note: "参考値・要確認",
    },
    {
      company: "四国電力",
      plan: "高圧電力",
      voltage: "高圧",
      basicRate: 1870.0,
      energyRateSummer: 16.82,
      energyRateOther: 15.71,
      fuelAdjustment: null,
      fuelAdjustmentMonth: "",
      sourceUrl: "https://www.yonden.co.jp/business/",
      updated: "2026-07-09",
      note: "参考値・要確認",
    },
    {
      company: "九州電力",
      plan: "高圧電力",
      voltage: "高圧",
      basicRate: 1760.0,
      energyRateSummer: 15.91,
      energyRateOther: 14.80,
      fuelAdjustment: null,
      fuelAdjustmentMonth: "",
      sourceUrl: "https://www.kyuden.co.jp/business_index.html",
      updated: "2026-07-09",
      note: "参考値・要確認",
    },
    {
      company: "沖縄電力",
      plan: "業務用電力(高圧)",
      voltage: "高圧",
      basicRate: 1980.0,
      energyRateSummer: 19.02,
      energyRateOther: 19.02,
      fuelAdjustment: null,
      fuelAdjustmentMonth: "",
      sourceUrl: "https://www.okiden.co.jp/business-support/",
      updated: "2026-07-09",
      note: "参考値・要確認(夏季区分なし)",
    },
  ],
};
