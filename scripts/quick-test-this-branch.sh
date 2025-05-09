#!/bin/bash

set -eux


src="$(dirname "$(dirname "$(readlink -f "${0}")")")"

LIVEFS_EDITOR="${LIVEFS_EDITOR-$src/livefs-editor}"
[ -d $LIVEFS_EDITOR ] || git clone https://github.com/mwhudson/livefs-editor $LIVEFS_EDITOR

LIVEFS_EDITOR=$(readlink -f $LIVEFS_EDITOR)

old_iso="$(readlink -f "${1}")"
new_iso="$(readlink -f "${2}")"
shift 2

tmpdir="$(mktemp -d)"
cd "${tmpdir}"

PYTHONPATH=$LIVEFS_EDITOR python3 -m livefs_edit $old_iso /dev/null --setup-rootfs \
          --shell 'cp rootfs/var/lib/snapd/seed/snaps/subiquity_*.snap '$tmpdir'/old.snap || \
                   cp rootfs/var/lib/snapd/seed/snaps/ubuntu-desktop-bootstrap_*.snap '$tmpdir'/old.snap'

if [ ! -f old.snap ] ; then
	echo "subiquity-like snap not found"
	exit 1
fi

$src/scripts/slimy-update-snap.sh old.snap new.snap

PYTHONPATH=$LIVEFS_EDITOR python3 -m livefs_edit $old_iso $new_iso --inject-snap new.snap "$@"
