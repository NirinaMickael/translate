#!/bin/bash
python translate/translate.py \
  --file sentiment140.csv \
  --link https://drive.google.com/file/d/15xHjrYc0ppQcMwANusnsCXbUECSfqV1t/view?usp=drive_link \
  --start_index 0 \
  --end_index 1000
