id: L0007
date: 2026-09-27
area: stego
tags: stego,lsb,png,channels
title: RGB-channel LSB stego: split channels first
context: dl/c29_qqqqqrrrrrrrr.png (chal 29 QRRRR HELLLL 2.0)
trigger: Whole-image LSB extraction yields noise; the payload is split across channels with different per-channel processing.
fix: Extract per-channel LSB planes to separate files (R,G,B), analyse each independently, then combine (xor/max/min/mean/sum-clip). The 'q'/'r'-heavy filename ~
verify: python3 -c "from PIL import Image; im=Image.open('dl/c29_qqqqqrrrrrrrr.png').convert('RGB'); [open(f'dl/lsb_{c}.png','wb').write(bytes(255-b for b in im.split()[i].tobytes())) for i,c in enumerate('RGB')]" && ls -l dl/lsb_*.png
transfer: Any PNG stego where zsteg/steghide fail: split RGB first, then per-channel statistics, bit-order reversal, and 2-bit groupings.
---

## Trigger — why this was hard
    Whole-image LSB extraction yields noise; the payload is split across channels with different per-channel processing.
## Wrong assumptions discarded
    Assumed one LSB plane held the flag and that a generic stego tool would find it.
## Actual root cause / what worked
    Extract per-channel LSB planes to separate files (R,G,B), analyse each independently, then combine (xor/max/min/mean/sum-clip). The 'q'/'r'-heavy filename hinted at channel-differential content.
## Verification (the command that proves it)
    python3 -c "from PIL import Image; im=Image.open('dl/c29_qqqqqrrrrrrrr.png').convert('RGB'); [open(f'dl/lsb_{c}.png','wb').write(bytes(255-b for b in im.split()[i].tobytes())) for i,c in enumerate('RGB')]" && ls -l dl/lsb_*.png
## Transfer — reuse this when
    Any PNG stego where zsteg/steghide fail: split RGB first, then per-channel statistics, bit-order reversal, and 2-bit groupings.
