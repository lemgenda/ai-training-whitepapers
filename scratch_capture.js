const http = require('http');
const fs = require('fs');
const path = require('path');
const net = require('net');
const crypto = require('crypto');

function createWebSocket(wsUrl) {
  return new Promise((resolve, reject) => {
    const url = new URL(wsUrl);
    const host = url.hostname;
    const port = url.port || 80;
    const pathName = url.pathname;

    const socket = net.createConnection(port, host);
    const secKey = crypto.randomBytes(16).toString('base64');

    socket.on('connect', () => {
      const headers = [
        `GET ${pathName} HTTP/1.1`,
        `Host: ${host}:${port}`,
        'Upgrade: websocket',
        'Connection: Upgrade',
        `Sec-WebSocket-Key: ${secKey}`,
        'Sec-WebSocket-Version: 13',
        '\r\n'
      ].join('\r\n');
      socket.write(headers);
    });

    let buffer = Buffer.alloc(0);
    let upgraded = false;
    let messageId = 1;
    const callbacks = new Map();

    socket.on('data', (chunk) => {
      buffer = Buffer.concat([buffer, chunk]);
      if (!upgraded) {
        const headerEnd = buffer.indexOf('\r\n\r\n');
        if (headerEnd !== -1) {
          const headersStr = buffer.slice(0, headerEnd).toString();
          if (headersStr.includes('101 Switching Protocols') || headersStr.includes('101 WebSocket Protocol Handshake') || headersStr.includes('101 ')) {
            upgraded = true;
            buffer = buffer.slice(headerEnd + 4);
          } else {
            return reject(new Error('Upgrade failed: ' + headersStr));
          }
        }
      }

      while (upgraded && buffer.length >= 2) {
        const byte0 = buffer[0];
        const byte1 = buffer[1];
        const opcode = byte0 & 0x0f;
        let payloadLen = byte1 & 0x7f;
        let offset = 2;

        if (payloadLen === 126) {
          if (buffer.length < 4) break;
          payloadLen = buffer.readUInt16BE(2);
          offset = 4;
        } else if (payloadLen === 127) {
          if (buffer.length < 10) break;
          payloadLen = Number(buffer.readBigUInt64BE(2));
          offset = 10;
        }

        if (buffer.length < offset + payloadLen) break;

        const payload = buffer.slice(offset, offset + payloadLen);
        buffer = buffer.slice(offset + payloadLen);

        if (opcode === 1) { // Text frame
          try {
            const msg = JSON.parse(payload.toString('utf8'));
            if (msg.id && callbacks.has(msg.id)) {
              callbacks.get(msg.id)(msg);
              callbacks.delete(msg.id);
            }
          } catch (e) {}
        }
      }
    });

    socket.on('error', reject);

    function send(method, params = {}) {
      return new Promise((res, rej) => {
        const id = messageId++;
        callbacks.set(id, (msg) => {
          if (msg.error) rej(msg.error);
          else res(msg.result);
        });
        const json = JSON.stringify({ id, method, params });
        const len = Buffer.byteLength(json);

        const maskKey = crypto.randomBytes(4);
        let header;
        if (len < 126) {
          header = Buffer.alloc(6);
          header[0] = 0x81;
          header[1] = 0x80 | len;
          maskKey.copy(header, 2);
        } else if (len <= 65535) {
          header = Buffer.alloc(8);
          header[0] = 0x81;
          header[1] = 0x80 | 126;
          header.writeUInt16BE(len, 2);
          maskKey.copy(header, 4);
        } else {
          header = Buffer.alloc(14);
          header[0] = 0x81;
          header[1] = 0x80 | 127;
          header.writeBigUInt64BE(BigInt(len), 2);
          maskKey.copy(header, 10);
        }

        const masked = Buffer.alloc(len);
        const src = Buffer.from(json);
        for (let i = 0; i < len; i++) {
          masked[i] = src[i] ^ maskKey[i % 4];
        }

        socket.write(Buffer.concat([header, masked]));
      });
    }

    const checkInterval = setInterval(() => {
      if (upgraded) {
        clearInterval(checkInterval);
        resolve({ send, close: () => socket.end() });
      }
    }, 50);
  });
}

async function capture() {
  const jsonRes = await new Promise((res, rej) => {
    http.get('http://localhost:9222/json', (r) => {
      let d = '';
      r.on('data', c => d += c);
      r.on('end', () => res(JSON.parse(d)));
    }).on('error', rej);
  });

  const page = jsonRes.find(p => p.type === 'page' && p.title.includes('LemGendary AI Studio'));
  if (!page) {
    console.error('LemGendary page not found');
    process.exit(1);
  }

  console.log('Connecting to:', page.webSocketDebuggerUrl);
  const client = await createWebSocket(page.webSocketDebuggerUrl);
  const outDir = 'c:/Development/python/model-training/lemgendary-docs/assets/gui';

  async function snap(filename) {
    const res = await client.send('Page.captureScreenshot', { format: 'png' });
    const buf = Buffer.from(res.data, 'base64');
    fs.writeFileSync(path.join(outDir, filename), buf);
    console.log('Saved:', filename, buf.length, 'bytes');
  }

  async function evaluate(exp) {
    const res = await client.send('Runtime.evaluate', { expression: exp, returnByValue: true });
    return res.result ? res.result.value : null;
  }

  await client.send('Emulation.setDeviceMetricsOverride', {
    width: 1440,
    height: 960,
    deviceScaleFactor: 1,
    mobile: false
  });

  await new Promise(r => setTimeout(r, 1000));

  // Reload page to get fresh health status
  console.log('Reloading page...');
  await client.send('Page.reload');
  await new Promise(r => setTimeout(r, 2000));

  // 1. Projects
  console.log('Navigating to Project Environments...');
  const res1 = await evaluate(`
    const btn = document.getElementById('tab-projects');
    if (btn) {
      btn.click();
      return 'clicked tab-projects';
    }
    const btns = Array.from(document.querySelectorAll('button'));
    const pBtn = btns.find(b => b.textContent.includes('Project Environments'));
    if (pBtn) {
      pBtn.click();
      return 'clicked pBtn text';
    }
    return 'none found';
  `);
  console.log('Projects click result:', res1);
  await new Promise(r => setTimeout(r, 3000));
  await snap('gui_managed_projects.png');

  // 2. Dataset Compiler
  console.log('Navigating to Dataset Compiler...');
  const res2 = await evaluate(`
    const btn = document.getElementById('tab-datasets');
    if (btn) {
      btn.click();
      return 'clicked tab-datasets';
    }
    const btns = Array.from(document.querySelectorAll('button'));
    const dBtn = btns.find(b => b.textContent.includes('Dataset Compiler'));
    if (dBtn) {
      dBtn.click();
      return 'clicked dBtn text';
    }
    return 'none found';
  `);
  console.log('Datasets click result:', res2);
  await new Promise(r => setTimeout(r, 3000));
  await snap('gui_dataset_compiler.png');

  // Subtab 1: Download from Kaggle
  console.log('Navigating to Kaggle Download Subtab...');
  const resK1 = await evaluate(`
    const btns = Array.from(document.querySelectorAll('button'));
    const dBtn = btns.find(b => b.textContent.includes('Download from Kaggle'));
    if (dBtn) { dBtn.click(); return 'clicked download'; }
    return 'not found download';
  `);
  console.log('Download subtab:', resK1);
  await new Promise(r => setTimeout(r, 1500));
  await snap('gui_kaggle_cloud_hub.png');

  // Subtab 2: Upload to Kaggle
  console.log('Navigating to Kaggle Upload Subtab...');
  const resK2 = await evaluate(`
    const btns = Array.from(document.querySelectorAll('button'));
    const uBtn = btns.find(b => b.textContent.includes('Upload to Kaggle'));
    if (uBtn) { uBtn.click(); return 'clicked upload'; }
    return 'not found upload';
  `);
  console.log('Upload subtab:', resK2);
  await new Promise(r => setTimeout(r, 1500));
  await snap('gui_kaggle_upload_hub.png');

  // Subtab 3: Update Metadata Only
  console.log('Navigating to Kaggle Metadata Subtab...');
  const resK3 = await evaluate(`
    const btns = Array.from(document.querySelectorAll('button'));
    const mBtn = btns.find(b => b.textContent.includes('Update Metadata Only'));
    if (mBtn) { mBtn.click(); return 'clicked metadata'; }
    return 'not found metadata';
  `);
  console.log('Metadata subtab:', resK3);
  await new Promise(r => setTimeout(r, 1500));
  await snap('gui_kaggle_metadata_hub.png');

  console.log('Done!');
  client.close();
  process.exit(0);
}

capture().catch(err => {
  console.error(err);
  process.exit(1);
});
