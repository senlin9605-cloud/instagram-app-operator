# Mirror input diagnosis

Read when Chinese input or paste fails. The current host documentation defines API signatures; these observations describe one session, not product-wide guarantees.

## Evidence: 2026-10-10, Spotlight

- Used Codex-native `cua_repl`, bound `com.apple.ScreenContinuity`, raised the observed window, opened Spotlight with `super+3`, and clicked the current search field.
- `paste("闲鱼", {format:"text"})` returned without an error twice but subsequent screenshots showed an empty field, including after re-raising/refocusing.
- `typeText("闲鱼")` also left the field empty.
- `paste("xianyu", {format:"text"})` left the field empty; immediately following `typeText("xianyu")` entered the full query and produced the native Xianyu result.
- The Mac Edit menu's Paste item was disabled, including after the field had received ASCII typing. This is not evidence that every iOS field forbids paste; the outer Mac menu may not reflect iOS editing support.
- The installed JS wrapper forwards the text and format to the native paste action. Source inspection alone does not prove clipboard delivery to the phone.
- No shell clipboard writes, raw key synthesis, permissions changes, or additional drivers were used.

## Follow-up: verified alternative, same day

- Native `paste("中文测试")` worked in a newly created blank Mac TextEdit document, verified through AX text. This establishes working Chinese paste in that native Mac field, not in every app.
- After normal Mac Copy and `mirror.pressKey("super+v")`, Xianyu displayed a paste-permission prompt. The user explicitly approved, and the assistant allowed it. The resulting text was `中文粘贴`, different from the earlier intended `中文测试`; do not count this as a controlled exact-content success.
- After approval, native `mirror.paste("闲鱼", {format:"text"})` inserted the old `中文粘贴` string into Spotlight rather than the requested string. This demonstrates stale-content behavior for that call.
- Controlled test 1: set the isolated TextEdit document to `闲鱼测试42`, verify its AX value, select/copy it normally, clear/refocus Spotlight, and use `mirror.pressKey("super+v")`. The new screenshot's query suggestion displayed the exact string `闲鱼测试42`.
- Controlled test 2: repeat with `中文验证73`; the screenshot displayed the exact new string, including `73`.
- No search submission, messages, account actions, shell clipboard writes, private driver, or security-setting changes were used.

## Normal-copy fallback

Use only for text and destination authorized by the user. Inform the user this deliberately replaces their clipboard and ask them not to copy/type/switch windows during the short transfer. Do not inspect or print their prior clipboard contents for diagnosis.

1. Create an independent empty scratch document in a native Mac editor. Do not modify whatever user document the editor initially has open. Avoid placing sensitive text in an autosaving/iCloud editor; use an appropriate approved scratch surface or hand off when confidentiality is uncertain.
2. Bind and observe that scratch window. Use its current editable AX field with `setValue(index, intendedText)` or native `paste(intendedText)`, and verify that its actual value matches the intended text.
3. Raise/focus the scratch window **before** selecting/copying; use current AX indices, not index 2 remembered from a prior window. Verify its field value, then use documented native `super+a` and `super+c`, and confirm the selected text. These shortcuts were tested in TextEdit, not guaranteed for arbitrary editors. Do not copy if source identity/value has not been verified.
4. Rebind/observe the mirror; use the current window's `Raise` action if available. Clear only the authorized target field, verify it is empty, and refocus it. Use `await mirror.pressKey("super+v")` without another `mirror.paste(...)` operation in between.
5. Inspect any permission prompt. Obtain the confirmation required by the current host policy before allowing paste; a prompt is a separate branch, not something to click blindly. The previous approval for one app/text is not blanket authority for every future app or sensitive payload.
6. Observe and compare the **exact** resulting text, including a unique suffix during tests. A suggestion is supplementary evidence, not proof of the editable field's complete value: in one audited run the suggestion showed the intended string while the field had an extra trailing `v` with active IME composition. When clipped, use an observation that truly exposes the field's tail or mark incomplete verification. A wrong/old string is failure even if it is Chinese.
7. If it fails, check state/focus and allow one evidence-informed retry, not a blind loop. Stop on another identical failure or interruption. Clean up only the scratch document created for this task and leave no unintended submission. Do not claim the previous clipboard has been restored.

## Interpretation and stopping rule

The observations distinguish native temporary paste from normal Copy + mirror Cmd+V. The successful alternative is a workflow workaround, not a patch to Codex or Apple's binaries. Temporary pasteboard restoration/Universal Clipboard timing is a plausible explanation for stale content, **not a confirmed internal root cause**. Paste permission was also an observed blocker. Do not present focus competition or model training as proven causes.

Use the correct text-first paste signature once; after a fresh focus/state check, permit one retry. Verify with a fresh screenshot. If that route fails, use the tested normal-copy fallback when an authorized scratch surface and required permission are available. Otherwise request user assistance rather than silently substituting pinyin for exact Chinese content.

Further internal diagnosis would require relevant native-service/Continuity diagnostics. Avoid reading the user's clipboard or private content merely to diagnose the issue. Do not disable security protections or use a private IPC client as a workaround.

## Audited Qwen follow-up: 2026-10-12

The native CUA path was callable, and Xianyu ultimately opened. The second Chinese field visibly matched the intended marker. The first exact-input claim did not pass: the original screenshot's field contained a trailing `v` that the matching suggestion omitted. Do not turn successful navigation into a blanket pass for input.

The run also invoked exec-only `text()` inside CUA after changing a field, causing `text is not defined`. Some earlier side effects had already occurred. Use `nodeRepl.write` only when output is needed and re-observe after errors before replaying actions.

The report's approximate Retina dimensions and universal claims that `super+a` never works or `Raise` must always be avoided were not established. Actual images were 334×735. Keep tested application-specific behavior distinct from explanations: a stray `v`, stale clipboard, or failed copy does not by itself prove a modifier-key or foreground-routing root cause.

If unexpected private text appears, stop the current copy/paste sequence, do not transcribe it in reports, and re-establish an authorized verified source before a bounded retry. If sensitive data reached an unintended external field, tell the user what happened without repeating the payload; do not continue merely because the eventual target text can be made correct.
