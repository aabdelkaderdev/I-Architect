"""Tests for embedding service. Per FG-Phase-44 §2."""

from __future__ import annotations

import pytest


class TestEmbedding:
    def test_embed_texts_empty(self):
        """Empty input returns empty list."""
        from raa.embedding.embedder import embed_texts

        result = embed_texts([])
        assert result == []

    def test_cosine_scores(self):
        """Cosine scores returns similarity scores keyed by cluster id."""
        from raa.embedding.embedder import cosine_scores

        vector = [1.0, 0.0, 0.0]
        group_vectors = {
            1: [1.0, 0.0, 0.0],  # identical
            2: [0.0, 1.0, 0.0],  # orthogonal
        }
        scores = cosine_scores(vector, group_vectors)
        assert 1 in scores
        assert 2 in scores
        assert scores[1] > scores[2]  # Identical should score higher than orthogonal

    def test_assign_non_asrs_empty(self):
        """Empty non-ASRs returns empty assignments."""
        from raa.embedding.embedder import assign_non_asrs

        group_vectors, assignments = assign_non_asrs([], [], 0.65)
        assert assignments == []

    def test_cosine_scores_empty(self):
        """Empty group_vectors returns empty dict."""
        from raa.embedding.embedder import cosine_scores

        scores = cosine_scores([1.0, 0.0], {})
        assert scores == {}

    def test_assign_non_asrs_duplicate_clusters_targets_unique_batches(self, monkeypatch):
        """Duplicate cluster IDs still produce unique concern batch assignments."""
        from raa.embedding import embedder

        def fake_embed_texts(texts):
            mapping = {
                "group A": [1.0, 0.0],
                "group B": [0.0, 1.0],
                "functional B": [0.0, 1.0],
            }
            return [mapping[text] for text in texts]

        monkeypatch.setattr(embedder, "embed_texts", fake_embed_texts)

        condition_groups = [
            {
                "cluster": 0,
                "nominal_condition": "condition A",
                "requirements": [{"id": "R1", "text": "group A"}],
            },
            {
                "cluster": 0,
                "nominal_condition": "condition B",
                "requirements": [{"id": "R2", "text": "group B"}],
            },
        ]
        non_asrs = [{"id": "R3", "text": "functional B"}]

        group_vectors, assignments = embedder.assign_non_asrs(
            condition_groups, non_asrs, 0.65
        )

        assert list(group_vectors) == ["concern_batch_1", "concern_batch_2"]
        assert assignments == [(non_asrs[0], "concern_batch_2")]
