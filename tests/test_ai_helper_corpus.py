"""AI Helper training corpus tests of the LemGendary AI Documentation Hub.

The corpus is data of the LemGendary Compiled Manifolds Repo; the tests skip with
an explicit reason when that sibling checkout is absent.
"""

import json
import os
import re

from docs_test_base import DocsTestCase, yaml

EMOJI_PATTERN = re.compile(r"[\U00010000-\U0010ffff]", flags=re.UNICODE)

REQUIRED_VAL_CATEGORIES = frozenset(
    {
        "gui_procedure",
        "cli_command",
        "api_procedure",
        "troubleshooting_diagnostic",
        "model_pipeline",
        "terminology_concept",
        "general_knowledge",
    }
)

FORBIDDEN_CORPUS_TEXT = (
    "POST /api/compile\n",
    "/api/ws/telemetry",
    "lem-env training",
    "lem-env datasets",
    "default: 1000",
)

STALE_LINEAGE = (
    ("Rain Streaks", "irrelevant 'Rain Streaks' lineage"),
    ("Parquet feature tensors", "stale Parquet description"),
)


class TestAiHelperCorpus(DocsTestCase):
    """Schema, split, SSOT and metadata checks of the AI Helper JSONL corpus."""

    def _read_jsonl(self, path):
        """Parse every non-empty line of ``path``; fail on malformed JSON."""
        records = []
        name = os.path.basename(path)
        with open(path, "r", encoding="utf-8") as f:
            for line_idx, line in enumerate(f, 1):
                if not line.strip():
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as e:
                    self.fail(f"Malformed JSON on line {line_idx} of {name}: {e}")
        return records

    def _check_record_text(self, record):
        """No emoji, no legacy NIMA Mobile backbone and no removed routes in one record."""
        text = " ".join(m["content"] for m in record["messages"])
        self.assertEqual(
            len(EMOJI_PATTERN.findall(text)), 0, f"Emoji detected in {record['id']}"
        )
        if "nima_aesthetic_mobile" in text.lower():
            self.assertFalse(
                bool(re.search(r"nima_aesthetic_mobile.*MobileNetV[12]", text, re.IGNORECASE)),
                f"Corpus {record['id']} claimed legacy MobileNet for NIMA Mobile instead of "
                "MobileNetV3-Small",
            )
        for forbidden in FORBIDDEN_CORPUS_TEXT:
            self.assertNotIn(forbidden, text)

    def _check_record_schema(self, record, name):
        """``id``, ``category`` and three ``messages`` (system, user, assistant)."""
        for key in ("id", "category", "messages"):
            self.assertIn(key, record, f"Missing '{key}' in {name}")
        self.assertEqual(
            len(record["messages"]),
            3,
            f"Expected 3 messages (system, user, assistant) in {record['id']}",
        )

    def _check_metadata(self, dataset_dir, train_count, val_count):
        """Dataset metadata has no stale lineage and its counts equal the splits."""
        info_path = os.path.join(dataset_dir, "dataset_info.yaml")
        for fname in ("dataset_info.yaml", "dataset-metadata.json", "README.md"):
            fpath = os.path.join(dataset_dir, fname)
            if not os.path.exists(fpath):
                continue
            with open(fpath, "r", encoding="utf-8") as f:
                txt = f.read()
            for stale, label in STALE_LINEAGE:
                self.assertNotIn(stale, txt, f"Found {label} in {fname}")
        if not os.path.exists(info_path):
            return
        with open(info_path, "r", encoding="utf-8") as f:
            info_data = yaml.safe_load(f)
        self.assertEqual(
            info_data.get("train_samples"), train_count, "dataset_info.yaml train count mismatch"
        )
        self.assertEqual(
            info_data.get("val_samples"), val_count, "dataset_info.yaml val count mismatch"
        )
        self.assertEqual(
            info_data.get("count"),
            train_count + val_count,
            "dataset_info.yaml total count mismatch",
        )

    def _split_ids(self, path):
        """Ids of one split, after the schema and emoji check of every record."""
        name = os.path.basename(path)
        ids = set()
        for record in self._read_jsonl(path):
            self._check_record_schema(record, name)
            self.assertFalse(
                EMOJI_PATTERN.search(json.dumps(record, ensure_ascii=False)),
                f"Found emoji in {name} record {record['id']}",
            )
            ids.add(record["id"])
        return ids

    # ── 13. AI Helper Training Corpus Integrity ─────────────────────────────
    def test_ai_helper_corpus_integrity(self):
        """Rule: AI Helper JSONL corpus must exist, parse cleanly, obey zero-emojis,
        strictly align with unified_models_v2.yaml SSOT, and maintain balanced validation
        coverage."""
        _corpus_dir, train_path, val_path = self._ai_helper_corpus()
        train_records = self._read_jsonl(train_path)
        val_records = self._read_jsonl(val_path)
        all_ids = [r["id"] for r in train_records + val_records]
        self.assertEqual(len(all_ids), len(set(all_ids)), "Duplicate IDs found in corpus")
        for record in train_records + val_records:
            self._check_record_text(record)
        missing = REQUIRED_VAL_CATEGORIES - {r["category"] for r in val_records}
        self.assertEqual(len(missing), 0, f"Held-out validation set missing categories: {missing}")

    # ── 36. AI Helper Dataset Schema & Split Integrity ───────────────────────
    def test_ai_helper_dataset_integrity(self):
        """Rule: ai_helper_train.jsonl and ai_helper_val.jsonl must have valid schemas, zero
        overlap, and 0 emojis."""
        dataset_dir, train_path, val_path = self._ai_helper_corpus()
        train_ids = self._split_ids(train_path)
        val_ids = self._split_ids(val_path)
        overlap = train_ids & val_ids
        self.assertEqual(
            len(overlap), 0, f"Train and validation splits share duplicate IDs: {overlap}"
        )
        self.assertGreaterEqual(
            len(val_ids),
            25,
            "Held-out validation set must contain >= 25 records for robust evaluation",
        )
        self._check_metadata(dataset_dir, len(train_ids), len(val_ids))
