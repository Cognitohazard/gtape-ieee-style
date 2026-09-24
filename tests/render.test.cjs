const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { test } = require('node:test');
const CSL = require('citeproc');

const root = path.resolve(__dirname, '..');
const locale = fs.readFileSync(path.join(__dirname, 'vendor/locales-en-US.xml'), 'utf8');
const author = [
  { given: 'Alice', family: 'Able' },
  { given: 'Bob', family: 'Baker' },
  { given: 'Carol', family: 'Clark' },
  { given: 'David', family: 'Dover' },
];
// Deliberately supplied out of date order. Each entry has access information
// to ensure suppressed fields do not leak into different bibliography formats.
const items = [
  { id: 'journal', type: 'article-journal', title: 'Journal example', author,
    'container-title': 'Example Journal', volume: '7', issue: '2', page: '10-15', issued: { 'date-parts': [[2022, 3]] } },
  { id: 'book', type: 'book', title: 'Book example', author: author.slice(0, 3),
    publisher: 'Example Press', issued: { 'date-parts': [[2020]] } },
  { id: 'web', type: 'webpage', title: 'Website example', author: author.slice(0, 1),
    'container-title': 'Example Site', issued: { 'date-parts': [[2024, 1, 1]] } },
  { id: 'film', type: 'motion_picture', title: 'Film example', director: author,
    'publisher-place': 'Boston', issued: { 'date-parts': [[2021, 6, 1]] } },
  { id: 'edited', type: 'book', title: 'Edited example', editor: author,
    publisher: 'Example Press', issued: { 'date-parts': [[2023]] } },
].map(item => ({ ...item, DOI: '10.1234/hidden-doi', URL: 'https://example.invalid/hidden-url',
  accessed: { 'date-parts': [[2025, 8, 20]] } }));

function render(filename) {
  const byId = Object.fromEntries(items.map(item => [item.id, item]));
  const processor = new CSL.Engine({ retrieveLocale: () => locale, retrieveItem: id => byId[id] },
    fs.readFileSync(path.join(root, filename), 'utf8'), 'en-US');
  processor.updateItems(items.map(item => item.id));
  const citations = processor.makeCitationCluster(items.map(item => ({ id: item.id })));
  const locator = processor.makeCitationCluster([{ id: 'book', locator: '12', label: 'page' }]);
  const bibliography = processor.makeBibliography()[1];
  return { citations, locator, bibliography };
}

const collapsed = render('ieee.csl');
const expanded = render('ieee-no-collapse.csl');
test('consecutive citation numbers collapse only in the original variant', () => {
  assert.match(collapsed.citations, /^\[1\][–-]\[5\]$/);
  assert.equal(expanded.citations, '[1], [2], [3], [4], [5]');
  assert.equal(expanded.locator, '[1, p. 12]');
});
test('both variants preserve the same bibliography and name rules', () => {
  assert.deepEqual(collapsed.bibliography, expanded.bibliography);
  const bibliography = expanded.bibliography.join('');
  assert.match(bibliography, /A\. Able, B\. Baker and C\. Clark/);
  assert.match(bibliography, /A\. Able, B\. Baker, C\. Clark <i>et al\.<\/i>/);
  assert.doesNotMatch(bibliography, /Dover|, <i>et al\.<\/i>|hidden-doi|hidden-url|Accessed|Available/);
  const titles = ['Book example', 'Film example', 'Journal example', 'Edited example', 'Website example'];
  titles.forEach((title, index) => assert.ok(expanded.bibliography[index].includes(title)));
});
test('rendered examples match the reviewed formatting snapshot', () => {
  const expected = JSON.parse(fs.readFileSync(path.join(__dirname, 'expected-rendering.json'), 'utf8'));
  assert.deepEqual({ collapsed, expanded }, expected);
});

// Used only for intentionally reviewing/updating expected output, never in CI.
if (process.env.UPDATE_RENDER_SNAPSHOT === '1') {
  fs.writeFileSync(path.join(__dirname, 'expected-rendering.json'), JSON.stringify({ collapsed, expanded }, null, 2) + '\n');
}
