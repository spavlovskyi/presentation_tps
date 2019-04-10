#!/bin/bash

set -ex

reference=fipscanister/2.0.16@local/stable
conan create . $reference -s build_type=Debug
conan upload --all $reference
