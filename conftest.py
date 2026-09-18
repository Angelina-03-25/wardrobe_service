"""
Конфигурация pytest.

Добавляет корень проекта в sys.path, чтобы тесты могли импортировать
модули items, storage, utils из корня проекта.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
