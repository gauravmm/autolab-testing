# Autolab Testing

Simple nose-like testing framework for Python, with AutoLab adapter.

Run it with:

```shell
python3 -m autograder --code user_code.py --test test_one.py --test test_two.py
```

The `--code` command imports (one or more) python files into a single, common, namespace. You should convert Jupyter notebooks to a python script using `jupyter nbconvert --to script [YOUR_NOTEBOOK].ipynb`.

The `--test` command imports python files into individual namespaces distinct from the common import namespace. All functions with names ending in `<base_name>_grade` are called with the function `<base_name>` and a Grader object. You can use that object with:

```python
# From --code submission.py:
def successor(i):
    return i + 1

# From --test tests.py
def successor_grade(grade, successor):
    # Check for simple equality:
    grade.equal(successor(-1), 0, score=2)
    grade.equal(successor(0), 1, score=1)
    grade.equal(successor(1), 2) # All asserts are worth 1 point by default.

    # Arbitrary assert statement:
    grade.true(successor(2) == 3)

    # Thrown error:
    grade.exception(successor({}))
```
