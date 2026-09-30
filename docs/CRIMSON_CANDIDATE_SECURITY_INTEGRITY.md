# Crimson Candidate Security & Integrity Contract

The generated v0.1 candidate is treated as an isolated package, not as trusted output merely because the builder produced it.

## Registration containment
Every gameplay registration in candidate `mod.json` must:
- use the exact reviewed production-style relative path;
- remain below candidate `Content/`;
- contain no absolute path;
- contain no `..` traversal;
- resolve to a non-empty file.

## Manifest containment
`candidate-manifest.json` is a deterministic SHA-256 inventory. Every manifest path must be relative and traversal-free.

The verifier compares both directions:
1. every manifest entry must exist and match byte size + SHA-256;
2. every actual candidate file (except the report and manifest themselves) must be represented in the manifest.

This prevents an untracked file from being silently added after the manifest is generated and prevents a tracked file from being changed or removed without detection.

## Asset verification
Direct quoted media are re-scanned independently from generated configs. Siege and puzzle resources are independently reconstructed from their prefixes. Builder counters are therefore evidence only; the verifier recomputes the candidate state.

## Boundary
These checks prove package closure/integrity, not VCMI gameplay correctness. Runtime gates remain blocked until the real media exist and the candidate passes local VCMI 1.7.5 loading, battle, town, siege, save/reload and rollover tests.
