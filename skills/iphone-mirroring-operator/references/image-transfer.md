# Image Transfer Through iPhone Mirroring

Use this workflow to move an explicit set of Mac image files to the user's iPhone and reliably find them in Photos or an iOS photo picker.

## Inputs and boundary

- Absolute paths to the intended images.
- Expected count and intended order.
- The user's specific iPhone as the AirDrop destination.
- The destination app or photo picker when selection is also requested.

Inspect every source image before transmission. Confirm relevance, orientation, legibility, sensitive content, and intended order. Do not infer files from a crowded folder or substitute visually similar images.

Transferring files and any sensitive content must be authorized for the specific files and destination under the active computer-use policy.

## Prepare a safe batch

Place or stage the intended images in a directory that contains images only. Prefix filenames with `01-`, `02-`, and so on when order matters. Keep manifests, notes, and drafts outside that media directory so Finder can safely select all.

## Send with AirDrop

1. In Finder, open the image-only directory, focus one image, select all, and verify the selected count equals the expected count.
2. Choose **Share > AirDrop**.
3. Match a unique recipient name. When the chooser is ambiguous, use iPhone Mirroring to read **Settings > General > About > Name** (`设置 > 通用 > 关于本机 > 名称`). Never guess by device position or icon.
4. If the phone has a generic name, ask the user to give it a durable unique name such as `<owner>-iphone13`. Do not change the name unless the active policy permits the settings change. After a rename, close and reopen the AirDrop chooser to refresh its cached list.
5. Select the exact recipient once and wait for the visible **Sent** (`已发送`) state. Do not resend automatically after an uncertain result.

Fallback to Apple-supported drag and drop through iPhone Mirroring only when the target app visibly accepts the files and the completed import can be verified.

## Verify in Photos

1. In iPhone Mirroring, open **Photos > Collections > Pinned Collections > Recently Saved** (`照片 > 精选集 > 固定 > 最近保存`).
2. Match the expected count and visible content. AirDrop preserves original capture dates, so transferred files may be scattered in the main Library even though they are grouped in Recently Saved.
3. Recently Saved is ordered by save time descending. A numbered batch commonly appears in reverse transfer order, such as `03, 02, 01`; that display order does not change the intended content order.

AirDrop's **Sent** state alone is insufficient. Receipt is complete only after the correct images are visible on the iPhone.

## Select in an iOS photo picker

Use **Images > Photo Library > Collections > Recently Saved** (`图片 > 照片图库 > 精选集 > 最近保存`). Identify each image by content and the source manifest, then tap them in the intended order. Do not assume left-to-right display order equals attachment order. Return to the destination app and inspect every attached thumbnail before continuing.

Do not delete phone photos as part of this workflow. Deletion is a separate destructive action.
