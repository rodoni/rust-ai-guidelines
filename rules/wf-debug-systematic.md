# wf-debug-systematic

> Investigate and resolve bugs through minimal reproduction and evidence-based hypotheses; never guess randomly.

## Why It Matters
Random trial-and-error editing in Rust (such as randomly adding `.clone()`, `Arc<Mutex<T>>`, or `unsafe`) masks underlying architectural flaws and degrades performance. Complex issues involving lifetimes, async deadlocks, or atomics require isolating the minimal failure reproduction and verifying root cause hypotheses before applying changes.

## Bad
```markdown
"The borrow checker is complaining about lifetime 'a. Let me try adding .clone() here.
Now it says cannot borrow as mutable. Let me wrap the struct in Rc<RefCell<T>>.
Now it says cannot cross threads. Let me change it to Arc<Mutex<T>>..."
(Chaotic trial-and-error introducing unnecessary overhead and masking ownership design flaws).
```

## Good
```markdown
### Systematic Debugging Protocol:
1. **Reproduce**: Create a minimal standalone test case in `tests/repro.rs` or `#[test]` reproducing the failure.
2. **Diagnose & Hypothesize**: Analyze compiler diagnostic, stack trace, or run under Miri:
   `cargo miri test --test repro`
3. **Isolate Root Cause**: Determine if the issue is lifetime variance, data race, or missing invariant.
4. **Fix Cirurgically**: Apply minimal, sound fix respecting ownership boundaries.
5. **Verify**: Ensure the reproduction test passes and no new clippy warnings are introduced.
```

## When Acceptable
Simple compile errors caused by obvious typos or recently renamed symbols where the diagnostic pinpoint is unambiguous.
