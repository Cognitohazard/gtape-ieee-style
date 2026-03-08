# GTAPE IEEE Citation Style

A modified IEEE citation style based on the official [citation-style-language/styles](https://github.com/citation-style-language/styles) repository.

## Implemented Customizations
- Citations collapse in the style of [1]-[5]
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

1. **Info section**: Keep title as "IEEE-GTAPE" and id/link pointing to this repo
2. **Author macro** (~line 125): `et-al-min="4" et-al-use-first="3" initialize-with="." delimiter-precedes-et-al="never" delimiter-precedes-last="never"`
3. **Director macro** (~line 143): Same et-al settings as author
4. **Access macro**: DOI output section should be removed (no `<else-if match="any" variable="DOI">` block)
5. **Citation element** (~line 322): Keep `collapse="citation-number"` attribute
6. **Article-journal bibliography**: Use period (not comma) before access macro
7. **Remove Access macro entirely**
