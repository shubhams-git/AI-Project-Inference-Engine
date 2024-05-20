import os
import unittest
import subprocess
from tqdm import tqdm


class TestInferenceEngine(unittest.TestCase):
    """
    Unit test class for the Inference Engine.
    """
    kb_files = [
        # Horn-based KB (test1.txt)
        {"file_content": "TELL\np2=> p3; p3 => p1; c => e; b&e => f; f&g => h; p2&p1&p3 => d; p1&p3 => c; a; b; p2;\nASK\nd", "filename": "test_1.txt", "methods": ["FC", "BC", "TT", "RP"]},
        
        # General KB (test2.txt)
        {"file_content": "TELL\n(a <=> (c => ~d)) & b & (b => a); c; ~f || g;\nASK\nd", "filename": "test_2.txt", "methods": ["TT", "RP"]},
        
        # Complex Query (test3.txt)
        {"file_content": "TELL\n(a <=> (c => ~d)) & b & (b => a); c; ~f || g;\nASK\n~d & (~g => ~f)", "filename": "test_3.txt", "methods": ["TT", "RP"]},
        
        # Additional Horn-based KB (test4.txt)
        {"file_content": "TELL\nq1 => q2; q2 => q3; q3 => q4; q1; q5 => q6; q6 => q7; q7 => q8; q5;\nASK\nq4", "filename": "test_4.txt", "methods": ["FC", "BC", "TT", "RP"]},
        
        # General KB with mixed operators (test5.txt)
        {"file_content": "TELL\n(m => n) & (~n => p) | q; r <=> (s & t); u & (v || ~w);\nASK\np", "filename": "test_5.txt", "methods": ["TT", "RP"]},
        
        # Complex Query (test6.txt)
        {"file_content": "TELL\n(x => y) & (y <=> z) & (z => ~w); a & b & (c || d);\nASK\n~w & (~d => a)", "filename": "test_6.txt", "methods": ["TT", "RP"]},
        
        # Horn-based KB with conjunctions (test7.txt)
        {"file_content": "TELL\nr1 => r2; r2 => r3; r3 & r4 => r5; r1; r4;\nASK\nr5", "filename": "test_7.txt", "methods": ["FC", "BC", "TT", "RP"]}
    ]

    @classmethod
    def setUpClass(cls):
        """
        Set up the class by creating test files in the 'tests' directory.
        """
        os.makedirs("tests", exist_ok=True)
        for kb in cls.kb_files:
            with open(f"tests/{kb['filename']}", "w") as f:
                f.write(kb["file_content"])

    def run_inference_engine(self, method, test_file):
        """
        Run the inference engine with the specified method and test file.
        
        :param method: The inference method to use (e.g., 'TT', 'FC', 'BC', 'RP').
        :param test_file: The path to the test file.
        :return: The output of the inference engine.
        """
        command = ["python", "InferenceEngine.py", method, test_file]
        result = subprocess.run(command, capture_output=True, text=True)
        return result.stdout.strip()

    def test_inference_engine(self):
        """
        Run the inference engine tests and collect the results.
        """
        results = []
        test_case_number = 1
        with tqdm(total=sum(len(kb["methods"]) for kb in self.kb_files)) as pbar:
            for kb in self.kb_files:
                for method in kb["methods"]:
                    with self.subTest(test_file=kb["filename"], method=method):
                        output = self.run_inference_engine(method, f"tests/{kb['filename']}")
                        results.append((test_case_number, method, kb["filename"], output))
                        pbar.update(1)

                        # Validate output format
                        if method == "TT":
                            self.assertTrue(output.startswith("YES:") or output == "NO", "TT output should be 'YES: <count>' or 'NO'")
                        elif method in ["FC", "BC"]:
                            self.assertTrue(output.startswith("YES:") or output == "NO", "FC/BC output should be 'YES: <symbols>' or 'NO'")
                        elif method == "RP":
                            self.assertIn(output, ["YES", "NO"], "RP output should be 'YES' or 'NO'")

                        test_case_number += 1

        self.generate_report(results)

    def generate_report(self, results):
        """
        Generate an HTML report summarizing the test results.
        
        :param results: A list of tuples containing test case number, method, filename, and output.
        """
        os.makedirs("test_reports", exist_ok=True)
        with open("test_reports/summary_report.html", "w") as report:
            report.write("<html><head><title>Test Summary Report</title></head><body>")
            report.write("<h1>Inference Engine Test Summary Report</h1>")
            report.write("<table border='1'>")
            report.write("<tr><th>Test Case</th><th>Method</th><th>File</th><th>Output</th></tr>")
            for result in results:
                test_case, method, filename, output = result
                report.write(f"<tr><td>{test_case}</td><td>{method}</td><td>{filename}</td><td>{output}</td></tr>")
            report.write("</table></body></html>")

if __name__ == "__main__":
    unittest.main()