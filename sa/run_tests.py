from tests.test_runner import test_invoke_sa
import traceback

if __name__ == "__main__":
    try:
        test_invoke_sa()
        print("Test passed successfully!")
    except Exception as e:
        print("Test failed:")
        traceback.print_exc()
