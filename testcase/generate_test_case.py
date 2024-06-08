import os
import glob
import json
import jinja2


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(path, "..", "templates")
    single_template_file = os.path.join(template_dir, "gen_test_case_end2end_single.tmpl")
    func_files = glob.glob(os.path.join(path, "func_data", "func_*.txt"))
    for i, func_file in enumerate(func_files):
        with open(func_file, "r") as f:
            func_desc = f.read()
        prompt_template = jinja2.Template(single_template_file)
        prompt = prompt_template.render({"function_description": func_desc})
    
    


