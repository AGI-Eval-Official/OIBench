import evaluate
from datasets import load_dataset
import shutil
import os
import multiprocessing
from code_eval_ojstyle.execute import create_tempdir
import json
LANGUAGE = "C++"
TEST_CASE_NUM = -1
TIMEOUT = 10
NUM_WORKERS = multiprocessing.cpu_count()
os.environ["HF_ALLOW_CODE_EVAL"] = "1"

dataset = load_dataset("AGI-Eval/OIBench")
# pwd this file's directory
cur_dir = os.path.dirname(os.path.abspath(__file__))
code_metric = evaluate.load(os.path.join(cur_dir, "code_eval_ojstyle"))



# number of workers equals to cpu core number 

# len(dataset["test"])
    # the input and output will be saved in the tempdir

def process_test_cases(problem_data, problem_id, tempdir, test_input_files, test_output_files):
    test_case_input_list = []
    test_case_output_list = []
    for test_case in problem_data["test_case"]:
        test_case_input_list.append(test_case["input"])
        test_case_output_list.append(test_case["output"])
    # save the test_case_input_list and test_case_output_list to the tempdir
    for test_case_id, (test_case_input, test_case_output) in enumerate(zip(test_case_input_list, test_case_output_list)):
        with open(f"{tempdir}/problem_{problem_id}_test_case_input_{test_case_id}.txt", "w") as f:
            f.write(test_case_input)
        with open(f"{tempdir}/problem_{problem_id}_test_case_output_{test_case_id}.txt", "w") as f:
            f.write(test_case_output)
    test_input_files.append([f"{tempdir}/problem_{problem_id}_test_case_input_{test_case_id}.txt" for test_case_id in range(len(test_case_input_list))])
    test_output_files.append([f"{tempdir}/problem_{problem_id}_test_case_output_{test_case_id}.txt" for test_case_id in range(len(test_case_output_list))])



if __name__ == '__main__':
    solution_list = []
    test_input_files = []
    test_output_files = []
    # We need to create a tempdir to save the test cases
    with create_tempdir() as tempdir:
        if TEST_CASE_NUM == -1:
            TEST_CASE_NUM = len(dataset["test"])
        for problem_id in range(TEST_CASE_NUM):
            problem_data = dataset["test"][problem_id]
            prob_en = problem_data["prob_en"]        
            process_test_cases(problem_data, problem_id, tempdir, test_input_files, test_output_files)

            # in practive, replace the solution with the response from your model!
            # for example, you can use the following code to get the response from your model:
            # import openai
            # openai.api_key = os.getenv("OPENAI_API_KEY")
            # from code_utils import extract_code
            # solution = openai.ChatCompletion.create(
            #     model="gpt-4o",
            #     messages=[{"role": "user", "content": prob_en}],
            # )
            # solution = extract_code(solution, LANGUAGE)
            solution = problem_data["canonical_solution"]
            solution_list.append([solution])
        
        metrics, cases = code_metric.compute(
            references=[""]*TEST_CASE_NUM,
            predictions=solution_list,
            language=LANGUAGE,
            timeout=TIMEOUT,
            num_workers=NUM_WORKERS,
            test_input_files=test_input_files,
            test_output_files=test_output_files,
        )
        print(metrics)
        json.dump(cases, open(os.path.join(cur_dir, "cases.json"), "w"), indent=4, ensure_ascii=False)
        # clean the tempdir
        shutil.rmtree(tempdir)
    





