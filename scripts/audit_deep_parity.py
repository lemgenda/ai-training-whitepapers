import os
import re
import json

docs_root = 'lemgendary-docs'
manifest_path = os.path.join(docs_root, 'manifest', 'documents.json')
with open(manifest_path, 'r', encoding='utf-8') as f:
    manifest = json.load(f)

print(f"Auditing all {len(manifest['documents'])} document pairs for comprehensive parity...")

issues_found = []

for doc in manifest['documents']:
    doc_id = doc['id']
    hp = os.path.join(docs_root, doc['html_path'])
    mp = os.path.join(docs_root, doc['md_path'])

    with open(hp, 'r', encoding='utf-8', errors='ignore') as f:
        h = f.read()
    with open(mp, 'r', encoding='utf-8', errors='ignore') as f:
        m = f.read()

    doc_issues = []

    # 1. H2 Headings
    h2_h = [re.sub(r'<[^>]+>', '', x).strip() for x in re.findall(r'<h2[^>]*>(.*?)</h2>', h, re.I)]
    h2_h = [x for x in h2_h if x.lower() not in ('contents', 'table of contents', 'navigation matrix') and not x.lower().startswith('category')]

    h2_m = [re.sub(r'[*_`]', '', x).strip() for x in re.findall(r'^##\s+(.+)$', m, re.M)]
    h2_m = [x for x in h2_m if x.lower() not in ('contents', 'table of contents', 'navigation matrix') and not x.lower().startswith('category')]

    h2_h_norm = [re.sub(r'\s+', ' ', x.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')).strip() for x in h2_h]
    h2_m_norm = [re.sub(r'\s+', ' ', x.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')).strip() for x in h2_m]

    if len(h2_h_norm) != len(h2_m_norm):
        doc_issues.append(f"H2 count mismatch: HTML({len(h2_h_norm)}) vs MD({len(h2_m_norm)})")

    # 2. Images
    h_imgs = set(os.path.basename(x.split('?')[0]) for x in re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', h, re.I) if 'logo' not in x.lower() and 'icon' not in x.lower() and not x.startswith('data:'))
    m_imgs = set(os.path.basename(x.split('?')[0].split('#')[0]) for x in re.findall(r'!\[.*?\]\((.*?)\)', m) if 'logo' not in x.lower() and 'icon' not in x.lower() and not x.startswith('data:'))
    if h_imgs != m_imgs:
        doc_issues.append(f"Image mismatch: HTML={sorted(list(h_imgs))} vs MD={sorted(list(m_imgs))}")

    # 3. Tables
    h_tables = len(re.findall(r'<table', h, re.I))
    m_tables = len(re.findall(r'\|(?:\s*:?-+:?\s*\|)+', m))
    if abs(h_tables - m_tables) > 1:
        doc_issues.append(f"Table count difference: HTML={h_tables} vs MD={m_tables}")

    # 4. Length anomaly
    ratio = len(m) / len(h) if len(h) > 0 else 0
    if ratio < 0.25:
        doc_issues.append(f"Markdown significantly smaller than HTML: ratio={ratio:.2f} (HTML={len(h)}, MD={len(m)})")
    elif ratio > 3.0:
        doc_issues.append(f"Markdown significantly larger than HTML: ratio={ratio:.2f} (HTML={len(h)}, MD={len(m)})")

    if doc_issues:
        issues_found.append((doc_id, doc_issues))

print(f"\n--- AUDIT SUMMARY: {len(issues_found)} files with discrepancies ---")
for doc_id, issues in issues_found:
    print(f"\n[{doc_id}]:")
    for iss in issues:
        print(f"  * {iss}")
