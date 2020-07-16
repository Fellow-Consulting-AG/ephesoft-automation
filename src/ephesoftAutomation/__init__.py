import os.path
import sys

from ephesoftAutomation.helper.main import compare_all_results

# Codee Junaid

def main_compare(
    base_dir,
    config
):
    if not os.path.exists(base_dir):
        return False, "Path provided for base directory does not exist"

    if not os.path.exists(os.path.join(base_dir, config)):
        return False, "Configurations file is missing"

    compare_all_results(base_dir, config)

    return True, "OK"

    #flow.run()