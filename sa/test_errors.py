import traceback
import tempfile
import os
import shutil
from sa.runner import invoke_sa

def test_missing_dir():
    try:
        invoke_sa({"entities": []}, {"asrs": [], "non_asr": []}, "/path/that/does/not/exist/for/sure")
        print("FAIL: Missing dir did not raise error")
    except FileNotFoundError:
        print("PASS: Missing dir raised FileNotFoundError")

def test_unwritable_dir():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Make it read-only
        os.chmod(temp_dir, 0o444)
        try:
            invoke_sa({"entities": []}, {"asrs": [], "non_asr": []}, temp_dir)
            print("FAIL: Unwritable dir did not raise error")
        except PermissionError:
            print("PASS: Unwritable dir raised PermissionError")
        finally:
            # Restore permissions to allow cleanup
            os.chmod(temp_dir, 0o777)

if __name__ == "__main__":
    test_missing_dir()
    test_unwritable_dir()
