import { execSync } from "child_process";
import { readFileSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const words = JSON.parse(
  readFileSync(join(__dirname, "../src/content/ng-words.json"), "utf-8")
);

console.log(`🎬 Rendering ${words.length} videos...\n`);

for (const word of words) {
  const id = word.id.toString().padStart(2, "0");
  const compositionId = `kyujinhyo-${id}`;
  const output = `out/${compositionId}.mp4`;

  console.log(`▶ [${id}/${words.length}] ${word.phrase}`);
  try {
    execSync(
      `npx remotion render ${compositionId} ${output} --log=error`,
      { stdio: "inherit", cwd: join(__dirname, "..") }
    );
    console.log(`  ✅ ${output}\n`);
  } catch {
    console.error(`  ❌ Failed: ${compositionId}\n`);
  }
}

console.log("🏁 All done!");
