---
name: web3-security
description: Smart contract auditing, blockchain security, and DeFi vulnerability assessment.
---

# Web3 Security Skill

## Smart Contract Auditing

### Solidity Analysis
```bash
# Slither (static analysis)
slither . --checklist

# Mythril (symbolic execution)
myth analyze contract.sol

# Securify2
securify2 contract.sol

# Echidna (fuzzing)
echidna-test contract.sol --contract ContractName
```

### Common Vulnerabilities

#### Reentrancy
```solidity
// Vulnerable
function withdraw() external {
    uint balance = balances[msg.sender];
    (bool success, ) = msg.sender.call{value: balance}("");
    require(success);
    balances[msg.sender] = 0;
}

// Fixed
function withdraw() external {
    uint balance = balances[msg.sender];
    balances[msg.sender] = 0; // State change before external call
    (bool success, ) = msg.sender.call{value: balance}("");
    require(success);
}
```

#### Integer Overflow
```solidity
// Vulnerable (Solidity <0.8)
uint balance = balances[msg.sender] + amount; // Overflow possible

// Fixed
uint balance = balances[msg.sender] + amount; // SafeMath or Solidity 0.8+
```

#### Access Control
```solidity
// Vulnerable
function transferOwnership(address newOwner) external {
    owner = newOwner; // No access control
}

// Fixed
function transferOwnership(address newOwner) external onlyOwner {
    owner = newOwner;
}
```

## DeFi Attacks

### Flash Loan Attacks
```solidity
// Borrow flash loan
// Manipulate price oracle
// Profit from price difference
// Repay flash loan
```

### Oracle Manipulation
```solidity
// Use single DEX as price source
// Manipulate price with large trade
// Exploit protocols using manipulated price
```

### Governance Attacks
```solidity
// Flash loan governance tokens
// Vote on malicious proposal
// Return tokens
```

## Tools

```bash
# Contract analysis
slither .
myth analyze .
securify2 .

# Fuzzing
echidna-test . --contract Test

# Symbolic execution
manticore contract.sol

# Manual review
# Check OpenZeppelin docs
# Review access control
# Check for reentrancy
```

## Output Format
```
[VULN] Vulnerability type
[CWE] CWE-XXX
[SEVERITY] Critical/High/Medium/Low
[CODE] Vulnerable code snippet
[FIX] Remediation code
[IMPACT] Potential exploitation
```
