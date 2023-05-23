#!/bin/sh
python3.9 app.py
docker run --rm -v "$(pwd)":/var/loadtest --net host direvius/yandex-tank
