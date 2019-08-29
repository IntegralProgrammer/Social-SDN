#!/bin/bash
exec unshare -f -p -r ./inner_run_pipeline.sh
