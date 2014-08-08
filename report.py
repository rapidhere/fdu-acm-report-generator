import os
import re
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))

class Report(object):
    def __init__(self):
        self._problems = []
        self._metas = {}
        self._sections = {}

    def update_meta(self, metas):
        """
        update the meta info of this report
        """
        if not metas:
            metas = {}

        self._metas.update(metas)

    def get_report_file_name(self):
        """
        get the report file name of this report
        """
        return self._metas.get("report_file_name", "report")

    def get_source_encode(self):
        """
        get the encoding of the source files 
        """
        return self._metas.get("source_encoding", "utf8")

    def get_contest_number(self):
        """
        get the contest number of this report
        """
        # may be int, convert to string
        return str(self._metas.get("contest_number", 1))

    def get_team_name(self):
        """
        get the team name of this report
        """
        return self._metas.get("team_name", "233 Team")

    def set_section(self, section_name, content):
        """
        set the section with content

        section_name must in ["overview", "process", "summary"]
        """
        try:
            self._sections[section_name] = content.decode(self.get_source_encode())
        except UnicodeDecodeError:
            raise Exception("Encode section `%s` with encoding %s failed" % (section_name, self.get_source_encode()))

    def add_problem(self, file_name, solution_text):
        """
        add a problem text into report
        order is important
        """
        try:
            solution_text = solution_text.decode(self.get_source_encode())
        except UnicodeDecodeError:
            raise Exception("Encode solution `%s` with encoding %s failed" % (file_name, self.get_source_encode()))
        self._problems.append(solution_text) 

    @staticmethod
    def _compile_problem(problem):
        """
        Compile the raw problem content

        return the a dict 
        {
            "title": the tile of problem,
            "solution": the solution of problem,
            "members": members who solved this problem,
            "situation": the situation of this problem,
        }
        """
        
        # just use simple re
        def _get(sname):
            ret = re.search("{%% *%s *: *(.+)? *%%}" % sname, problem)

            if not ret:
                return ""

            return ret.groups()[0]

        return {
            "title":        _get("title"),
            "solution":     _get("solution"),
            "members":      _get("members"),
            "situation":    _get("situation"),
        }

    @staticmethod
    def _set_template_content(template, section_name, content):
        """
        repalce the specified template section with content
        raw template will not be modified, will return the generated template
        """
        return template.replace("{%%%s%%}" % section_name, content)

    def generate_latex(self):
        """
        Generate latex content from report object

        Please note there is no cache, everything will generate every time
        """
        # get problem and report template
        tex_template_dir = os.path.join(FILE_DIR, "templates")
        
        # read in and decode with "utf-8"
        _template = file(os.path.join(tex_template_dir, "template.tex")).read().decode("utf8")
        _problem = file(os.path.join(tex_template_dir, "problem.tex")).read().decode("utf8")
        
        # the final compile result
        ret = _template

        # set up the template
        ret = self._set_template_content(ret, "CONTEST_NUMBER",      self.get_contest_number())
        ret = self._set_template_content(ret, "TEAM_NAME",           self.get_contest_number())
        ret = self._set_template_content(ret, "OVERVIEW_CONTENT",    self._sections["overview"])
        ret = self._set_template_content(ret, "PROCESS_CONTENT",     self._sections["process"])
        ret = self._set_template_content(ret, "SUMMARY_CONTENT",     self._sections["summary"])

        # set problems
        prob = u""
        for p in self._problems:
            pmeta = self._compile_problem(p)

            # copy the template
            cprob = _problem
            
            # set up the content
            cprob = self._set_template_content(cprob, "PROBLEM_TITLE",       pmeta["title"])
            cprob = self._set_template_content(cprob, "SITUATION_CONTENT",   pmeta["situation"])
            cprob = self._set_template_content(cprob, "PERSON_LIST_CONTENT", pmeta["members"])
            cprob = self._set_template_content(cprob, "SOLUTION_CONTENT",    pmeta["solution"])
            
            # add to final ret
            prob += cprob
        
        # add problem content into template
        ret = self._set_template_content(ret, "PROBLEMS_CONTENT", prob)

        return ret.encode("utf8")
