#!/bin/bash

set -ex

rm -rf tmp
version=1.0.2r
ref=OpenSSL/$version@local/stable
git clone https://github.com/conan-community/conan-openssl.git -b release/$version tmp
patch -d tmp -p1 <fips.diff
conan create tmp $ref -u -s build_type=Debug --build=missing -o "&!:shared=True" -o OpenSSL:fips=True
conan upload --all $ref
rm -rf tmp
