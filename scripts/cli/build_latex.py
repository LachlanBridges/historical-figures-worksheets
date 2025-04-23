import argparse
from pathlib import Path
from core.builder import build_latex, build_all

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("json_path", type=Path, nargs="?", help="Path to a specific JSON file")
    parser.add_argument("--no-render", action="store_true", help="Compile existing .tex without regenerating it")
    parser.add_argument("--force", action="store_true", help="Rebuild even if PDF already exists")
    parser.add_argument("--all", action="store_true", help="Process all .json files in the data/ folder")
    args = parser.parse_args()

    if args.all:
        build_all(render=not args.no_render, force=args.force)
    elif args.json_path:
        build_latex(args.json_path, render=not args.no_render, force=args.force)
    else:
        parser.print_help()
