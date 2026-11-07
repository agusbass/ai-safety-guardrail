"""Obfuscation-stripping for the SANITIZE stage.

Grounded in obfuscation vectors discussed for prompt-injection detection:
  - AgentWatcher, arXiv 2604.01194 (rule-based prompt injection monitor)
  - DataSentinel, arXiv 2504.11358 (game-theoretic detection)
  - PIShield, arXiv 2510.14005 (intrinsic LLM features)

These works note that adversarial prompts are routinely hidden from
keyword/pattern filters via zero-width Unicode, homoglyph substitution,
and base64-encoded payloads.
"""

import base64
import re

# Zero-width / invisible Unicode used to hide injected instructions.
ZERO_WIDTH = frozenset({
    '​',  # zero width space
    '‌',  # zero width non-joiner
    '‍',  # zero width joiner
    '⁠',  # word joiner
    '﻿',  # zero width no-break space / BOM
    '­',  # soft hyphen
})

# Cyrillic/Greek homoglyphs commonly substituted for Latin look-alikes to
# evade keyword/pattern filters.
HOMOGLYPHS = {
    'а': 'a', 'е': 'e', 'о': 'o', 'р': 'p',
    'с': 'c', 'у': 'y', 'х': 'x', 'і': 'i',
    'А': 'A', 'Е': 'E', 'О': 'O', 'Р': 'P',
    'С': 'C', 'һ': 'h',
}

BASE64_RE = re.compile(r'[A-Za-z0-9+/]{20,}={0,2}')


def sanitize_text(text: str) -> tuple[str, list[str]]:
    """Strip obfuscation vectors from `text`.

    Returns (clean_text, flags) where flags is a list of the obfuscation
    techniques detected and reversed:
      - "zero_width_chars_removed"
      - "homoglyphs_normalized"
      - "base64_payload_decoded"

    Decoded base64 payloads are appended (not substituted) so downstream
    stages can scan both the original and decoded content.
    """
    flags = []

    stripped = ''.join(ch for ch in text if ch not in ZERO_WIDTH)
    if stripped != text:
        flags.append('zero_width_chars_removed')
        text = stripped

    normalized = ''.join(HOMOGLYPHS.get(ch, ch) for ch in text)
    if normalized != text:
        flags.append('homoglyphs_normalized')
        text = normalized

    decoded_chunks = []
    for match in BASE64_RE.finditer(text):
        try:
            decoded = base64.b64decode(match.group(), validate=True).decode('utf-8')
            if decoded.isprintable():
                decoded_chunks.append(decoded)
        except (ValueError, UnicodeDecodeError):
            continue
    if decoded_chunks:
        flags.append('base64_payload_decoded')
        text = text + '\n[decoded]: ' + ' '.join(decoded_chunks)

    return text, flags
