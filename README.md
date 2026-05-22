# Math Research Lab Plugins

This repository is a Codex plugin marketplace repository. It currently exposes one local plugin: `math-research-lab`.

`math-research-lab` is a universal mathematical and scientific research audit plugin for formalization, proof critique, metric validation, experiment auditing, numerical and statistical validation, concept governance, and balanced adversarial research judging.

## Install From A Local Clone

```bash
codex plugin marketplace add /path/to/marketplace-repo
```

Point this command at the marketplace repository root, not the plugin folder. The marketplace root is the directory that contains `.agents/plugins/marketplace.json`.

For this checkout on Windows, use:

```powershell
codex plugin marketplace add C:\math-research-lab
```

Do not use `C:\math-research-lab\plugins\math-research-lab` with `marketplace add`; that directory is the plugin package referenced by the marketplace.

For another checkout, use the absolute path to that repository root.

```bash
codex plugin marketplace add /absolute/path/to/marketplace-repo
```

Then open Codex and run:

```text
/plugins
```

to inspect, install, or enable the plugin.

## Install From GitHub After Publishing

This command works only after a GitHub repository with this exact owner/name exists and contains this marketplace root.

```bash
codex plugin marketplace add bytetiff/math-research-lab-for-codex --ref main
```

To upgrade the marketplace later:

```bash
codex plugin marketplace upgrade math-research-lab-for-codex
```

Then open Codex and run:

```text
/plugins
```

## Run Tests

```bash
cd plugins/math-research-lab
python -m pytest -q
```

The package uses Python 3.11+ and declares lightweight scientific dependencies in `plugins/math-research-lab/pyproject.toml`.
