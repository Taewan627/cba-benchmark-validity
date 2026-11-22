"""Load the FROZEN v1 renderer, parser and scorer from public_release/code
without modifying them. The v1 modules import `src.spec`; we provide that one
constant here instead of editing frozen files."""
import importlib.util, sys, types
from pathlib import Path

CODE = Path(__file__).resolve().parents[3] / "public_release" / "code"

def _load(name, fname):
    spec = importlib.util.spec_from_file_location(name, CODE / fname)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

if "src.spec" not in sys.modules:
    pkg = types.ModuleType("src"); pkg.__path__ = []
    spec_mod = types.ModuleType("src.spec")
    spec_mod.CONDITIONS = ("CLEAN", "COMMISSION", "OMISSION")
    sys.modules.setdefault("src", pkg); sys.modules["src.spec"] = spec_mod

protocol_construction = _load("frozen_protocol_construction", "protocol_construction.py")
parser = _load("frozen_parser", "parser.py")
scoring = _load("frozen_scoring", "deterministic_scoring.py")
