set -x
cd _code
python3 lint_check.py
python3 run_tests.py
python3 build_image.py