#!/bin/bash
# Generates the src.rpm
mkdir -p ~/rpmbuild/SOURCES
wget https://github.com/projecthamster/hamster/archive/v3.0.3.tar.gz -O ~/rpmbuild/SOURCES/hamster-3.0.3.tar.gz
cp hamster-time-tracker.appdata.xml ~/rpmbuild/SOURCES/
rpmbuild -ba hamster-time-tracker.spec
cp ~/rpmbuild/SRPMS/hamster* .
cp ~/rpmbuild/RPMS/noarch/hamster* .
