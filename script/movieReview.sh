#!/bin/bash
python translate/translate.py \
  --file movieReview.csv \
  --link https://drive.google.com/file/d/1MOEdvgAr_c156lHR_mObGVSGz3q8gG_6/view?usp=drive_link \
  --start_index 0 \
  --end_index 1000
