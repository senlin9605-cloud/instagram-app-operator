# Conversation close and GitHub saving

## Local state

Read `~/.codex/instagram-app-operator/local.json`: `repo`, `expected_remote`, `branch`, `scope_roots`, `operations_root`, optional `http_proxy`. Config/status remain local. Reuse only an authorized existing proxy; do not change OS networking or embed credentials.

The operations root contains the private account/device map and per-account activity JSON. Preserve metric labels and nulls for unavailable data. Record targets, actual text when relevant, completion evidence and uncertainty. Do not infer success from pending submissions.

Keep credentials, account/device identities, private metrics, screenshots, media, transcripts and hook payloads outside Git. The local map enables future switching without publishing account setup.

## GitHub contract

Save reviewed general instructions and lessons in this Skill. The agent updates procedures before ending a relevant turn. The helper uses no LLM, reads no transcripts and infers no lessons from messages. No new lesson means no forced rewrite.

The helper uses an explicit file allowlist; verifies remote and branch; and refuses symlinks, extra files, other staged files, conflicts, detached HEADs, divergence and unrelated unpushed commits. It leaves unrelated working changes alone, never force-pushes and never resolves conflicts automatically. Failed pushes keep the local commit. This is not a complete secret scanner: review outgoing text.

## Stop hook

Codex's `Stop` event runs after an agent turn. Add the handler to the existing user `hooks.json`, preserving other entries:

```json
{"hooks":{"Stop":[{"hooks":[{
  "type":"command",
  "command":"python3 '<installed-skill>/scripts/sync.py' --config '<local-config>' --hook",
  "timeout":120,
  "statusMessage":"Save Instagram workflow updates"
}]}]}}
```

Generate absolute paths for this installation. The handler ignores workspaces outside configured roots and saves only this Skill; it does not operate Instagram in the background or archive unrelated conversations.

Non-managed hooks need the user's review/trust through the supported hook UI or CLI `/hooks`. A changed definition requires review again. Do not write trust records, bypass trust, or replace `notify` to avoid this gate. New hooks may load only in a resumed/new session. Until active, the agent explicitly saves at conversation close; distinguish this from a verified lifecycle invocation.

Test the helper with a temporary repository and bare remote. A synthetic payload proves helper behavior, not that the desktop actually invoked Stop. Verify a real invocation in local `sync-status.json` before claiming automatic operation.

Official reference: [Codex lifecycle hooks](https://learn.chatgpt.com/docs/hooks).
