---
name: instagram-app-operator
description: Operate Instagram accounts for mobile apps through iPhone Mirroring, including account and device switching, Insights review, relevant community interaction, content preparation and publishing, and saving verified results and reusable workflow improvements. Use for ongoing App account operations; not paid ads or account registration.
---

# Instagram App operator

Run the authorized account task to a verified result. Treat growth as reaching likely app users and improving conversion, not accumulating activity counts.

## Start with identity and scope

- Read `~/.codex/instagram-app-operator/local.json`, its `operations_root`, the account/device map including content and asset-creation preferences, and latest activity record there. Keep these private files outside this skill's Git repository.
- Reuse established authorization for ordinary operations and device switching. Apply the active host confirmation policy to the actual action; do not add blanket approval gates or copy an old policy into this skill.
- Verify the Instagram handle before each account's work and after a device switch or reconnect. An installed App, avatar, similar name or another account's link does not establish identity.
- If an account is unregistered or its mapping is unknown, skip its mutations and continue known accounts. Do not register accounts or repurpose a different brand account without a request.

## iPhone Mirroring

Use [iphone-mirroring-operator](../iphone-mirroring-operator/SKILL.md) for native navigation, input and transfers. For device switching, interruptions or stale frames, read [mirror-recovery.md](references/mirror-recovery.md). Keep UI actions in the available computer-use runtime.

## Choose the next useful action

1. Check notifications and comments on the account's own content first. Answer relevant questions using verified App capabilities. Acknowledge a creator's real response when appropriate. Keep internally owned accounts' activity separate from external audience response.
2. Read recent Insights: observation time, plays, viewers/reach with the displayed metric name, average watch, skips, likes, comments, sends/shares, saves and follows. Record unavailable values as unknown, not zero. Compare similar post ages; make early conclusions provisional and revisit at 72 hours and 7 days.
3. Match research to actual App use cases. Inspect beyond the first search screen when useful. Read media, caption and relevant comments before interacting. Prefer a small set of worthwhile interactions; no quota or invented safe hourly limit is required.
4. Like relevant work and write short comments identifying an actual detail, answering a question or adding a useful observation. Avoid copied praise, promotional links, unsolicited pitches and repeatedly questioning creators just to generate replies.
5. Stop on restrictions, spam warnings, challenges or unresolved errors. Do not change IPs/devices/accounts to evade enforcement. No bought engagement, follow/unfollow loops, repetitive comments, mass DMs or simulated popularity. A low action count does not guarantee compliance.

For strategy and calendars, use `instagram-organic` when installed. Ground decisions in the account's data; generic benchmarks are not promises or platform limits. Verify rules against official Meta/Instagram sources when a decision depends on current policy.

## Prepare and publish when requested

- Follow the user's saved asset-creation route. When they want text, images and video prepared in the conversation, keep creation and review there; do not substitute in-App video generation. If the available tools cannot produce a requested asset, report the limitation instead of changing its source silently.
- When demonstrating App features, use verified App output or workflow with a visible payoff in the opening. Original concepts prepared elsewhere can support relevant content, with accurate provenance and product claims.
- Check the trend's date and source. Identify an AI concept as a concept. Do not present separately generated imagery as an App result unless the App actually produced it.
- Use original/authorized assets, concise captions and a readable cover. Review final media, grid crop, spelling and the complete caption. Apply AI disclosure when required and check music usage rights for the account.
- Base timing on audience Insights when available, otherwise label the slot as a test. Create scheduled work only when requested and supported.
- Observe the final composer and follow existing authorization plus the active host policy. A tap, upload progress or pending status is not completion.
- Verify the visible post/account and completion. For comments, wait for pending status to clear and ordinary Reply/Edit controls. For likes, confirm a selected heart or equivalent state. Re-observe before retrying to avoid duplicate comments or toggling a like off.

## Close every relevant conversation turn

Read [persistence.md](references/persistence.md) for records and GitHub synchronization.

1. Update private activity records with verified actions, metrics, errors, uncertainties and next steps. Preserve mappings/preferences. Do not copy whole transcripts or unrelated phone content.
2. Update [field-notes.md](references/field-notes.md) only for a demonstrated new behavior or correction. Amend the actual procedure for durable lessons; avoid repeated rules or rewriting the Skill for every message.
3. Validate instruction changes; run tests after script changes. Run `python3 <skill-dir>/scripts/sync.py --config ~/.codex/instagram-app-operator/local.json` to save reviewed Skill changes. A trusted Stop hook repeats this idempotently. With no changes, create no empty commit.
4. Report verified completion and concrete blockers briefly. Distinguish local save, commit and verified GitHub push. A Skill cannot activate or trust its own hook.
