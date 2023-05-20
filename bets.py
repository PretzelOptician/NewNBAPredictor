from get_curr_spreadsheets import *
from apply_ml_model import *
from apply_regression_model import *
import sys

mode_functions = {
    "all": [get_current_spreadsheets, get_regression_probs, get_ml_probs],
    "generate": [get_current_spreadsheets],
    "regression": [get_regression_probs],
    "ml": [get_ml_probs],
    "betsonly": [get_regression_probs, get_ml_probs]
}

def main(mode, notweet=False):
    if mode in mode_functions:
        for func in mode_functions[mode]:
            if func != get_current_spreadsheets:
                func(notweet)
            else: 
                func()
    else:
        print("Invalid mode selected")

if __name__ == "__main__": 
    if len(sys.argv) == 1: 
        mode = "all"
    else: 
        mode = sys.argv[1]
    notweet = len(sys.argv) > 2 and sys.argv[2] == "notweet"
    main(mode, notweet)