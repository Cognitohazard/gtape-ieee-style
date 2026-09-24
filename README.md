# GTAPE IEEE Citation Styles

Two customized IEEE styles based on the official [CSL IEEE style](https://github.com/citation-style-language/styles/blob/master/ieee.csl). This project tracks that single upstream file, not updates to the entire CSL styles collection.

## Install

Download a `.csl` file below, then in Zotero open **Settings → Cite → Styles → +** and select the downloaded file. Both variants can be installed together because they have distinct style IDs.

| File | Zotero style name | Consecutive citations |
| --- | --- | --- |
| [ieee.csl](https://raw.githubusercontent.com/Cognitohazard/gtape-ieee-style/master/ieee.csl) | IEEE-GTAPE | Collapsed into a range |
| [ieee-no-collapse.csl](https://raw.githubusercontent.com/Cognitohazard/gtape-ieee-style/master/ieee-no-collapse.csl) | IEEE-GTAPE (No Citation Collapse) | [1], [2], [3] |

Both variants retain:

- The first three authors followed by italicized *et al.* for four or more authors, with no comma before *et al.*; the same settings apply to directors and author substitutions.
- Suppressed DOI, URL, and access-date output.
- The existing name initialization and punctuation, with the bibliography sorted oldest first, then by citation number.

There is still a space between initials and the surname; this project does not implement the requested removal of that space.

## Upstream updates

The **Check upstream IEEE style** workflow runs every Monday at 00:00 UTC and can also be started from the Actions tab. It downloads only `ieee.csl` at a recorded upstream commit and compares it with `.upstream-baseline/ieee.csl`.

When the file changes, the workflow prepares three-way merges for both variants and opens a pull request. It never pushes directly to `master` and never automatically merges a pull request. An existing open upstream update is left intact so manual resolutions are not overwritten.

- Clean updates include both styles and the new baseline with its source commit.
- Conflicting updates open a draft pull request with proposals and instructions under `.upstream-review/`. The installed styles and accepted baseline stay unchanged. Validation intentionally fails until the conflicts are resolved and that directory is removed.
- **Validate styles** must pass before merging. Review the diff and rendered examples before accepting an update. If GitHub requests approval to run a bot-created pull request's workflows, approve the run; the updater also explicitly dispatches validation on the proposed branch.
- If an update was closed without merging, reopen its pull request to resume work. The updater will not overwrite an existing update branch.

The baseline's `source.json` records a commit at which the upstream file was verified; it need not be the commit that originally changed that file.

## Validation and examples

Every pull request and push to `master` runs the official pinned **CSL 1.0.2** schema, its macro-reference checks, rendering examples with citeproc-js, and tests of the update process. Schema and locale sources and licenses are recorded in [tests/vendor/README.md](tests/vendor/README.md).

For local checks, use Python 3.12+ and Node.js 22+:

```sh
python -m pip install -r requirements-dev.txt
npm ci --ignore-scripts
python scripts/validate.py
npm test
python -m unittest discover -s tests -p 'test_*.py' -v
```

The rendering tests cover collapsed and expanded citations, page locators, three/four-author boundaries, directors, editor substitution, hidden access fields, bibliography order, and a reviewed output snapshot. When deliberately changing formatting, update `tests/expected-rendering.json` using `UPDATE_RENDER_SNAPSHOT=1 npm test` in a POSIX shell, then inspect the resulting diff. Do not regenerate snapshots merely to make a failing check pass.

Preserve each style's title, ID, and self link. Keep `collapse="citation-number"` only in `ieee.csl`. The empty-output access macro must retain `<text value=""/>`; an entirely empty macro is invalid CSL.

## Attribution and license

The styles derive from the [Citation Style Language styles project](https://github.com/citation-style-language/styles). Original authors and contributors remain credited inside both files. Style adaptations retain the [Creative Commons Attribution-ShareAlike 3.0 license](https://creativecommons.org/licenses/by-sa/3.0/) declared in their `<rights>` elements. GTAPE modifications include author truncation, suppression of access information, bibliography ordering, and the citation-collapse variant.
