"""Validate the installable styles against the pinned CSL 1.0.2 schemas."""
from pathlib import Path
import sys

from lxml import etree, isoschematron
import rnc2rng

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "tests" / "vendor" / "schema"


def main():
    if (ROOT / ".upstream-review").exists():
        sys.exit("Unresolved upstream update: see .upstream-review/README.md")
    rng = rnc2rng.dumps(rnc2rng.load(str(SCHEMA / "csl.rnc")))
    relaxng = etree.RelaxNG(etree.fromstring(rng.encode("utf-8")))
    schematron = isoschematron.Schematron(etree.parse(str(SCHEMA / "csl.sch")))
    valid = True
    ids = set()
    ns = {"c": "http://purl.org/net/xbiblio/csl"}
    for filename in ("ieee.csl", "ieee-no-collapse.csl"):
        try:
            doc = etree.parse(str(ROOT / filename))
            for validator in (relaxng, schematron):
                if not validator.validate(doc):
                    print(validator.error_log, file=sys.stderr)
                    valid = False
            style_id = doc.findtext("c:info/c:id", namespaces=ns)
            if style_id in ids:
                raise ValueError("Both styles must have distinct IDs")
            ids.add(style_id)
            print(f"Checked {filename}")
        except (etree.XMLSyntaxError, ValueError) as exc:
            print(f"{filename}: {exc}", file=sys.stderr)
            valid = False
    return 0 if valid else 1


if __name__ == "__main__":
    sys.exit(main())
