# Module 3 Debugging Log and Reflection

1. I intentionally let an invalid status value slip through the validation path, and the API stopped rejecting unsupported status updates.
2. Failing test: test_patch_invalid_status_value_pending_returns_422 — it failed because the request did not produce the expected 422 validation error for the status field.
3. The AI assistant diagnosed the issue as a mismatch between the allowed status enum values and the transition logic, which meant the invalid value was not being blocked correctly.
4. I accepted the fix because it restored the expected validation behavior and kept the API aligned with the test contract.

The VS Code AI assistant helped during frontend work by suggesting where to look for mismatches between the task board UI and the API behavior. One place I had to correct the assistant was when it suggested a broader status list than the app actually allows, so I constrained it to the existing enum values. Inspecting pytest output and the API error details helped me see the real problem instead of guessing. One habit I will reuse in later modules is to read the failing test first, then compare that expectation with the code before accepting a fix.
