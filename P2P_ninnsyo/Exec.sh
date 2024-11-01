#!/bin/bash

# Pythonのインタラクティブセッションを開きます
python3 -i User.py 10.58.58.97 <<EOF
for i in {1..3}; do
    user.send_query('$i', 3, '10.58.60.06')
done
EOF
