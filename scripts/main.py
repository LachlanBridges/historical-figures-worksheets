import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: main.py {build,download,generate,merge,merge-toc,sort} [args...]")
        return

    command = sys.argv[1]
    args = sys.argv[2:]

    if command == "build":
        from cli import build_latex
        sys.argv = ["build_latex.py"] + args
        build_latex.run()
    elif command == "download":
        from cli import download_images
        sys.argv = ["download_images.py"] + args
        download_images.run()
    elif command == "generate":
        from cli import generate_figures
        sys.argv = ["generate_figures.py"] + args
        generate_figures.run()
    elif command == "merge":
        from cli import merge
        sys.argv = ["merge.py"] + args
        merge.run()
    elif command == "merge-toc":
        from cli import merge_pdfs_with_toc
        sys.argv = ["merge_pdfs_with_toc.py"] + args
        merge_pdfs_with_toc.run()
    elif command == "sort":
        from cli import sort_figures
        sys.argv = ["sort_figures.py"] + args
        sort_figures.run()
    else:
        print(f"Unknown command: {command}")
        print("Usage: main.py {build,download,generate,merge,merge-toc,sort} [args...]")

if __name__ == "__main__":
    main()
