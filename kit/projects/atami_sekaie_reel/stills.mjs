// 絵コンテ静止画: stills/s1..s8.png と sheet.png を作る
// 使い方: npm i playwright && node stills.mjs
import { chromium } from "playwright";
import { fileURLToPath } from "url";
import path from "path";
import fs from "fs";
const here = path.dirname(fileURLToPath(import.meta.url));
fs.mkdirSync(path.join(here, "stills"), { recursive: true });
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
const ids = ["s1","s2","s3","s4","s5","s6","s7","s8"];
for (const s of ids) {
  await page.goto("file://" + path.join(here, "storyboard.html") + "?s=" + s);
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: path.join(here, "stills", s + ".png") });
}
// 一覧(4×2)
const imgs = ids.map(s => "data:image/png;base64," + fs.readFileSync(path.join(here, "stills", s + ".png")).toString("base64"));
await page.setViewportSize({ width: 4 * 380 + 100, height: 2 * 675 + 60 });
await page.setContent(`<body style="margin:0;background:#222;display:grid;grid-template-columns:repeat(4,380px);gap:20px;padding:20px">${imgs.map(u=>`<img src="${u}" style="width:380px;height:675px">`).join("")}</body>`);
await page.screenshot({ path: path.join(here, "sheet.png") });
await browser.close();
console.log("✓ stills/ と sheet.png");
