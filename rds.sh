#!/bin/sh

cat kurzy_debugv.py > kurzy.py
sed -i 's/#DEBUG_START.*#DEBUG_END//'

exit 0
