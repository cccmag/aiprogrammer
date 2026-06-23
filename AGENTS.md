# AGENTS.md — AI 程式人雜誌

## What this repo is

A monthly Chinese-language tech magazine (`AI 程式人雜誌`), written entirely by AI (OpenCode + Big Pickle). The editor (陳鍾誠, ccckmit) reviews and publishes. Seven issues exist: 202603–202609.

## Structure

Each month `2026MM/` follows a fixed layout:

```
2026MM/
├── README.md       # Issue index with links to all content
├── news.md         # Monthly tech news
├── focus.md        # Theme overview
├── focus1–7.md     # Theme deep-dive articles
├── focus_code.md   # Code documentation
├── articles.md     # Article index
├── article1–10.md  # Feature articles (5 programming + 5 AI)
├── end.md          # Conclusion
└── _code/          # Code examples
    ├── test.sh     # Test/run script
    └── ...
```

## Code conventions

- **Python months** (202603–202606): single-file scripts. Run with `python3 _code/xxx.py` or `_code/test.sh`.
- **Rust months** (202607–202609): standalone Cargo projects. Edition `"2024"`. Cargo.lock committed. Test with `cargo test` or `_code/test.sh`.
- Every `_code/` directory contains a `test.sh` — run it to verify the example.

## Content rules

- All articles are written in Traditional Chinese (zh-TW).
- References/links in articles should point to Google search URLs, not direct paper links (they rot).
- Before writing an issue: first produce a draft TOC in `README.md`, get editor approval, then fill all files.
- Consistency matters: when renaming files, update all cross-references (`README.md`, `focus.md`, `articles.md`, `end.md`).

## Git

- Commits use conventional style with month prefix (e.g., `202603 finished`).
- `target/` directories are committed (not in `.gitignore`).

## Key files

- `_doc/prompt.md` — the system prompt used to generate each issue.
- `_doc/editor.md` — detailed editor workflow and troubleshooting guide.
