#!/bin/bash
python translate/translate.py \
  --file TwitterUSAirline.csv \
  --link https://drive.google.com/file/d/1yRrk8Yyt6Inv-KdpB3NC5tQ2DPhpQ2Me/view?usp=drive_link \
  --start_index 0 \
  --end_index 1000
