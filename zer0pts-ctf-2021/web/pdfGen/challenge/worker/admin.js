const puppeteer = require('puppeteer');
const Redis = require('ioredis');
const connection = new Redis(6379, 'redis');

const browser_option = {
  args: [
    '-wait-for-browser'
  ]
}

let browser = undefined;

const init = async () => {
  const browser = await puppeteer.connect({
    browserWSEndpoint:  'ws://headful:5678/chrome?args=--window-size=1920,1080'
  });
  return browser;
};

const crawl = async (url) => {
  console.log(`[+] Crawling started: ${url}`);

  try {
    const page = await browser.newPage();
    
    await page.goto(url, {
      waitUntil: 'networkidle0',
      timeout: 3 * 1000,
    });
    await page.close();
  } catch (e) {
    console.log('[-] ERROR');
    console.log('[-]', e);
  }

  console.log(`[+] Crawling finished: ${url}`);
};

const handle = () => {
  console.log('[+] handle');
  connection.blpop('url', 0, async (err, message) => {
    browser = await init();
    await crawl( message[1]);
    setTimeout(handle, 10);
  });
};

handle();
