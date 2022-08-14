#!/bin/bash
> test_result.log
> test.log

> ml_coretools_config_test.json

pytest -k positive -v | tee -a test_result.log

pytest -k negative -v | tee -a test_result.log

rm ml_coretools_config_test.json