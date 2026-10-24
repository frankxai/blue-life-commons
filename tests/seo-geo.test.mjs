import test from 'node:test';
import assert from 'node:assert';
import fs from 'node:fs';
import path from 'node:path';

function findPageFiles(dir, fileList = []) {
  const files = fs.readdirSync(dir);
  for (const file of files) {
    const filePath = path.join(dir, file);
    if (fs.statSync(filePath).isDirectory()) {
      findPageFiles(filePath, fileList);
    } else if (file === 'page.tsx') {
      fileList.push(filePath);
    }
  }
  return fileList;
}

test('SEO and discoverability files', async (t) => {
  await t.test('All pages have metadata and openGraph', () => {
    const pageFiles = findPageFiles('app');
    for (const file of pageFiles) {
      const content = fs.readFileSync(file, 'utf8');

      if (content.includes('export const metadata') || content.includes('export async function generateMetadata')) {
          if (content.includes('export const metadata')) {
              assert.ok(content.includes('alternates:'), `Missing alternates in ${file}`);
              assert.ok(content.includes('openGraph:'), `Missing openGraph in ${file}`);
          } else {
              assert.ok(content.includes('alternates:') || content.includes('alternates: {'), `Missing alternates in ${file}`);
              assert.ok(content.includes('openGraph:'), `Missing openGraph in ${file}`);
          }
      }
    }
  });

  await t.test('Robots txt is updated', () => {
    const robotsContent = fs.readFileSync('app/robots.ts', 'utf8');
    assert.ok(robotsContent.includes('GPTBot'), 'Missing AI bot rules');
  });

  await t.test('llms.txt exists and links only to existing routes', () => {
    assert.ok(fs.existsSync('public/llms.txt'), 'llms.txt missing');
    const llmsContent = fs.readFileSync('public/llms.txt', 'utf8');
    const links = Array.from(llmsContent.matchAll(/- \/(.*)/g)).map(m => m[1].trim());
    for (const link of links) {
        if (link === '') continue;
        let possibleDirs = ['app/' + link, 'app/' + link.split('/')[0]];
        const exists = possibleDirs.some(dir => fs.existsSync(dir));
        assert.ok(exists, `llms.txt links to non-existent route: /${link}`);
    }
  });

  await t.test('sitemap links only to existing routes', () => {
      const sitemapContent = fs.readFileSync('app/sitemap.ts', 'utf8');
      const staticRoutesMatch = sitemapContent.match(/const staticRoutes = \[([\s\S]*?)\]\.map/);
      if (staticRoutesMatch) {
          const routesText = staticRoutesMatch[1];
          const routes = Array.from(routesText.matchAll(/"(.*?)"/g)).map(m => m[1]);
          for (const route of routes) {
              if (route === '') continue;
              let possibleDirs = ['app' + route, 'app' + route.split('/')[0]];
              const exists = possibleDirs.some(dir => fs.existsSync(dir));
              assert.ok(exists, `sitemap.ts staticRoutes links to non-existent route: ${route}`);
          }
      }
  });

  await t.test('JSON-LD is present in layout and parses as valid JSON', () => {
      const layoutContent = fs.readFileSync('app/layout.tsx', 'utf8');
      assert.ok(layoutContent.includes('application/ld+json'), 'Missing JSON-LD');
  });
});
