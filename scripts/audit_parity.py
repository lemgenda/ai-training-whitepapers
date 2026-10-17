import os
import re
import json

docs_root = 'lemgendary-docs'
manifest_path = os.path.join(docs_root, 'manifest', 'documents.json')
with open(manifest_path, 'r', encoding='utf-8') as f:
    manifest = json.load(f)

print(f"Auditing parity across all {len(manifest['documents'])} document pairs...")

results = []

for doc in manifest['documents']:
    doc_id = doc['id']
    hp = os.path.join(docs_root, doc['html_path'])
    mp = os.path.join(docs_root, doc['md_path'])

    with open(hp, 'r', encoding='utf-8', errors='ignore') as f:
        h_txt = f.read()
    with open(mp, 'r', encoding='utf-8', errors='ignore') as f:
        m_txt = f.read()

    # 1. H1 title
    h1_match = re.search(r'<h1>(.*?)</h1>', h_txt, re.IGNORECASE | re.DOTALL)
    m1_match = re.search(r'^#\s+(.+)$', m_txt, re.MULTILINE)
    h_h1 = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip() if h1_match else ""
    m_h1 = m1_match.group(1).strip() if m1_match else ""

    # 2. H2 headings
    h2_matches = [re.sub(r'<[^>]+>', '', x).strip() for x in re.findall(r'<h2[^>]*>(.*?)</h2>', h_txt, re.IGNORECASE | re.DOTALL)]
    h2_matches = [re.sub(r'\s+', ' ', x.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')).strip() for x in h2_matches if not x.lower().startswith('category') and x.lower() not in ('contents', 'table of contents', 'navigation matrix')]
    m2_matches = [re.sub(r'[*_`]', '', x).strip() for x in re.findall(r'^##\s+(.+)$', m_txt, re.MULTILINE)]
    m2_matches = [re.sub(r'\s+', ' ', x.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')).strip() for x in m2_matches if not x.lower().startswith('category') and x.lower() not in ('contents', 'table of contents', 'navigation matrix')]

    # 3. Images (non-logo)
    h_imgs = set(os.path.basename(x.split('?')[0]) for x in re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', h_txt, re.IGNORECASE) if 'logo' not in x.lower() and 'icon' not in x.lower() and not x.startswith('data:'))
    m_imgs = set(os.path.basename(x.split('?')[0].split('#')[0]) for x in re.findall(r'!\[.*?\]\((.*?)\)', m_txt) if 'logo' not in x.lower() and 'icon' not in x.lower() and not x.startswith('data:'))

    # 4. Tables
    h_tables = len(re.findall(r'<table', h_txt, re.IGNORECASE))
    m_tables = len(re.findall(r'\|(?:\s*:?-+:?\s*\|)+', m_txt))

    # 5. Check if one has significant content missing compared to the other
    h_len = len(h_txt)
    m_len = len(m_txt)
    ratio = m_len / h_len if h_len > 0 else 0

    img_diff = h_imgs ^ m_imgs
    h2_diff = set(h2_matches) ^ set(m2_matches)

    results.append({
        'id': doc_id,
        'h1_html': h_h1,
        'h1_md': m_h1,
        'h2_html_count': len(h2_matches),
        'h2_md_count': len(m2_matches),
        'h2_diff': list(h2_diff),
        'h_imgs': list(h_imgs),
        'm_imgs': list(m_imgs),
        'img_diff': list(img_diff),
        'h_tables': h_tables,
        'm_tables': m_tables,
        'ratio': ratio,
        'h_len': h_len,
        'm_len': m_len
    })

print("\n--- RESULTS SUMMARY ---")
desync_count = 0
for r in results:
    issues = []
    if r['img_diff']:
        issues.append(f"Image diff: {r['img_diff']}")
    if abs(r['h2_html_count'] - r['h2_md_count']) > 2:
        issues.append(f"H2 count mismatch: HTML {r['h2_html_count']} vs MD {r['h2_md_count']}")
    if r['ratio'] < 0.25 or r['ratio'] > 2.0:
        issues.append(f"Length ratio anomaly: ratio={r['ratio']:.2f} (HTML={r['h_len']}, MD={r['m_len']})")
    
    if issues:
        desync_count += 1
        print(f"[{r['id']}]:")
        for iss in issues:
            print(f"    - {iss}")
        if r['h2_diff']:
            print(f"    - Diff elements: {r['h2_diff']}")

print(f"\nTotal pairs with notable differences: {desync_count} / {len(results)}")
