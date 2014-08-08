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

rep = Report()

# discover the directory
def discover():
    # discover the problem problems
    def discover_problems(dpath):
        meta_file = os.path.join(dpath, "meta.json")

        if not os.path.isfile(meta_file):
            sys.stderr.write("Cannot find problem meta file\n")
            exit(1)

        try:
            _meta = simplejson.load(file(meta_file))
        except Exception as e:
            raise Exception("Failed to load problem json file: %s" % str(e))

        _list = _meta.get("list", None)

        if _list is None:
            sys.stderr.write("Cannot find key `list` in meta file\n")
            exit(1)

        for p in _list:
            pfile = os.path.join(dpath, p + ".md")

            if not os.path.isfile(pfile):
                sys.stderr.write("Cannot find md file for problem `%s`\n" % p)
                exit(1)

            rep.add_problem(pfile, file(pfile).read())

    # List up the directory
    for f in os.listdir(WORK_DIR):
        fpath = os.path.join(WORK_DIR, f)

        if os.path.isfile(fpath):
            if f == "meta.json":
                _meta = simplejson.load(file(fpath))
                rep.update_meta(_meta)
            elif f == "overview.md":
                rep.set_section("overview", file(fpath).read())
            elif f == "process.md":
                rep.set_section("process", file(fpath).read())
            elif f == "summary.md":
                rep.set_section("summary", file(fpath).read())
            else:
                sys.stderr.write("Warning: Unkown section file: %s\n" % fpath)
        elif os.path.isdir(fpath):
            if f == "problems":
                discover_problems(fpath)
            else:
                sys.stderr.write("Warning: Unkown directory: %s\n" % fpath)
        else:
            sys.stderr.write("Warning: Unkown file type: %s\n" % fpath)

# use xelatex to compile
def make():
    _latex = rep.generate_latex()

    lfile = os.path.join(WORK_DIR, rep.get_report_file_name() + ".tex")
    file(lfile, "w").write(_latex)

    import subprocess
    p = subprocess.Popen(["xelatex", lfile])

    p.wait()


def run():
    discover()
    make()

if __name__ == "__main__":
    run()
