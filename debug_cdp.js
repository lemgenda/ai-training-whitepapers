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
    const socket = net.createConnection(port, host);
    const secKey = crypto.randomBytes(16).toString('base64');

    socket.on('connect', () => {
      socket.write([
        `GET ${url.pathname} HTTP/1.1`,
        `Host: ${host}:${port}`,
        'Upgrade: websocket',
        'Connection: Upgrade',
        `Sec-WebSocket-Key: ${secKey}`,
        'Sec-WebSocket-Version: 13',
        '\r\n'
      ].join('\r\n'));
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
          if (headersStr.includes('101')) {
            upgraded = true;
            buffer = buffer.slice(headerEnd + 4);
          } else {
            return reject(new Error('Upgrade failed: ' + headersStr));
          }
        }
      }

      while (upgraded && buffer.length >= 2) {
        let payloadLen = buffer[1] & 0x7f;
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

        if ((buffer[0] & 0x0f) === 1 || true) {
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
        for (let i = 0; i < len; i++) masked[i] = src[i] ^ maskKey[i % 4];
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

async function main() {
  const jsonRes = await new Promise((res, rej) => {
    http.get('http://localhost:9222/json', (r) => {
      let d = '';
      r.on('data', c => d += c);
      r.on('end', () => res(JSON.parse(d)));
    }).on('error', rej);
  });

  const page = jsonRes.find(p => p.type === 'page' && p.title.includes('LemGendary AI Studio'));
  console.log('Connecting to ws:', page.webSocketDebuggerUrl);
  const client = await createWebSocket(page.webSocketDebuggerUrl);

  const evalRaw = async (exp) => {
    const res = await client.send('Runtime.evaluate', { expression: exp, returnByValue: true });
    return res.result ? res.result.value : null;
  };

  const outDir = 'c:/Development/python/model-training/lemgendary-docs/assets/gui';
  const snap = async (filename) => {
    const res = await client.send('Page.captureScreenshot', { format: 'png' });
    const buf = Buffer.from(res.data, 'base64');
    fs.writeFileSync(path.join(outDir, filename), buf);
    console.log('Saved:', filename, buf.length, 'bytes');
  };

  // Inspect page buttons
  const buttons = await evalRaw(`
    Array.from(document.querySelectorAll('button')).map(b => ({
      id: b.id,
      text: b.textContent.replace(/\\s+/g, ' ').trim()
    }))
  `);
  console.log('DOM Buttons:', buttons);

  // 1. Click Projects
  console.log('Clicking Projects tab...');
  await evalRaw(`
    const b = Array.from(document.querySelectorAll('button')).find(x => x.textContent.includes('Project Environments'));
    if (b) b.click();
  `);
  await new Promise(r => setTimeout(r, 2000));
  await snap('gui_managed_projects.png');

  // 2. Click Dataset Compiler
  console.log('Clicking Dataset Compiler tab...');
  await evalRaw(`
    const b = Array.from(document.querySelectorAll('button')).find(x => x.textContent.includes('Dataset Compiler'));
    if (b) b.click();
  `);
  await new Promise(r => setTimeout(r, 2000));
  await snap('gui_dataset_compiler.png');

  // 3. Subtab Download
  console.log('Clicking Download subtab...');
  await evalRaw(`
    const b = Array.from(document.querySelectorAll('button')).find(x => x.textContent.includes('Download from Kaggle'));
    if (b) b.click();
  `);
  await new Promise(r => setTimeout(r, 1500));
  await snap('gui_kaggle_cloud_hub.png');

  // 4. Subtab Upload
  console.log('Clicking Upload subtab...');
  await evalRaw(`
    const b = Array.from(document.querySelectorAll('button')).find(x => x.textContent.includes('Upload to Kaggle'));
    if (b) b.click();
  `);
  await new Promise(r => setTimeout(r, 1500));
  await snap('gui_kaggle_upload_hub.png');

  // 5. Subtab Metadata
  console.log('Clicking Metadata subtab...');
  await evalRaw(`
    const b = Array.from(document.querySelectorAll('button')).find(x => x.textContent.includes('Update Metadata Only'));
    if (b) b.click();
  `);
  await new Promise(r => setTimeout(r, 1500));
  await snap('gui_kaggle_metadata_hub.png');

  console.log('ALL DONE!');
  client.close();
  process.exit(0);
}

main().catch(console.error);
