# -*- coding: utf-8 -*-

"""Test training mode for ConvE."""

import logging
import os
import tempfile
import unittest

import numpy as np

import pykeen
import pykeen.constants as pkc
from tests.constants import RESOURCES_DIRECTORY

logging.basicConfig(level=logging.INFO)
logging.getLogger('pykeen').setLevel(logging.INFO)

CONFIG = dict(
    training_set_path=os.path.join(RESOURCES_DIRECTORY, 'data', 'rdf.nt'),
    execution_mode=pkc.TRAINING_MODE,
    random_seed=0,
    kg_embedding_model_name=pkc.CONV_E_NAME,
    embedding_dim=50,
    ConvE_input_channels=1,
    ConvE_output_channels=3,
    ConvE_height=5,
    ConvE_width=10,
    ConvE_kernel_height=5,
    ConvE_kernel_width=3,
    conv_e_input_dropout=0.2,
    conv_e_feature_map_dropout=0.5,
    conv_e_output_dropout=0.5,
    margin_loss=1,
    learning_rate=0.01,
    num_epochs=20,
    batch_size=64,
    preferred_device='cpu'
)


class TestTrainingModeForConvE(unittest.TestCase):
    """Test that ConvE can be trained and evaluated correctly in training mode."""

    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.dir.cleanup()

    def test_training(self):
        """Test that ConvE is trained correctly in training mode."""
        results = pykeen.run(
            config=CONFIG,
            output_directory=self.dir.name,
        )

        self.assertIsNotNone(results)
        self.assertIsNotNone(results.results[pkc.TRAINED_MODEL])
        self.assertIsNotNone(results.results[pkc.LOSSES])
        self.assertIsNotNone(results.results[pkc.ENTITY_TO_EMBEDDING])
        self.assertNotIn(pkc.EVAL_SUMMARY, results.results)
        self.assertIsNotNone(results.results[pkc.ENTITY_TO_ID])
        self.assertIsNotNone(results.results[pkc.RELATION_TO_ID])
        self.assertIsNotNone(results.results[pkc.FINAL_CONFIGURATION])

    def test_evaluation(self):
        """Test that ConvE is trained and evaluated correctly in training mode. """
        # 10 % of training set will be used as a test set
        config = CONFIG.copy()
        config[pkc.TEST_SET_RATIO] = 0.1
        config[pkc.FILTER_NEG_TRIPLES] = True

        results = pykeen.run(
            config=config,
            output_directory=self.dir.name,
        )

        self.assertIsNotNone(results)
        self.assertIsNotNone(results.results[pkc.TRAINED_MODEL])
        self.assertIsNotNone(results.results[pkc.LOSSES])
        self.assertIsNotNone(results.results[pkc.ENTITY_TO_EMBEDDING])
        self.assertIn(pkc.EVAL_SUMMARY, results.results)
        self.assertIn(pkc.MEAN_RANK, results.results[pkc.EVAL_SUMMARY])
        self.assertEqual(type(results.results[pkc.EVAL_SUMMARY][pkc.MEAN_RANK]), float)
        self.assertIn(pkc.HITS_AT_K, results.results[pkc.EVAL_SUMMARY])
        self.assertEqual(type(results.results[pkc.EVAL_SUMMARY][pkc.HITS_AT_K][1]), np.float64)
        self.assertEqual(type(results.results[pkc.EVAL_SUMMARY][pkc.HITS_AT_K][3]), np.float64)
        self.assertEqual(type(results.results[pkc.EVAL_SUMMARY][pkc.HITS_AT_K][5]), np.float64)
        self.assertEqual(type(results.results[pkc.EVAL_SUMMARY][pkc.HITS_AT_K][10]), np.float64)
        self.assertIsNotNone(results.results[pkc.ENTITY_TO_ID])
        self.assertIsNotNone(results.results[pkc.RELATION_TO_ID])
        self.assertIsNotNone(results.results[pkc.FINAL_CONFIGURATION])