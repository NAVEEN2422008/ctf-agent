id: 
date: 2026-11-22
host: REI
area: tooling
tags: ctf,hexdump,decompression,shell
title: xxd -r vs xxd -r -p on full hexdumps
context: bandit12 nested gzip/bzip2/tar decompression
trigger: xxd -r -p produced a file with 4 leading NUL bytes; file -b said 'data' instead of gzip, and a shell loop referenced an unassigned variable then failed to ~
fix: use 'xxd -r data.txt out' (no -p) for standard offset+hex+ASCII dumps; assign f=f after creating the file and again after every gzip/bzip2 branch because those ~
verify: file -b f reports 'gzip compressed data' immediately after xxd -r; loop reaches 'The password is ...'
transfer: When reversing a hexdump that contains offset columns, use xxd -r not xxd -r -p. In iterative decompression loops, re-establish the working filename after each ~
---

## Trigger — why this was hard
    xxd -r -p produced a file with 4 leading NUL bytes; file -b said 'data' instead of gzip, and a shell loop referenced an unassigned variable then failed to reset it after decompression
## Wrong assumptions discarded
    assumed -p (plain) was right for a file that had offset columns; assumed the loop variable stayed valid after gunzip/bunzip2 rewrote the file as f
## Actual root cause / what worked
    use 'xxd -r data.txt out' (no -p) for standard offset+hex+ASCII dumps; assign f=f after creating the file and again after every gzip/bzip2 branch because those tools emit a file named f in the cwd
## Verification (the command that proves it)
    file -b f reports 'gzip compressed data' immediately after xxd -r; loop reaches 'The password is ...'
## Transfer — reuse this when
    When reversing a hexdump that contains offset columns, use xxd -r not xxd -r -p. In iterative decompression loops, re-establish the working filename after each tool rewrites it — never assume the previous path survives.
