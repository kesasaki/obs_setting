"""
AuxAudioDevice1をグローバルソースから各シーンアイテムへ移行するスクリプト。
- JSONルートの AuxAudioDevice1 キーを削除しsourcesへ移動
- マイク不要シーン以外の全シーンにシーンアイテムとして追加
"""

import json
import shutil
from pathlib import Path

SCENES_JSON = Path(__file__).parent / "basic/scenes/無題.json"

NO_MIC_SCENES = {
    "オープニング",
    "エンディング",
    "縦型オープニング",
    "縦型エンディング",
    "サモラン参加型用",
    "マイクラ参加型用",
    "縦型参加型サモラン",
    "縦型参加型マイクラ",
    "イラスト録画用",
    "ショートカットキー箱",
}

MIC_UUID = "35a66a28-47d3-4e92-9985-5773f216a859"


def make_mic_item(next_id: int) -> dict:
    return {
        "name": "マイク",
        "source_uuid": MIC_UUID,
        "visible": True,
        "locked": False,
        "rot": 0.0,
        "scale_ref": {"x": 1920.0, "y": 1080.0},
        "align": 5,
        "bounds_type": 0,
        "bounds_align": 0,
        "bounds_crop": False,
        "crop_left": 0,
        "crop_top": 0,
        "crop_right": 0,
        "crop_bottom": 0,
        "id": next_id,
        "group_item_backup": False,
        "pos": {"x": 0.0, "y": 0.0},
        "pos_rel": {"x": 0.0, "y": 0.0},
        "scale": {"x": 1.0, "y": 1.0},
        "scale_rel": {"x": 1.0, "y": 1.0},
        "bounds": {"x": 0.0, "y": 0.0},
        "bounds_rel": {"x": 0.0, "y": 0.0},
        "scale_filter": "disable",
        "blend_method": "default",
        "blend_type": "normal",
        "show_transition": {"duration": 0},
        "hide_transition": {"duration": 0},
        "private_settings": {},
    }


def migrate():
    # バックアップ
    backup = SCENES_JSON.with_suffix(".json.bak")
    shutil.copy2(SCENES_JSON, backup)
    print(f"Backup: {backup}")

    data = json.loads(SCENES_JSON.read_text(encoding="utf-8"))

    # 1. グローバルキーからsourcesへ移動
    if "AuxAudioDevice1" not in data:
        print("AuxAudioDevice1 not found at root level — already migrated?")
        return

    mic_source = data.pop("AuxAudioDevice1")
    data["sources"].append(mic_source)
    print(f"Moved AuxAudioDevice1 to sources array (uuid: {mic_source['uuid']})")

    # 2. 各シーンにシーンアイテムを追加
    added = []
    skipped = []

    for source in data["sources"]:
        if source.get("id") != "scene":
            continue
        scene_name = source["name"]
        if scene_name in NO_MIC_SCENES:
            skipped.append(scene_name)
            continue

        items: list = source.setdefault("settings", {}).setdefault("items", [])

        # 既に追加済みなら skip
        if any(item.get("source_uuid") == MIC_UUID for item in items):
            print(f"  SKIP (already has mic): {scene_name}")
            continue

        next_id = max((item.get("id", 0) for item in items), default=0) + 1
        items.append(make_mic_item(next_id))
        added.append(scene_name)

    print(f"\nAdded mic to {len(added)} scenes:")
    for name in added:
        print(f"  + {name}")

    print(f"\nSkipped {len(skipped)} scenes (no mic needed):")
    for name in skipped:
        print(f"  - {name}")

    SCENES_JSON.write_text(
        json.dumps(data, ensure_ascii=False, indent=4), encoding="utf-8"
    )
    print(f"\nSaved: {SCENES_JSON}")


if __name__ == "__main__":
    migrate()
