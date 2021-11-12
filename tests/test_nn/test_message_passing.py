# -*- coding: utf-8 -*-

"""Tests for message passing blocks."""

import pykeen.nn.message_passing
from tests import cases


class BlockDecompositionTests(cases.DecompositionTestCase):
    """Tests for block Decomposition."""

    cls = pykeen.nn.message_passing.BlockDecomposition


class EfficientBasesDecompositionTestCase(cases.BasesDecompositionTestCase):
    """Tests for efficient bases decomposition."""

    cls = pykeen.nn.message_passing.EfficientBasesDecomposition


class EfficientBlockDecompositionTestCase(cases.DecompositionTestCase):
    """Tests for efficient block decomposition."""

    cls = pykeen.nn.message_passing.EfficientBlockDecomposition


class LowMemoryBasesDecompositionTestCase(cases.BasesDecompositionTestCase):
    """Tests for BasesDecomposition with low memory requirement."""

    kwargs = dict(
        num_bases=4,
        memory_intense=False,
    )


class HighMemoryBasesDecompositionTestCase(cases.BasesDecompositionTestCase):
    """Tests for BasesDecomposition with high memory requirement."""

    kwargs = dict(
        num_bases=4,
        memory_intense=True,
    )
