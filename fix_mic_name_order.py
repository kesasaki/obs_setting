"""
AuxAudioDevice1（共通マイク）のリネームと順序修正。
- ソース名: "マイク" → "マイク（共通）"
- 各シーンのシーンアイテム名も同様に変更
- 各シーンのitemsの先頭に移動（= OBSソースリストの一番下）
"""

import json
import shutil
from pathlib import Path

SCENES_JSON = Path(__file__).parent / "basic/scenes/無題.json"
MIC_UUID = "35a66a28-47d3-4e92-9985-5773f216a859"
NEW_NAME = "マイク（共通）"


def fix():
    backup = SCENES_JSON.with_suffix(".json.bak2")
    shutil.copy2(SCENES_JSON, backup)
    print(f"Backup: {backup}")

    data = json.loads(SCENES_JSON.read_text(encoding="utf-8"))

    # 1. sourcesのAuxAudioDevice1ソース名を変更
    for source in data["sources"]:
        if source.get("uuid") == MIC_UUID:
            source["name"] = NEW_NAME
            print(f"Renamed source: {NEW_NAME}")
            break

    # 2. 各シーンのシーンアイテムをリネーム＋先頭へ移動
    updated = []
    for source in data["sources"]:
        if source.get("id") != "scene":
            continue
        items: list = source.get("settings", {}).get("items", [])
        mic_items = [i for i in items if i.get("source_uuid") == MIC_UUID]
        if not mic_items:
            continue
        # 現在位置から取り除いて名前変更
        remaining = [i for i in items if i.get("source_uuid") != MIC_UUID]
        for mic in mic_items:
            mic["name"] = NEW_NAME
        # 先頭に挿入（= OBSソースリスト一番下）
        source["settings"]["items"] = mic_items + remaining
        updated.append(source["name"])

    print(f"\nUpdated {len(updated)} scenes:")
    for name in updated:
        print(f"  {name}")

    SCENES_JSON.write_text(
        json.dumps(data, ensure_ascii=False, indent=4), encoding="utf-8"
    )
    print(f"\nSaved: {SCENES_JSON}")


if __name__ == "__main__":
    fix()
