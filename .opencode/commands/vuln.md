---
description: Nuclei vulnerability scan with severity filtering
agent: webapp
---

Execute Nuclei vulnerability scan against: $ARGUMENTS

## Critical + High
```bash
nuclei -u $ARGUMENTS -t ~/nuclei-templates/ -severity critical,high -o nuclei_critical.txt
```

## All Severity
```bash
nuclei -u $ARGUMENTS -t ~/nuclei-templates/ -severity critical,high,medium,low -o nuclei_all.txt
```

## Specific Tags
```bash
nuclei -u $ARGUMENTS -t ~/nuclei-templates/ -tags cve,rce,sqli,xss -o nuclei_tags.txt
```

## Multiple Targets
```bash
nuclei -l urls.txt -t ~/nuclei-templates/ -severity critical,high -o nuclei批量.txt
```

## Custom Templates
```bash
nuclei -u $ARGUMENTS -t ./custom-templates/ -o nuclei_custom.txt
```

## Stats
```bash
nuclei -u $ARGUMENTS -t ~/nuclei-templates/ -stats -severity critical,high,medium
```
