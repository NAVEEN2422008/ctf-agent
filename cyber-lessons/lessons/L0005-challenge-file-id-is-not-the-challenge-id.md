id: L0005
date: 2026-09-27
area: recon
tags: ctfd,ids,submit
title: Challenge file_id is NOT the challenge_id
context: dl.sh <file_id> <out> vs sub.sh <challenge_id> <flag>
trigger: Easy to submit against the wrong challenge, burning attempts and risking rate-limiting or a flag on a teammate's board.
fix: Map via chal.json (challenges[].files[].id -> parent challenge id), or read column 2 of filelist.txt.
verify: jq -r '.challenges[]|select(.files[]?.id==24)|.id' ~/ctf/chal.json
transfer: Any CTFd-style platform where download ids and submission ids are separate spaces.
---

## Trigger — why this was hard
    Easy to submit against the wrong challenge, burning attempts and risking rate-limiting or a flag on a teammate's board.
## Wrong assumptions discarded
    Assumed the integer on a download is the integer to submit. filelist.txt column 1 is a file id; the real challenge id is column 2 / chal.json.
## Actual root cause / what worked
    Map via chal.json (challenges[].files[].id -> parent challenge id), or read column 2 of filelist.txt.
## Verification (the command that proves it)
    jq -r '.challenges[]|select(.files[]?.id==24)|.id' ~/ctf/chal.json
## Transfer — reuse this when
    Any CTFd-style platform where download ids and submission ids are separate spaces.
