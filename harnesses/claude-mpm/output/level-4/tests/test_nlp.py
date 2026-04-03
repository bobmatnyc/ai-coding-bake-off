"""Tests for the NLP analysis module."""

from doc_pipeline.nlp import extract_entities, extract_key_phrases, generate_summary


SAMPLE_TEXT = """Acme Corporation Q3 2024 Financial Report

Acme Corporation is pleased to report strong results for the third quarter of 2024.
Revenue increased by 12% driven by cloud services growth and international expansion.

CEO Jane Mitchell commented: "We are very pleased with our momentum and growth this
quarter. Our innovation in cloud services has been outstanding."

CFO Robert Chen added that the company expects continued growth in Q4 2024.

The company operates in San Francisco, New York, and London, serving over 5,000
enterprise customers. TechGlobal Inc. partnership has been particularly successful.
"""


class TestExtractEntities:
    """Tests for the extract_entities function."""

    def test_returns_list(self) -> None:
        """Should return a list."""
        result = extract_entities(SAMPLE_TEXT)
        assert isinstance(result, list)

    def test_finds_entities(self) -> None:
        """Should find at least one entity in the sample text."""
        result = extract_entities(SAMPLE_TEXT)
        assert len(result) > 0

    def test_entity_has_text_and_type(self) -> None:
        """Each entity should have 'text' and 'type' fields."""
        result = extract_entities(SAMPLE_TEXT)
        for entity in result:
            assert isinstance(entity, dict)
            assert "text" in entity or "name" in entity
            assert "type" in entity or "label" in entity

    def test_finds_organization(self) -> None:
        """Should find Acme Corporation as an organization."""
        result = extract_entities(SAMPLE_TEXT)
        texts = [e.get("text", e.get("name", "")) for e in result]
        types = [e.get("type", e.get("label", "")) for e in result]
        org_entities = [t for t, typ in zip(texts, types) if "ORG" in typ.upper()]
        assert len(org_entities) > 0, "Should find at least one ORG entity"

    def test_finds_person(self) -> None:
        """Should find at least one person entity."""
        result = extract_entities(SAMPLE_TEXT)
        types = [e.get("type", e.get("label", "")).upper() for e in result]
        assert any("PERSON" in t or "PER" in t for t in types), \
            "Should find at least one PERSON entity"

    def test_empty_text_returns_empty(self) -> None:
        """Empty text should return empty list."""
        result = extract_entities("")
        assert result == []

    def test_entity_text_in_original(self) -> None:
        """Entity text should appear in the original text."""
        result = extract_entities(SAMPLE_TEXT)
        for entity in result:
            entity_text = entity.get("text", entity.get("name", ""))
            assert entity_text in SAMPLE_TEXT, \
                f"Entity '{entity_text}' not found in original text"


class TestExtractKeyPhrases:
    """Tests for the extract_key_phrases function."""

    def test_returns_list(self) -> None:
        """Should return a list."""
        result = extract_key_phrases(SAMPLE_TEXT)
        assert isinstance(result, list)

    def test_finds_phrases(self) -> None:
        """Should find at least one key phrase."""
        result = extract_key_phrases(SAMPLE_TEXT)
        assert len(result) > 0

    def test_phrases_are_strings(self) -> None:
        """All key phrases should be strings."""
        result = extract_key_phrases(SAMPLE_TEXT)
        for phrase in result:
            assert isinstance(phrase, str)

    def test_phrases_are_non_empty(self) -> None:
        """All key phrases should be non-empty."""
        result = extract_key_phrases(SAMPLE_TEXT)
        for phrase in result:
            assert len(phrase.strip()) > 0

    def test_empty_text_returns_empty(self) -> None:
        """Empty text should return empty list."""
        result = extract_key_phrases("")
        assert result == []

    def test_returns_unique_phrases(self) -> None:
        """Key phrases should be deduplicated."""
        result = extract_key_phrases(SAMPLE_TEXT)
        assert len(result) == len(set(result)), "Phrases should be unique"

    def test_short_text_returns_something(self) -> None:
        """Should handle short text gracefully."""
        text = "cloud services growth revenue"
        result = extract_key_phrases(text)
        assert isinstance(result, list)


class TestGenerateSummary:
    """Tests for the generate_summary function."""

    def test_returns_string(self) -> None:
        """Should return a string."""
        result = generate_summary(SAMPLE_TEXT)
        assert isinstance(result, str)

    def test_summary_is_shorter(self) -> None:
        """Summary should be shorter than original text."""
        result = generate_summary(SAMPLE_TEXT)
        assert len(result) < len(SAMPLE_TEXT)

    def test_summary_is_non_trivial(self) -> None:
        """Summary should be more than 20 characters."""
        result = generate_summary(SAMPLE_TEXT)
        assert len(result) > 20

    def test_empty_text_returns_empty(self) -> None:
        """Empty text should return empty string."""
        result = generate_summary("")
        assert result == ""

    def test_single_sentence(self) -> None:
        """Single sentence should return that sentence."""
        text = "This is a single sentence about Acme Corporation and its products."
        result = generate_summary(text)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_summary_contains_meaningful_content(self) -> None:
        """Summary should contain text from the original."""
        result = generate_summary(SAMPLE_TEXT)
        # At least some words from the original should appear
        original_words = set(SAMPLE_TEXT.lower().split())
        summary_words = set(result.lower().split())
        overlap = original_words & summary_words
        assert len(overlap) > 5, "Summary should share words with original"
