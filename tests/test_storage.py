

import os
from storage import load_items, save_items


def test_save_and_load(tmp_path):
    filename = os.path.join(tmp_path, "items.json")
    items = [{"id": 1, "name": "Пальто"}]
    save_items(filename, items)
    loaded = load_items(filename)
    assert loaded == items


def test_load_missing_file(tmp_path):
    filename = os.path.join(tmp_path, "no_file.json")
    assert load_items(filename) == []
