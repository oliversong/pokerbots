find $1 -name "Match*.txt" -type f -print0 | xargs -0 python StephenBot/run_replayer.py
