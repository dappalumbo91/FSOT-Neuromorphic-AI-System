# FSOT Neuromorphic AI System

An experimental, brain-inspired AI system built on FSOT 2.0 (Fluid Spacetime Omni-Theory). It models brain regions (frontal cortex, hippocampus, amygdala, thalamus, cerebellum and others) as separate Python modules coordinated by an orchestrator, with FSOT-derived constants used as the system's mathematical basis. The repository also keeps a large set of analysis scripts, integration experiments and dated reports from September 2025.

Part of the FSOT project family. The hub repository is **[FSOT-2.1-Lean](https://github.com/dappalumbo91/FSOT-2.1-Lean)**.

## What's inside

| Path | Contents |
|------|----------|
| `FSOT_Clean_System/` | The modular rewrite: `main.py` entry point, `brain/` (one module per brain region plus `brain_orchestrator.py`), `core/` (`fsot_engine.py`, `neural_signal.py`, `consciousness.py`), `config/`, `interfaces/`, `integration/`, `capabilities/`, `tests/`. It has its own [README](FSOT_Clean_System/README.md) and `requirements.txt`. |
| `src/` | Earlier package layout: `neuromorphic_brain/`, `multimodal/` (vision, audio, integration), `fsot_core/` |
| `tests/` | `test_brain.py`, `test_integration.py`, `test_multimodal.py` |
| `utils/` | `memory_manager.py` |
| `FSOT_Visual_Archive/` | Archived experiments, generated images, logs and reports, sorted into numbered folders. See `FSOT_Visual_Archive/FILE_INDEX.md`. |
| top-level `*.py` | Standalone scripts: FSOT 2.0 foundation/implementation variants, simulations, validators, performance monitors, web/research integration experiments, demos |
| top-level `*_YYYYMMDD_*.json` / `*.md` | Dated output reports from those scripts |
| `.github/workflows/fsot_ci.yml` | CI: compatibility tests, integration test, performance benchmark and compliance checks across Python 3.9–3.12 |
| `requirements.txt` | Top-level dependencies (`numpy`, `scipy`, `mpmath`, `sympy`, `pytest`) |

## Install and run

Commands below are the ones the CI workflow uses. They were also run locally on Python 3.13:

```bash
python -m pip install -r requirements.txt
python -m pytest fsot_compatibility_tests.py -v     # 9 tests, pass
python fsot_integration_test.py --ci-mode           # finishes in its "fallback mode" (one import fails, see below)
```

For the modular system, see [`FSOT_Clean_System/README.md`](FSOT_Clean_System/README.md). It has its own `requirements.txt` and starts with `python main.py`. Some modules under `src/` import `torch` and other packages that are not in the top-level `requirements.txt`.

## Status

This is experimental research code from September 2025 and is not under active development. The existing CI workflow passed on its most recent recorded runs (November 2025). Many scripts are one-off experiments, and their reports are kept for the record. Treat claims in the generated reports as script output, not independent validation. When run locally, `fsot_integration_test.py --ci-mode` reports that `FSOT_Foundation` cannot be imported from `FSOT_Clean_System/fsot_2_0_foundation.py`, then falls back and exits successfully.

Current FSOT work (Lean 4 proofs, frozen compute authority, verification) lives in [FSOT-2.1-Lean](https://github.com/dappalumbo91/FSOT-2.1-Lean).

## License

There is no LICENSE file in this repository.
