"""`kr` CLI — `run` / `bench` / `config` subcommands."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from rich.console import Console
from rich.table import Table

from .config import env_status, load_prefs, resolve_anthropic_api_key, resolve_prefs_path
from .godproof import run_godproof
from .orchestrator import run_research


def _cmd_run(args: argparse.Namespace) -> int:
    prefs = load_prefs(Path(args.prefs) if args.prefs else None)

    # CLI overrides (per-session, do not mutate the YAML).
    if args.breadth:
        prefs.default_breadth = args.breadth
    if args.depth:
        prefs.default_depth = args.depth

    summary = run_research(
        args.query,
        prefs=prefs,
        sessions_root=Path(args.sessions_root) if args.sessions_root else None,
        stub=args.stub,
    )

    console = Console()
    console.rule("Katala Research — session summary")
    console.print_json(data=summary)
    console.print(f"\n[bold]Report[/]: {summary['report_path']}")
    return 0


def _cmd_bench(args: argparse.Namespace) -> int:
    from .bench.runner import run_bench

    summary = run_bench(
        n_tasks=args.tasks,
        stub=args.stub,
        sessions_root=Path(args.sessions_root) if args.sessions_root else None,
    )
    Console().print_json(data=summary)
    return 0


def _cmd_config(args: argparse.Namespace) -> int:
    prefs = load_prefs(Path(args.prefs) if args.prefs else None)
    console = Console()
    console.rule("Resolved preferences")
    console.print_json(data=prefs.model_dump(by_alias=True))

    table = Table(title="Environment (resolved from .env / shell)")
    table.add_column("Variable"); table.add_column("Value")
    table.add_row("prefs_path", str(resolve_prefs_path()))
    for k, v in env_status().items():
        display = v if v else "[red]NOT SET[/red]"
        table.add_row(k, display)
    console.print(table)
    return 0


def _cmd_godproof(args: argparse.Namespace) -> int:
    summary = run_godproof(
        sessions_root=Path(args.sessions_root) if args.sessions_root else None,
        query=args.query,
    )
    console = Console()
    console.rule("Katala Research — God proof frontier")
    console.print_json(data=summary)
    console.print(f"\n[bold]Report[/]: {summary['report_path']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="kr",
        description="Katala Research — anti-filter-bubble deep-research agent.",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    run_p = sub.add_parser("run", help="Run a research session.")
    run_p.add_argument("query", help="Research query (wrap in quotes).")
    run_p.add_argument("--prefs", help="Path to a research-prefs.yaml override.")
    run_p.add_argument("--sessions-root", help="Override the sessions root dir.")
    run_p.add_argument("--breadth", type=int, help="Override default_breadth.")
    run_p.add_argument("--depth", type=int, help="Override default_depth.")
    run_p.add_argument("--stub", action="store_true",
                       help="Use stub backends (no network / no API key required).")
    run_p.set_defaults(func=_cmd_run)

    bench_p = sub.add_parser("bench", help="Run the DRB-5 + creativity rubric smoke.")
    bench_p.add_argument("--tasks", type=int, default=5)
    bench_p.add_argument("--stub", action="store_true",
                         help="Run bench with stub backends (fast, deterministic).")
    bench_p.add_argument("--sessions-root", help="Override the sessions root dir.")
    bench_p.set_defaults(func=_cmd_bench)

    cfg_p = sub.add_parser("config", help="Show resolved configuration.")
    cfg_p.add_argument("--prefs", help="Path to a research-prefs.yaml override.")
    cfg_p.set_defaults(func=_cmd_config)

    god_p = sub.add_parser(
        "godproof",
        help="Build a local proof-frontier graph for God-existence arguments.",
    )
    god_p.add_argument(
        "--query",
        default="God proof proof-frontier",
        help="Session label/query for the generated log directory.",
    )
    god_p.add_argument("--sessions-root", help="Override the sessions root dir.")
    god_p.set_defaults(func=_cmd_godproof)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
