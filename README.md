# GTAPE IEEE Citation Style

A modified IEEE citation style based on the official [citation-style-language/styles](https://github.com/citation-style-language/styles) repository.

## Available Variants

| File | Style name | Consecutive citations |
| --- | --- | --- |
| [ieee.csl](ieee.csl) | IEEE-GTAPE | Collapsed into a range |
| [ieee-no-collapse.csl](ieee-no-collapse.csl) | IEEE-GTAPE (No Citation Collapse) | Each number shown separately: [1], [2], [3] |

Both variants show the first three authors followed by italicized *et al.* for four or more authors, with no comma before *et al.*, and hide DOI output. They retain the existing name formatting, oldest-first bibliography order, and punctuation. The existing suppression of URLs and access dates is also retained.

Install the desired `.csl` file in your reference manager. The variants have distinct style IDs, so both can be installed together.

The weekly upstream workflow maintains both variants. When merging upstream changes manually, update both files against `.upstream-baseline/ieee.csl`, preserve their respective citation behavior and metadata, and refresh the baseline only after both files are merged.

## Implemented Customizations
- Citations collapse in the style of [1]-[5] in `ieee.csl`; `ieee-no-collapse.csl` lists every number separately
- Authors' names collapse to *et al.* after 3 names, with no delimiter before it
- DOI is hidden

## Unimplemented Styles
The professor wants there to be only a period but no space between initialized first name and last name. As far as I know it's not doable with CSL 1.0.2 specification.

## Updating from Upstream

To pull the latest changes from the official IEEE style and merge with GTAPE customizations:

```bash
# 1. Fetch the latest from upstream
git fetch upstream master

# 2. Extract the upstream ieee.csl to a temporary file
git show upstream/master:ieee.csl > ieee.csl.upstream

# 3. Compare the two files to see what changed
diff ieee.csl ieee.csl.upstream

# 4. Manually merge any desired upstream changes into ieee.csl
#    while preserving GTAPE customizations (see below)

# 5. Clean up and commit
rm ieee.csl.upstream
git add ieee.csl
git commit -m "Merge upstream IEEE style updates"
```

### GTAPE Customizations to Preserve

When merging upstream changes, make sure to keep these GTAPE-specific modifications:

1. **Info section**: Preserve each variant's distinct title, ID, and self link
2. **Author macro** (~line 125): `et-al-min="4" et-al-use-first="3" initialize-with="." delimiter-precedes-et-al="never" delimiter-precedes-last="never"`
3. **Director macro** (~line 143): Same et-al settings as author
4. **Access macro**: DOI output section should be removed (no `<else-if match="any" variable="DOI">` block)
5. **Citation element**: Keep `collapse="citation-number"` in `ieee.csl`; omit it in `ieee-no-collapse.csl`
6. **Article-journal bibliography**: Use period (not comma) before access macro
7. **Access macro**: Keep `<text value=""/>` to suppress DOI, URL, and access-date output. CSL requires a rendering element, so do not leave the macro empty.
8. **Bibliography sort**: Keep issued date ascending, then citation number ascending
