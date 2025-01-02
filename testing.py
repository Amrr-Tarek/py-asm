import os
from main import main


def run_code():
    test_files = []
    for file in os.listdir():
        if os.path.isfile(file):
            test_files.append(os.path.abspath(file))

    for i, file_path in enumerate(test_files, 1):  # Run the file on 3 files
        main(["main.py", file_path, rf"output\out{i}.txt", "-h"], "main.py")


def Exit(msg: str, code: int) -> None:
    print("===== Test Failed ======\n")
    print(msg)
    print(f"\n=> The program exitted with code {code}")
    exit(code)


# Testing
def test_file(output_path, correct_path):
    output_path_name = os.path.basename(output_path)
    correct_path_name = os.path.basename(correct_path)

    with open(output_path) as f1, open(correct_path) as f2:
        ln = 1
        for line1, line2 in zip(f1, f2):
            if line1 != line2:
                Exit(
                    f"Error: Difference found at line {ln}:\noutput\\{output_path_name}:\t'{line1}'\ncorrect\\{correct_path_name}:\t'{line2}'",
                    1,
                )
            ln += 1

        for line in f1:
            Exit(
                f"Extra lines in output\\{output_path_name} at line {ln}: {line.strip()}",
                2,
            )
            ln += 1

        for line in f2:
            Exit(
                f"Extra lines in correct\\{correct_path_name} at line {ln}: {line.strip()}",
                3,
            )
            ln += 1


if __name__ == "__main__":
    os.chdir(rf"{os.getcwd()}\testing")
    run_code()
    test_file(r"output\out1.txt", r"correct\out1.txt")
    print("===== Test Passed =====")
