---
name: iphone-mirroring-operator
description: Operate an explicitly requested iOS app or transfer specified images through macOS iPhone Mirroring. Use when the user requests this interface, device verification, or iOS photo-picker selection.
---

# iPhone Mirroring Operator

Operate only the iPhone surface and data needed for the user's current task. Treat every mirrored screen as potentially sensitive.
If the user explicitly requests iPhone Mirroring, do not substitute a browser, API, or connector for that part of the task. Otherwise, use a safer purpose-built interface when it can complete the task without exposing the phone UI.

## Choose the route

- For ordinary navigation, reading, tapping, typing, or scrolling, follow the operating rules below.
- For Mac-to-iPhone image transfer, receipt verification, or photo-picker selection, read [image-transfer.md](references/image-transfer.md).

## Fast app launch (Spotlight)

Tested 2026-10-10: `pressKey("super+3")` opens Spotlight from the home screen and Xianyu. Prefer this route for launching a named app instead of hunting across home pages. Current runtime documentation takes precedence over historical test notes.

1. `pressKey "super+3"` → the app-search screen opens (Siri-suggestions or best-results view).
2. Locate the search pill in the current screenshot and click it to focus the field. Verify entered text rather than assuming focus from an action returning OK. If the screenshot is a blurred transition, observe again before choosing a target.
3. Enter the query:
   - For app-name lookup, use `await mirror.typeText("xianyu")` or the requested app's pinyin/English name. Verify the full query, then confirm the native app's icon and name in the results. Pinyin matched Xianyu in the current test; matching other apps is not guaranteed.
   - For exact Chinese text, the documented native signature is `await mirror.paste("闲鱼", { format: "text" })`. Pass the intended text directly; do not call `paste()` without arguments or prewrite the clipboard with shell commands. The native API manages the Mac pasteboard. This correct signature does **not** guarantee that the iPhone field receives the text.
   - If native `paste(text)` leaves the field empty **or inserts old clipboard content**, stop that route after one state-informed retry. A tested alternative is to put the exact authorized text in an independent Mac scratch editor, verify it, copy it normally with `super+c`, then focus the mirrored field and use the documented `mirror.pressKey("super+v")`. This keeps known clipboard content available for Universal Clipboard instead of relying on native `paste`'s temporary pasteboard operation. Read [input-diagnostics.md](references/input-diagnostics.md) before using this fallback, including permissions, clipboard side effects, scratch cleanup, and exact-content verification.
   - Pinyin is a fallback for app lookup, not a substitute when the user requires exact Chinese content. Chinese `typeText` failed in the current mirror tests; this is not a universal ASCII-only guarantee or proof of a Qwen defect.
4. Read the current search-results screenshot and identify the app by its icon **and** adjacent name or context. Prefer a clearly identified native-app card near the top; if absent, inspect the current results below it. The order of rows in the Settings section can change between identical searches. Never reuse a row's y-coordinate from a prior screenshot. Crop or measure the current candidate when its small icon is hard to locate, then click its center and verify the requested app opened. A color match alone is insufficient.
5. To replace an existing query, prefer the visible × control and click the field again, then verify the replacement. An earlier session lost the first character after `super+a` followed by `typeText`; this is a historical warning, not a universal ban on selection. `BackSpace` removes characters but is not a whole-field clear command.

Coordinate discipline: obtain the current screenshot's actual dimensions from bytes/metadata, not from a zoomed preview. Do not assume 2x Retina, halve coordinates, or add title-bar offsets without current runtime mapping evidence. When using `qwen-codex-computer-use`, its screenshot-dimensions helper can measure PNG/JPEG bytes. The mirror may show the Mac cursor at the tap location; use that as a calibration clue after a miss. Recheck the target from a fresh screenshot rather than nudging a guessed coordinate.

Exact-input gate: inspect the entire editable field, not just a matching suggestion. A trailing `v` or active IME composition makes `中文验证84v` a failure for the requested `中文验证84`, even when the suggestion omits the suffix. Do not infer literal spaces from font gaps. If the end of the field is not readable, report incomplete verification before using the query.

Do not work around failed native input with CGEvent, AppleScript, private sockets, or an extra driver. Earlier raw Cmd+V tests produced a literal "v", but the **documented native** `mirror.pressKey("super+v")` successfully pasted Chinese in the current test; keep these paths distinct.

## Operating rules


1. Use the available computer-use interface and bind the macOS app by bundle identifier `com.apple.ScreenContinuity` when possible. This works across localized app names such as `iPhone镜像`.
2. Observe the current screen before acting. After every navigation or input action, observe again and derive fresh accessibility elements or screenshot-relative coordinates. Never reuse coordinates after the window or screen changes.
3. Prefer labeled accessibility controls. For unlabeled iOS content, use the current screenshot and click only a visually unambiguous target.
4. Follow the current runtime's app-specific scroll instructions. Earlier home-screen scroll and drag tests were unreliable; do not turn them into a fixed gesture recipe. Use Spotlight for app lookup. Re-observe after navigation because the screen may still be animating.
5. Use the mirror's Home shortcut (`pressKey "super+1"`) to leave an app and return to the home screen. Do not invent swipe gestures when a supported control is available.
6. For feed, search, or comment research, look beyond the first screen when results permit. Re-observe after each scroll and continue while additional content changes the conclusion; stop when the sample is sufficient or results repeat.
7. For long visual threads, save task-relevant screenshots locally when they help compare content later; keep them out of version control and avoid unrelated personal information. Do not prescribe interaction timing or patterns to evade platform detection.
8. Keep inspection narrow. Do not browse Messages, Mail, Photos, health, finance, passwords, chats, or other personal content unless that exact surface is required by the user-requested task.
9. Follow the active computer-use confirmation policy for uploads, sensitive-data transmission, settings changes, deletion, communication, purchases, and other consequential actions. A request to inspect the phone is not blanket permission for those actions.
10. The mirror's accessibility tree exposes only the outer macOS window; mirrored iPhone content has no AX elements. Plan mirrored work as vision-based and read each screenshot before acting.
11. Before every click, verify the latest screenshot shows no modal dialog. iOS system alerts (e.g. the accessory-permission prompt "允许配件连接?") can appear spontaneously, dim the home screen, and invalidate all coordinates; dismiss them first, preferring the non-permitting button unless the task requires the permission.
12. A screenshot can be captured mid-transition (page-snap animation, black launch frame). If it does not match the expected state, capture once more before deriving coordinates.
13. Pixel measurement is useful when the iOS canvas has no AX element and nearby targets look alike. Restrict measurement to the relevant region of the current screenshot, then confirm the candidate against its label, shape, or surrounding result. Do not encode a particular app color, fixed row order, or 334×735 coordinates as a general rule.
14. Reduce focus competition: ask the user to avoid typing, switching windows, or copying during a short input test. If the current AX window exposes `Raise`, use `performSecondaryAction(currentWindowIndex, "Raise")` before input, then focus the current field. This native route worked in the current test; it is not proof of permanent foreground ownership. Use only `cua_repl` for UI control and verify the resulting field, rather than requiring shell-based activation.
15. Use key names documented by the runtime. Earlier tests favored `BackSpace` over lowercase `backspace`; do not treat an OK return as proof that the phone received the key.

## Connection handling

- A ready mirror shows the iPhone screen and the mirror's Home/App Switcher controls.
- If the app reports that the iPhone is in use, the phone normally must be physically locked before mirroring can resume. Attempt the visible Connect control once only when phone access is part of the current request; if the state persists, ask the user to lock the phone and stop retrying.
- For `连接中断`, locate the current `重试` control and retry once. If it becomes `未找到 iPhone`, stop and ask the user to check proximity and Continuity readiness, following the app's current instructions about phone lock state. Do not prescribe unlocking if the app requires a locked phone for mirroring.
- Reddit on this iPhone may require the Shadowrocket proxy. If Reddit does not load, open Shadowrocket through Home or Spotlight and inspect its current state. A known-good state has the top connection switch enabled and `全局路由` set to `代理`; the particular selected node is not a permanent requirement. If the proxy is off, request any confirmation required for changing VPN settings immediately before enabling it. Do not switch nodes, edit subscriptions, or change routing rules unless the user explicitly requests that change. Return to Reddit and verify that fresh feed content loads; if it still fails, report the visible error instead of repeatedly cycling the proxy.
- If VPN or local networking blocks Continuity, report the blocker. Do not change VPN, AirDrop visibility, Bluetooth, Wi-Fi, or other system settings without the authorization required by the active policy.

## Completion

Do not treat a tap or transfer attempt as success. Verify the requested app state, data, or image batch visibly on the iPhone, then stop without exploring unrelated content.

Keep failure and privacy evidence accurate: report unexpected clipboard contents as `[unexpected private clipboard content]`, never transcribe a private address/string. Do not mark all tests successful because the final app opened. Create and verify an independent scratch window before editing it; an existing `未命名` window is not proof of isolation. Document cleanup only if it actually happened.
