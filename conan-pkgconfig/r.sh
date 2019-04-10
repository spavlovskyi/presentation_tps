#!/bin/bash

set -ex
reference=pkg-config/0.28@local/stable
conan create . $reference -s os=Windows
conan upload --all $reference
