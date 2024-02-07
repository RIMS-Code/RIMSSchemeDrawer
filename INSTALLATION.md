# Installation

The following instructions are for installation of the GUI for release version `2.1.4`.
Instructions for installation from source are given for the development version.

## GUI

To install the GUI, 
it is recommended that you use [`pipx`](https://github.com/pypa/pipx).
This will create a new virtual environment
in which the `rimsschemedrawer` is executed.

Follow the instructions at the given link to install `pipx`.
Then install the `rimsschemedrawer` by typing:

```bash
pipx install rimsschemedrawer[gui]
```

You can now run the drawer by simply running the installed executable:

```bash
rimsschemedrawer
```

## Development version (`v3`)

This version is currently under development.
To install development versions and pre-releases from `pypi`,
please see the main [README](README.md).

## From Source

To install the `rimsschemedrawer` from source
and work with it,
we recommend that you have [`rye`](https://rye-up.com/) installed.

Clone the repository and go into the folder:

```bash
git clone https://github.com/RIMS-Code/RIMSSchemeDrawer.git
cd RIMSSchemeDrawer
```

If you have `rye` installed,
simply run:

```bash
rye sync --all-features
```

Using `pip` 
ideally inside a virtual environment
run:

```bash
pip install .[gui]
```

If you do not want the GUI capability, 
leave the `--all-features` (`rye`)
or the `[gui]` part (`pip`) out.

If you have the GUI, 
you can now run:

```bash
rye run rimsschemedrawer
```

or 

```bash
rimsschemedrawer
```

## Contribute

If you use `rye` and follow the instructions above
for installation from source,
you will have all required dependencies for development installed.

The following additional commands can be useful:

- `rye format`: Format the code with [`ruff`](https://docs.astral.sh/ruff/formatter/)
- `rye lint`: Lint the code with [`ruff`](https://docs.astral.sh/ruff/formatter/)
- `rye run test`: Test the code with [`pytest`](https://docs.pytest.org/)
