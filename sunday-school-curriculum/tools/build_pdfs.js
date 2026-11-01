// Builds a PDF next to every .md file (README, 00-start-here/, phases/) and every printable
// worksheet (printables/*.html), then combines them into two email-ready files in SHARE-PDF/.
// The .md and .html source files are kept.
// Usage (from the repo root):  node sunday-school-curriculum/tools/build_pdfs.js
// Requires: pandoc, and Playwright with Chromium.
const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const DIRS = ['.', '00-start-here', 'phases'];
const START_HERE_ORDER = ['program-overview', 'teacher-training-guide', 'weekly-session-template',
  'books-of-the-bible-memory-system', 'game-library', 'youtube-video-guide', 'supply-list', 'parent-welcome-letter'];
const SHARE = path.join(ROOT, 'SHARE-PDF');

const CSS = `
@page { size: Letter; margin: 0.6in 0.6in 0.7in; }
body { font-family: "Segoe UI", "DejaVu Sans", Arial, "Noto Color Emoji", sans-serif; font-size: 10.5pt; line-height: 1.45; color: #1a1a1a; }
h1 { font-size: 22pt; color: #3b2a7a; border-bottom: 3px solid #3b2a7a; padding-bottom: 4px; margin-top: 0; }
h2 { font-size: 15pt; color: #3b2a7a; border-bottom: 1px solid #ccc; padding-bottom: 2px; margin-top: 22px; break-after: avoid; }
h3 { font-size: 12.5pt; color: #5a3fa8; break-after: avoid; }
h4, h5 { font-size: 11pt; break-after: avoid; }
table { border-collapse: collapse; width: 100%; margin: 8px 0; font-size: 9.5pt; }
th, td { border: 1px solid #bbb; padding: 4px 6px; vertical-align: top; text-align: left; }
th { background: #ece8f7; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
tr { break-inside: avoid; }
blockquote { border-left: 4px solid #b9a8e6; margin: 8px 0; padding: 4px 12px; background: #f7f5fc; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
code, pre { font-family: Consolas, "DejaVu Sans Mono", monospace; font-size: 9pt; }
pre { background: #f4f4f4; padding: 8px; white-space: pre-wrap; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
a { color: #3b2a7a; }
ul.task-list { list-style: none; padding-left: 1em; }
hr { border: 0; border-top: 1px solid #ddd; }
`;

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  let count = 0;
  for (const dir of DIRS) {
    const abs = path.join(ROOT, dir);
    for (const f of fs.readdirSync(abs).filter(f => f.endsWith('.md')).sort()) {
      const md = path.join(abs, f);
      let body = execFileSync('pandoc', [md, '-f', 'gfm', '-t', 'html5'], { encoding: 'utf8' });
      body = body.replace(/href="([^"#:]+)\.(md|html)(#[^"]*)?"/g, 'href="$1.pdf$3"'); // link to sibling PDFs
      const title = f.replace(/\.md$/, '');
      const html = `<!doctype html><html><head><meta charset="utf-8"><title>${title}</title><style>${CSS}</style></head><body>${body}</body></html>`;
      await page.setContent(html, { waitUntil: 'load' });
      await page.pdf({
        path: md.replace(/\.md$/, '.pdf'), format: 'Letter', printBackground: true,
        displayHeaderFooter: true, headerTemplate: '<div></div>',
        footerTemplate: '<div style="font-size:8px;width:100%;text-align:center;color:#777">Purpose Church Kids · Through the Bible in 12 Months · Page <span class="pageNumber"></span> of <span class="totalPages"></span></div>',
        margin: { top: '0.6in', bottom: '0.7in', left: '0.6in', right: '0.6in' },
      });
      count++;
      console.log('wrote', path.join(dir, f.replace(/\.md$/, '.pdf')));
    }
  }

  // Printable worksheets: use each sheet's own print CSS (Letter, one worksheet per page).
  const pr = path.join(ROOT, 'printables');
  for (const f of fs.readdirSync(pr).filter(f => f.endsWith('.html') && f !== 'index.html').sort()) {
    await page.goto('file://' + path.join(pr, f), { waitUntil: 'load' });
    await page.pdf({ path: path.join(pr, f.replace(/\.html$/, '.pdf')), format: 'Letter', printBackground: true, preferCSSPageSize: true });
    count++;
    console.log('wrote', path.join('printables', f.replace(/\.html$/, '.pdf')));
  }
  await browser.close();

  // Combined, email-ready files.
  fs.mkdirSync(SHARE, { recursive: true });
  const guide = [path.join(ROOT, 'README.pdf'),
    ...START_HERE_ORDER.map(n => path.join(ROOT, '00-start-here', n + '.pdf')),
    ...fs.readdirSync(path.join(ROOT, 'phases')).filter(f => f.endsWith('.pdf')).sort().map(f => path.join(ROOT, 'phases', f))];
  const prints = [...fs.readdirSync(pr).filter(f => /^phase-\d+-printables\.pdf$/.test(f)).sort().map(f => path.join(pr, f)),
    path.join(pr, 'bible-passport.pdf'), path.join(pr, 'certificate.pdf')];
  execFileSync('pdfunite', [...guide, path.join(SHARE, '1 - Teacher Guide - Through the Bible in 12 Months.pdf')]);
  execFileSync('pdfunite', [...prints, path.join(SHARE, '2 - Printables - Coloring, Puzzles, Flashcards, Passport.pdf')]);
  console.log(count, 'PDFs + 2 combined files in SHARE-PDF/');
})();
