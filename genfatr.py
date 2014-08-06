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
    def discover_problems(dpath):
        meta_file = os.path.join(dpath, "meta.json")

        if not os.path.isfile(meta_file):
            sys.stderr.write("Cannot find problem meta file\n")
            exit(1)

        _meta = simplejson.load(file(meta_file))

        _list = _meta.get("list", None)

        if _list is None:
            sys.stderr.write("Cannot find key `list` in meta file\n")
            exit(1)

        for p in _list:
            sol_file = os.path.join(dpath, p + ".md")
            json_file = os.path.join(dpath, p + ".json")

            if not os.path.isfile(sol_file):
                sys.stderr.write("Cannot find solution file for problem `%s`\n" % p)

            if not os.path.isfile(json_file):
                sys.stderr.write("Cannot find json file for problem `%s`\n" % p)
        
            rep.add_problem(simplejson.load(file(json_file)), file(sol_file).read().decode("utf8"))

    for f in os.listdir(WORK_DIR):
        fpath = os.path.join(WORK_DIR, f)

        if os.path.isfile(fpath):
            if f == "meta.json":
                _meta = simplejson.load(file(fpath))
                options = _meta.get("options", {})
                rep.update_meta(_meta)
            elif f == "overview.md":
                rep.set_overview(file(fpath).read().decode("utf8"))
            elif f == "process.md":
                rep.set_process(file(fpath).read().decode("utf8"))
            elif f == "summary.md":
                rep.set_summary(file(fpath).read().decode("utf8"))
            else:
                sys.stderr.write("Warning: Unkown section file: %s\n" % fpath)
        elif os.path.isdir(fpath):
            if f == "problems":
                discover_problems(fpath)
            else:
                sys.stderr.write("Warning: Unkown directory: %s\n" % fpath)
        else:
            sys.stderr.write("Warning: Unkown file type: %s\n" % fpath)

def make():
    _latex = rep.generate_latex()

    lfile = rep.get_file_name() + ".tex"
    file(lfile, "w").write(_latex)

    import subprocess
    p = subprocess.Popen(["xelatex", lfile])

    p.wait()


def run():
    discover()
    make()

if __name__ == "__main__":
    run()
