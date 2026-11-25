# SPDX-License-Identifier: GPL-3.0
from __future__ import annotations

import pytest

from tuxemon.states.journal_info import (
    DESCRIPTION_SCALES,
    pick_description_scale,
)


@pytest.mark.parametrize(
    "heights, room, expected",
    [
        pytest.param({1.0: 40}, 43, 1.0, id="fits_unchanged"),
        pytest.param({1.0: 50, 0.9: 42}, 43, 0.9, id="second_step"),
        pytest.param(
            {1.0: 90, 0.9: 80, 0.8: 70, 0.7: 60, 0.6: 50, 0.5: 40},
            43,
            0.5,
            id="last_step",
        ),
        pytest.param(
            {1.0: 90, 0.9: 80, 0.8: 70, 0.7: 60, 0.6: 50, 0.5: 44},
            43,
            0.5,
            id="never_fits_uses_smallest",
        ),
        pytest.param({1.0: 43}, 43, 1.0, id="exact_fit_counts"),
    ],
)
def test_pick_scale(
    heights: dict[float, float], room: float, expected: float
) -> None:
    calls: list[float] = []

    def height_at(scale: float) -> float:
        calls.append(scale)
        return heights[scale]

    assert pick_description_scale(height_at, room) == expected
    # the last layout built is the chosen one, and no smaller step is tried
    assert calls[-1] == expected
    assert calls == list(DESCRIPTION_SCALES[: len(calls)])


def test_scales_descend_from_one() -> None:
    assert DESCRIPTION_SCALES[0] == 1.0
    assert list(DESCRIPTION_SCALES) == sorted(DESCRIPTION_SCALES, reverse=True)
