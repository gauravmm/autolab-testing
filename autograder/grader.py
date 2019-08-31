def impl_equal(value, reference):
    if value == reference:
        return (True, "Passed")
    else:
        return (False, f"Failed: {unicode(value):1000.1000} is not equal to reference value")

def impl_true(prop):
    if prop:
        return (True, "Passed")
    else:
        return (False, f"Assertion failed")

def impl_exception(lmbd, excpt=Exception):
    try:
        lmbd()
    except Exception as e:
        if isinstance(e, excpt):
            return (True, "Passed")
        else:
            return (False, f"Exception type {e}, not subclass of {excpt}")
        return
    return (False, f"No exception thrown.")


class Grader(object):
    def __init__(self, func_name=""):
        self.tests_output = []
        self.score = 0
        self.max = 0
        self.func_name = func_name

    def process(self, passed, output, score=1):
        if len(self.tests_output) == 0:
            print(f"{self.func_name} " + ("=" * (80-len(self.func_name)-1)))
        print(f"[{len(self.tests_output): >3}: {score if passed else 0:0>2}/{score:0>2}] {output}")

        self.max += score
        self.tests_output.append(passed)
        if passed:
            self.score += score

    def get(self):
        return self.score

    def equal(self, value, reference, **kwargs):
        self.process(*impl_equal(value, reference), **kwargs)

    def true(self, prop, **kwargs):
        self.process(*impl_true(prop), **kwargs)

    def exception(self, lmbd, excpt=Exception, **kwargs):
        self.process(*impl_exception(lmbd, excpt), **kwargs)
