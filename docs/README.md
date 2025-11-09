# RackSum Documentation

This directory contains the MkDocs documentation for RackSum.

## Building the Documentation

### Prerequisites

Install the required Python packages:

```bash
pip install -r ../requirements.txt
```

### Serve Locally

To preview the documentation locally with live reload:

```bash
# From project root
npm run docs:serve

# Or directly with mkdocs
mkdocs serve
```

The documentation will be available at [http://localhost:8000](http://localhost:8000)

### Build Static Site

To build the static documentation site:

```bash
# From project root
npm run docs:build

# Or directly with mkdocs
mkdocs build
```

The built site will be in the `site/` directory.

### Deploy to GitHub Pages

To deploy documentation to GitHub Pages:

```bash
# From project root
npm run docs:deploy

# Or directly with mkdocs
mkdocs gh-deploy
```

## Documentation Structure

```
docs/
├── index.md              # Home page
├── installation.md       # Installation guide
├── usage.md             # Usage guide
├── configuration.md     # Configuration guide
├── deployment.md        # Deployment guide
├── development.md       # Development guide
├── api.md               # API reference
├── stylesheets/         # Custom CSS
│   └── extra.css
└── javascripts/         # Custom JavaScript
    └── extra.js
```

## Writing Documentation

### Markdown Extensions

The documentation uses several Markdown extensions:

- **Admonitions**: For notes, warnings, tips
  ```markdown
  !!! note
      This is a note
  ```

- **Code Blocks**: With syntax highlighting
  ```markdown
  ```python
  def hello():
      print("Hello, world!")
  ```
  ```

- **Tables**: Standard Markdown tables
  ```markdown
  | Column 1 | Column 2 |
  |----------|----------|
  | Value 1  | Value 2  |
  ```

- **Task Lists**: Checkboxes
  ```markdown
  - [x] Completed task
  - [ ] Incomplete task
  ```

### Adding New Pages

1. Create a new Markdown file in `docs/`
2. Add it to the navigation in `mkdocs.yml`:
   ```yaml
   nav:
     - Home: index.md
     - New Page: new-page.md
   ```

### Code Examples

Use fenced code blocks with language identifiers:

```markdown
```bash
npm install
```

```python
print("Hello, world!")
```

```javascript
console.log("Hello, world!");
```
```

### Images

Place images in `docs/images/` and reference them:

```markdown
![Alt text](images/screenshot.png)
```

## Styling

Custom styles are in `docs/stylesheets/extra.css`. Modify this file to change the appearance of the documentation.

## Theme Configuration

The documentation uses the Material for MkDocs theme. Configuration is in `mkdocs.yml`:

```yaml
theme:
  name: material
  palette:
    primary: blue
    accent: indigo
  features:
    - navigation.tabs
    - search.suggest
    # ... more features
```

## Search

The documentation includes a built-in search feature. Search indexes are automatically generated during the build process.

## Contributing to Documentation

1. Edit the relevant `.md` file in `docs/`
2. Test locally with `npm run docs:serve`
3. Submit a pull request with your changes

## Resources

- [MkDocs Documentation](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [Markdown Guide](https://www.markdownguide.org/)
