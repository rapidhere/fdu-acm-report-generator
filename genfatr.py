from report import Report

import sys
import os
import simplejson

WORK_DIR = os.getcwd()

if len(sys.argv) > 1:
    WORK_DIR = sys.argv[1]

if not os.path.isdir(WORK_DIR):
    sys.stderr.write("Wrong working directory!\n")
    exit(1)

DIST_DIR = os.path.join(WORK_DIR, "dist")

rep = Report()
options = {}

def discover():
    def discover_problems():
        pass

    for f in os.listdir(WORK_DIR):
        fpath = os.path.join(WORK_DIR, f)

        if os.path.isfile(fpath):
            if f == "meta.json":
                _meta = simplejson.load(file(fpath))
                options = _meta.get("options", {})
                rep.update_meta(_meta)
            elif f == "overview.md":
                rep.set_overview(file(fpath).read())
            elif f == "process.md":
                rep.set_process(file(fpath).read())
            elif f == "summary.md":
                rep.set_summary(file(fpath).read())
            else:
                sys.stderr.write("Warning: Unkown section file: %s\n", fpath)
        elif os.path.isdir(fpath):
            if f == "problems":
                discover_problems(fpath)
            else:
                sys.stderr.write("Warning: Unkown directory: %s\n", fpath)
        else:
            sys.stderr.write("Warning: Unkown file type: %s\n", fpath)

def make():
    pass

def run():
    discover()
    make()

if __name__ == "__main__":
    run()
