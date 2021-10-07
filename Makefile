TITLE="EPIC3 UBNT_1101_Relays"

PKG_NAME="UBNT_1101_Relays"
PKG_VERSION="1.1"
PKG_RELEASE=3

MODULE_FILES=relays.py
MODULE_FILES_DIR=/usr/lib/python3.8/

.PHONY: all install

all: install

install:
	for f in $(MODULE_FILES); do cp $${f} $(MODULE_FILES_DIR); done

clean:
	for f in $(MODULE_FILES); do rm -f $(MODULE_FILES_DIR)$${f}; done
