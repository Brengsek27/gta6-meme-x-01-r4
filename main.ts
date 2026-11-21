import * as fs from 'fs';
import * as path from 'path';

const botDir = process.env.MAKEFUN_BOT_DIR || '/bot';
const outDir = process.env.MAKEFUN_OUTPUT_DIR || '/output';

// Ensure output directory exists
fs.mkdirSync(outDir, { recursive: true });

const src = path.join(botDir, 'POST.json');
const dest = path.join(outDir, 'POST.json');
fs.copyFileSync(src, dest);

try {
  const data = fs.readFileSync(dest, 'utf-8');
  const obj = JSON.parse(data);
  const url: string = obj.url;
  const xPattern = /^https:\/\/((x|twitter)\.com)\/[^\/]+\/status\/\d+$/;
  if (xPattern.test(url)) {
    console.log(`Recorded post URL: ${url}`);
  } else {
    console.warn('Warning: URL does not look like an X/Twitter post address');
  }
} catch (err) {
  console.error((err as Error).message);
  process.exit(1);
}
