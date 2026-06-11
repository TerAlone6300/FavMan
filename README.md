# FavMan

A simple CLI tool to manage your favorite directories and files.

## Installation

```bash
pip install favman
```

Or from source:

```bash
git clone https://github.com/TerAlone6300/FavMan.git
pip install -e .
```

## Commands

- `addfav <alias> [path]`: Add a favorite directory (defaults to current dir).
- `rmfav <alias>`: Remove a favorite directory.
- `listfav`: List all favorite directories and files.
- `goto <alias>`: Print the path of a favorite directory.
- `addfavf <alias> <path>`: Add a favorite file.
- `rmfavf <alias>`: Remove a favorite file.
- `execute <alias> [--interpreter python]`: Run a favorite file.

## Shell Integration (for `goto` to work)

Add this to your `.bashrc` or `.zshrc`:

```bash
goto() {
    target=$(command goto "$1" 2>/dev/null)
    if [ $? -eq 0 ] && [ -d "$target" ]; then
        cd "$target"
    else
        command goto "$@"
    fi
}
```
