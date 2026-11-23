import { copyFile, mkdir } from "node:fs/promises";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

try {
  await mkdir(outputDir, { recursive: true });
  await copyFile(join(botDir, "POST.json"), join(outputDir, "POST.json"));
} catch (err) {
  const message = err instanceof Error ? err.message : String(err);
  console.error(`failed to copy POST.json: ${message}`);
  process.exit(1);
}
