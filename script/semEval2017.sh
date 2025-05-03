#!/bin/bash
python translate/translate.py \
  --file semEval2017.csv \
  --link https://drive.google.com/file/d/1hgHBneFPfMMvGOCfFyBFoN7QANg0CZKl/view?usp=drive_link \
  --start_index 0 \
  --end_index 1000
