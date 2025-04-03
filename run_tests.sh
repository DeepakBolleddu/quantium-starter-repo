#!/bin/bash

# Activate the virtual environment
source venv/bin/activate

# Run the test suite
pytest tests/test_app.py -v

# Check the exit code of pytest
if [ $? -eq 0 ]; then
    echo "All tests passed."
    exit 0
else
    echo "Some tests failed."
    exit 1
fi
