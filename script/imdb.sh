#!/bin/bash
python translate/translate.py \
  --file imdb.csv \
  --link  https://drive.google.com/file/d/1qoi4MeKGQsMNDWd_oyWQil87E-paO9vv/view?usp=drive_link \
  --start_index 0 \
  --end_index 1000
