import argparse
import glob
import inspect
import itertools
import json
import os
import traceback
from pathlib import Path

from .grader import Grader

GRADE_FUNC_SUFFIX = "_grade"

def main(args):
    minimal_globals = lambda: {"__builtins__": __builtins__}

    import_globals = minimal_globals()
    # TODO: Add sys.meta_path filter inside the globals to control what students can import
    assert args.code, "There must be at least one --code source file"
    assert args.test, "There must be at least one --test testset"

    for import_file_path, import_file in itertools.chain(*args.code):
        import_globals["__file__"] = str(import_file_path.resolve())
        exec(import_file, import_globals)

    graders = {}
    for test_file_path, test_file in itertools.chain(*args.test):
        test_global = {**minimal_globals(), "__file__": str(test_file_path.resolve()) }
        exec(test_file, test_global)

        # Now we pass each test function a grader object:
        for key, grading_func in test_global.items():
            if key.startswith("_") or not key.endswith(GRADE_FUNC_SUFFIX):
                continue
            func_name = key[:-len(GRADE_FUNC_SUFFIX)]
            # Find function by name:
            graders[func_name] = Grader(func_name=func_name)
            if func_name not in import_globals:
                print(f"ERROR: CANNOT FIND FUNCTION {func_name}")
                continue

            graded_func = import_globals[func_name]
            try:
                grading_func(graders[func_name], graded_func)

            except Exception as exc:
                print(f"ERROR: UNCAUGHT EXCEPTION DURING GRADING")
                print("\n".join(traceback.format_exception(etype=type(exc), value=exc, tb=exc.__traceback__)))

    if len(graders) == 0:
        print(f"ERROR: NO GRADING FUNCTIONS FOUND")

    scores = { k: v.get() for k, v in graders.items()}
    scoreboard = [ sum(g.get() for g in graders.values()) ]
    return json.dumps({ "scores": scores, "scoreboard": scoreboard })

def read_file(p):
    files = [Path(f) for f in glob.glob(p)]
    return [(f, f.read_text()) for f in files if f.suffix == ".py"]

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Autolab Grader for Jupyter Notebooks")
    p.add_argument("--code", nargs="+", type=read_file)
    p.add_argument("--test", nargs="+", type=read_file)

    scores = main(p.parse_args())

    print()
    print("="*80)
    print(scores)
