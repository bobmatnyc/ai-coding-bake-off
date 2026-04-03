"""NLP module for entity extraction, key phrase extraction, and summarization.

Uses regex-based extraction to avoid heavy dependency downloads.
"""

import re
from dataclasses import dataclass


@dataclass
class Entity:
    """Represents a named entity found in text."""

    text: str
    type: str
    count: int = 1


# Known locations for detection
KNOWN_LOCATIONS = {
    "San Francisco", "New York", "London", "Los Angeles", "Chicago",
    "Boston", "Seattle", "Austin", "Denver", "Atlanta", "Paris",
    "Berlin", "Tokyo", "Sydney", "Toronto", "Vancouver",
}

# Person title patterns
TITLE_PATTERNS = [
    r"\bCEO\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)",
    r"\bCFO\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)",
    r"\bCTO\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)",
    r"\bCOO\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)",
    r"\bMr\.\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)",
    r"\bMrs\.\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)",
    r"\bMs\.\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)",
    r"\bDr\.\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)",
    r"\bPresident\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)",
    r"\bDirector\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)",
    r"Chief\s+(?:Executive|Financial|Technical|Operating)\s+Officer\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)",
]

# Organization suffix patterns
ORG_PATTERN = re.compile(
    r"\b([A-Z][A-Za-z0-9&\s\.]+(?:Corporation|Corp|Inc\.|Inc|Ltd\.|Ltd|LLC|Company|Co\.|Co|Group|International|Technologies|Solutions|Systems|Services|Bank|Institute|University|Foundation))\b"
)

# Quoted name patterns (e.g., CEO John Smith)
QUOTED_PERSON_PATTERN = re.compile(
    r'"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)"'
)


def extract_entities(text: str) -> list[dict]:
    """Extract named entities using regex patterns.

    Identifies organizations, persons, and locations without
    requiring heavy NLP library downloads.

    Args:
        text: Input text to analyze.

    Returns:
        List of entity dicts with 'text', 'type', and 'count' keys.
    """
    found: dict[str, Entity] = {}

    def add_entity(entity_text: str, entity_type: str) -> None:
        """Add or increment entity count."""
        key = f"{entity_type}:{entity_text.strip()}"
        entity_text = entity_text.strip()
        if not entity_text or len(entity_text) < 2:
            return
        if key in found:
            found[key].count += 1
        else:
            found[key] = Entity(text=entity_text, type=entity_type)

    # Extract organizations
    for match in ORG_PATTERN.finditer(text):
        org_name = match.group(1).strip()
        if org_name:
            add_entity(org_name, "ORG")

    # Extract persons using title patterns
    for pattern in TITLE_PATTERNS:
        for match in re.finditer(pattern, text):
            person_name = match.group(1).strip()
            if person_name:
                add_entity(person_name, "PERSON")

    # Extract persons from quoted statements (e.g., "We are pleased..." - CEO Jane Mitchell)
    # Pattern: word said, "quote" - Name Title
    quoted_attribution = re.compile(
        r'"[^"]+"\s*[-—]\s*(?:said\s+)?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
    )
    for match in quoted_attribution.finditer(text):
        person_name = match.group(1).strip()
        # Filter out company names
        if not any(suffix in person_name for suffix in ["Corp", "Inc", "Ltd", "LLC", "Company"]):
            add_entity(person_name, "PERSON")

    # Also look for names after "commented," or "noted that"
    name_after_verb = re.compile(
        r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\s+(?:commented|noted|said|stated|announced|explained|added)',
    )
    for match in name_after_verb.finditer(text):
        person_name = match.group(1).strip()
        # Filter obvious non-persons
        words = person_name.split()
        if len(words) >= 2 and not any(
            suffix in person_name for suffix in ["Corp", "Inc", "Ltd", "LLC", "Company", "Office", "Division"]
        ):
            add_entity(person_name, "PERSON")

    # Extract locations from known list
    for location in KNOWN_LOCATIONS:
        if location in text:
            add_entity(location, "LOCATION")

    # Also look for "in/at <Capitalized City>" patterns
    location_pattern = re.compile(
        r"\b(?:in|at|from|near|to)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b"
    )
    for match in location_pattern.finditer(text):
        loc = match.group(1).strip()
        # Only add if it looks like a place name (not a common word)
        common_words = {"The", "This", "That", "Their", "Our", "Your", "Its", "All", "Some"}
        if loc not in common_words and len(loc) > 3:
            # Verify it's capitalized (already is by regex) and not an org
            if not ORG_PATTERN.search(loc):
                # Only if it appears to be a standalone name without org suffix
                if loc in KNOWN_LOCATIONS or re.match(r'^[A-Z][a-z]+$', loc):
                    add_entity(loc, "LOCATION")

    return [
        {"text": e.text, "type": e.type, "count": e.count}
        for e in found.values()
    ]


def extract_key_phrases(text: str) -> list[str]:
    """Extract key phrases from text using statistical and pattern-based methods.

    Identifies important noun phrases and recurring significant terms.

    Args:
        text: Input text to analyze.

    Returns:
        List of key phrase strings, ordered by importance.
    """
    if not text or not text.strip():
        return []

    phrases: list[str] = []

    # Pattern for noun phrases: optional adjectives + nouns
    noun_phrase_pattern = re.compile(
        r"\b(?:[A-Z][a-z]+\s+){1,3}(?:services?|solutions?|products?|systems?|platform|technology|capabilities?|operations?|revenue|growth|division|office|headquarters?|market|partnership|analytics?)\b",
        re.IGNORECASE,
    )

    # Find all noun phrases
    found_phrases: dict[str, int] = {}
    for match in noun_phrase_pattern.finditer(text):
        phrase = match.group(0).strip().lower()
        # Normalize
        words = phrase.split()
        if 1 < len(words) <= 5:
            found_phrases[phrase] = found_phrases.get(phrase, 0) + 1

    # Add frequently occurring capitalized multi-word phrases
    capitalized_phrase = re.compile(
        r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3}\b"
    )
    cap_counts: dict[str, int] = {}
    for match in capitalized_phrase.finditer(text):
        phrase = match.group(0).strip()
        # Exclude single common words
        if len(phrase.split()) >= 2:
            cap_counts[phrase] = cap_counts.get(phrase, 0) + 1

    # Include phrases that appear 2+ times
    for phrase, count in cap_counts.items():
        if count >= 2 and phrase.lower() not in found_phrases:
            found_phrases[phrase.lower()] = count

    # Sort by frequency
    sorted_phrases = sorted(found_phrases.items(), key=lambda x: -x[1])
    phrases = [phrase for phrase, _ in sorted_phrases[:20]]

    # If we didn't find enough with the above patterns, extract bigrams
    if len(phrases) < 5:
        words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
        # Filter stopwords
        stopwords = {
            "the", "and", "for", "that", "this", "with", "are", "was", "were",
            "has", "have", "had", "will", "would", "could", "should", "may",
            "our", "its", "their", "they", "from", "into", "about", "also",
            "than", "been", "more", "year", "percent", "per", "quarter",
        }
        filtered = [w for w in words if w not in stopwords and len(w) > 3]

        # Count bigrams
        bigrams: dict[str, int] = {}
        for i in range(len(filtered) - 1):
            bigram = f"{filtered[i]} {filtered[i+1]}"
            bigrams[bigram] = bigrams.get(bigram, 0) + 1

        sorted_bigrams = sorted(bigrams.items(), key=lambda x: -x[1])
        for phrase, count in sorted_bigrams[:10]:
            if phrase not in phrases:
                phrases.append(phrase)

    # Ensure we return at least some phrases by extracting from headings/titles
    if not phrases:
        # Extract from first line or headings
        lines = text.split("\n")
        for line in lines[:5]:
            line = line.strip()
            if line and len(line) > 10:
                # Extract multi-word chunks
                words = line.split()
                if len(words) >= 2:
                    phrases.append(" ".join(words[:3]))
                    break

    # Deduplicate while preserving order
    seen: set[str] = set()
    unique_phrases = []
    for p in phrases:
        p_lower = p.lower()
        if p_lower not in seen:
            seen.add(p_lower)
            unique_phrases.append(p)

    return unique_phrases[:15]


def generate_summary(text: str) -> str:
    """Generate an extractive summary of the text.

    Returns the first 2-3 meaningful sentences that capture
    the key information.

    Args:
        text: Input text to summarize.

    Returns:
        Summarized text string (shorter than original).
    """
    if not text or not text.strip():
        return ""

    # Split into sentences
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())

    # Filter to meaningful sentences (not too short, not too long)
    meaningful = [
        s.strip()
        for s in sentences
        if len(s.strip()) > 30 and len(s.strip()) < 500
    ]

    if not meaningful:
        # Fallback: just truncate to a reasonable length
        words = text.split()
        if len(words) > 50:
            return " ".join(words[:50]) + "..."
        return text

    # Take first 2-3 sentences as summary
    # Aim for roughly 20% of original length
    target_length = max(50, len(text) // 5)
    summary_sentences = []
    current_length = 0

    for sentence in meaningful[:3]:
        if current_length + len(sentence) <= target_length * 2 or not summary_sentences:
            summary_sentences.append(sentence)
            current_length += len(sentence)
            if current_length >= target_length and len(summary_sentences) >= 2:
                break

    summary = " ".join(summary_sentences)

    # Ensure summary is shorter than original
    if len(summary) >= len(text):
        words = text.split()
        summary = " ".join(words[:30]) + "..."

    return summary
