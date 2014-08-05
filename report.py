class Report(object):
    def __init__(self, metas=None):
        self.update_meta(metas)

    def update_meta(self, metas):
        if not metas:
            metas = {}

        if not hasattr(self, "_metas"):
            self._metas = {}

        self._metas.update(metas)

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
        return ""
