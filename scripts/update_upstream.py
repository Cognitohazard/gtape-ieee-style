"""Prepare a reviewable IEEE update; never commit, push, or replace conflicted styles."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET

STYLES = ("ieee.csl", "ieee-no-collapse.csl")
NS = "{http://purl.org/net/xbiblio/csl}"


def prepare(root, incoming, commit):
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("Expected a full upstream commit SHA")
    baseline = root / ".upstream-baseline" / "ieee.csl"
    if not baseline.is_file():
        raise ValueError("Missing upstream baseline; restore it before updating")
    if (root / ".upstream-review").exists():
        raise ValueError("Resolve the existing upstream review first")
    upstream = incoming.read_text(encoding="utf-8")
    if ET.fromstring(upstream).tag != NS + "style":
        raise ValueError("Upstream download is not a CSL style")
    if baseline.read_text(encoding="utf-8") == upstream:
        return {"changed": "false", "conflict": "false"}
    merged = {}
    conflicts = []
    with tempfile.TemporaryDirectory() as directory:
        temporary = Path(directory)
        base = temporary / "baseline.csl"
        theirs = temporary / "upstream.csl"
        base.write_text(baseline.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
        theirs.write_text(upstream, encoding="utf-8", newline="\n")
        for name in STYLES:
            ours = temporary / name
            ours.write_text((root / name).read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
            result = subprocess.run(
                ["git", "merge-file", "-p", "-L", name, "-L", "previous upstream", "-L", "new upstream",
                 str(ours), str(base), str(theirs)], capture_output=True, encoding="utf-8"
            )
            # git merge-file returns the number of conflicts (at most 127), or an error.
            if result.returncode < 0 or result.returncode > 127 or result.stderr:
                raise RuntimeError(result.stderr or f"git merge-file failed: {result.returncode}")
            merged[name] = result.stdout
            if result.returncode:
                conflicts.append(name)
    source = json.dumps({
        "repository": "https://github.com/citation-style-language/styles",
        "path": "ieee.csl", "commit": commit
    }, indent=2) + "\n"
    if conflicts:
        # Keep both installable styles and the accepted baseline unchanged.
        review = root / ".upstream-review"
        review.mkdir()
        for name, content in merged.items():
            (review / (name + ".txt")).write_text(content, encoding="utf-8", newline="\n")
        (review / "ieee.csl.upstream").write_text(upstream, encoding="utf-8", newline="\n")
        (review / "source.json").write_text(source, encoding="utf-8", newline="\n")
        (review / "README.md").write_text(
            "# Resolve upstream conflicts\n\nConflicts: " + ", ".join(conflicts) + ".\n\n"
            "The .csl.txt files contain proposed merges, including conflict markers.\n"
            "Resolve both proposals into the root style files, preserving GTAPE customizations.\n"
            "Copy ieee.csl.upstream to .upstream-baseline/ieee.csl and source.json to\n"
            ".upstream-baseline/source.json only after resolving both styles.\n"
            "Remove this .upstream-review directory, run validation and rendering tests,\n"
            "then mark the pull request ready for review. Do not merge with this directory present.\n",
            encoding="utf-8", newline="\n"
        )
    else:
        for name, content in merged.items():
            (root / name).write_text(content, encoding="utf-8", newline="\n")
        baseline.write_text(upstream, encoding="utf-8", newline="\n")
        (baseline.parent / "source.json").write_text(source, encoding="utf-8", newline="\n")
    return {"changed": "true", "conflict": str(bool(conflicts)).lower()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("incoming", type=Path)
    parser.add_argument("commit")
    args = parser.parse_args()
    result = prepare(Path(__file__).resolve().parents[1], args.incoming, args.commit)
    output = "".join(f"{key}={value}\n" for key, value in result.items())
    print(output, end="")
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as stream:
            stream.write(output)
