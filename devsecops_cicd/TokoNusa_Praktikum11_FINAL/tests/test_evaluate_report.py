import json
import tempfile
import unittest
from pathlib import Path
from evaluate_report import evaluate

class TestReport(unittest.TestCase):
    def run_case(self, report):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td)/'report.json'
            path.write_text(json.dumps(report))
            return evaluate(path)
    def test_pass(self):
        self.assertEqual(self.run_case({'SchemaVersion':2,'Results':[]}), 0)
    def test_block(self):
        self.assertEqual(self.run_case({'SchemaVersion':2,'Results':[{'Target':'config.py','Secrets':[{'StartLine':20}]}]}), 1)
    def test_fail_closed(self):
        self.assertEqual(self.run_case({'error':'broken'}), 1)

if __name__=='__main__':
    unittest.main()
