import os
import re

FILE_DIR = os.path.dirname(os.path.realpath(__file__))

class Report(object):
    def __init__(self, metas=None):
        self.update_meta(metas)

    def update_meta(self, metas):
        if not metas:
            metas = {}

        if not hasattr(self, "_metas"):
            self._metas = {}

        self._metas.update(metas)

    def get_file_name(self):
        return self._metas.get("filename", "report")

    def set_overview(self, overview_content):
        self._overview_content = overview_content

    def get_overview(self):
        return self._overview_content

    def set_process(self, process_content):
        self._process_content = process_content

    def get_process(self):
        return self._process_content

    def set_summary(self, summary_content):
        self._summary_content = summary_content

    def get_summary(self):
        return self._summary_content

    def add_problem(self, problem_meta, problem_solution):
        if not hasattr(self, "_problems"):
            self._problems = []

        self._problems.append({
            "meta": problem_meta,
            "solu": problem_solution})

    def generate_latex(self):
        def _set_template_content(template, section_name, content):
            return template.replace("{%%%s%%}" % section_name, content)

        tex_template_dir = os.path.join(FILE_DIR, "templates")

        _template = file(os.path.join(tex_template_dir, "template.tex")).read().decode("utf8")
        _problem = file(os.path.join(tex_template_dir, "problem.tex")).read().decode("utf8")

        ret = _template

        ret = _set_template_content(ret, "CONTEST_NUMBER", str(self._metas["contest_number"]))
        ret = _set_template_content(ret, "TEAM_NAME", self._metas["team_name"])
        ret = _set_template_content(ret, "OVERVIEW_CONTENT", self._overview_content)
        ret = _set_template_content(ret, "PROCESS_CONTENT", self._process_content)
        ret = _set_template_content(ret, "SUMMARY_CONTENT", self._summary_content)

        # set problems
        prob = u""

        for p in self._problems:
            cprob = _problem
            
            cprob = _set_template_content(cprob, "PROBLEM_TITLE", p["meta"]["title"])
            cprob = _set_template_content(cprob, "SITUATION_CONTENT", p["meta"]["situation"])
            cprob = _set_template_content(cprob, "PERSON_LIST_CONTENT", ",".join(p["meta"]["members"]))
            cprob = _set_template_content(cprob, "SOLUTION_CONTENT", p["solu"])

            prob += cprob

        ret = _set_template_content(ret, "PROBLEMS_CONTENT", prob)

        print ret

        return ret.encode("utf8")
