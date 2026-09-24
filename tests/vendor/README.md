# Pinned validation sources

These files are vendored so checks do not depend on live schema or locale downloads.

- `schema/`: official CSL **v1.0.2**, commit [`506040022f6c37846343edd36658b23e85b5b8ff`](https://github.com/citation-style-language/schema/tree/506040022f6c37846343edd36658b23e85b5b8ff/schemas/styles). Files are copied unchanged from `schemas/styles/`. The MIT license is included in `schema/LICENSE.txt`.
- `locales-en-US.xml`: official CSL locale at commit [`a89adece41013402236e2c9020972d7e931fbab8`](https://github.com/citation-style-language/locales/blob/a89adece41013402236e2c9020972d7e931fbab8/locales-en-US.xml). It retains its original contributors and the Creative Commons Attribution-ShareAlike 3.0 license declaration inside the file.

Update these pins deliberately and review any rendering changes. CSL validation combines the RELAX NG schema with `csl.sch` so undefined or duplicate macros also fail.
