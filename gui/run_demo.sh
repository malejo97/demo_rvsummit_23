#!/bin/bash

pyrcc5 resources.qrc -o resources_rc.py
pyuic5 -x demo_ui.ui -o demo_ui.py
python3 main.py