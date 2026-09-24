import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "update_upstream.py"
spec = importlib.util.spec_from_file_location("update_upstream", SCRIPT)
update = importlib.util.module_from_spec(spec)
spec.loader.exec_module(update)
SHA = "a" * 40
BASE = '<style xmlns="http://purl.org/net/xbiblio/csl">\n<!-- upstream -->\n</style>\n'


class UpstreamTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / ".upstream-baseline").mkdir()
        self.baseline = self.root / ".upstream-baseline/ieee.csl"
        self.baseline.write_text(BASE, encoding="utf-8")
        for name in update.STYLES:
            (self.root / name).write_text(BASE, encoding="utf-8")
        self.incoming = self.root / "incoming"

    def run_update(self, text):
        self.incoming.write_text(text, encoding="utf-8")
        return update.prepare(self.root, self.incoming, SHA)

    def test_unchanged_does_not_create_an_update(self):
        self.assertEqual(self.run_update(BASE), {"changed": "false", "conflict": "false"})
        self.assertFalse((self.root / ".upstream-baseline/source.json").exists())

    def test_clean_update_updates_both_styles_and_baseline(self):
        incoming = BASE.replace("upstream", "upstream changed")
        self.assertEqual(self.run_update(incoming)["conflict"], "false")
        for path in [self.baseline, *(self.root / name for name in update.STYLES)]:
            self.assertEqual(path.read_text(encoding="utf-8"), incoming)
        source = json.loads((self.root / ".upstream-baseline/source.json").read_text())
        self.assertEqual(source["commit"], SHA)

    def test_conflict_preserves_both_styles_and_baseline(self):
        original = BASE.replace("upstream", "customized locally")
        (self.root / update.STYLES[0]).write_text(original, encoding="utf-8")
        incoming = BASE.replace("upstream", "upstream changed")
        self.assertEqual(self.run_update(incoming)["conflict"], "true")
        self.assertEqual((self.root / update.STYLES[0]).read_text(), original)
        self.assertEqual((self.root / update.STYLES[1]).read_text(), BASE)
        self.assertEqual(self.baseline.read_text(), BASE)
        review = self.root / ".upstream-review"
        self.assertIn("<<<<<<<", (review / "ieee.csl.txt").read_text())
        self.assertEqual((review / "ieee.csl.upstream").read_text(), incoming)
        with self.assertRaisesRegex(ValueError, "existing upstream review"):
            self.run_update(incoming)

    def test_invalid_download_and_missing_baseline_do_not_mutate_styles(self):
        with self.assertRaisesRegex(ValueError, "not a CSL style"):
            self.run_update("<html>error page</html>")
        self.baseline.unlink()
        with self.assertRaisesRegex(ValueError, "Missing upstream baseline"):
            self.run_update(BASE)
        for name in update.STYLES:
            self.assertEqual((self.root / name).read_text(), BASE)


if __name__ == "__main__":
    unittest.main()
