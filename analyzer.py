#!/usr/bin/env python3
# analyzer.py
# Beginner-friendly AI SEO Content Analyzer
# Reads content from sample_content.txt, computes simple SEO metrics,
# and asks an LLM (or a mock) for improvement suggestions.

import os
import re
import argparse
from collections import Counter

try:
    import openai
except Exception:
    openai = None

# ------- Helper functions -------

def read_file(path):
    """Read and return text content from a file."""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def get_words(text):
    """Return a list of words (simplified tokenizer)."""
    # Find word-like tokens, ignore punctuation
    return re.findall(r"\w+", text.lower())


def word_count(text):
    """Return total number of words in the text."""
    return len(get_words(text))


def sentence_split(text):
    """Split text into sentences using simple punctuation rules."""
    parts = re.split(r'[.!?]+', text)
    # Strip whitespace and remove empty strings
    return [p.strip() for p in parts if p.strip()]


def avg_sentence_length(sentences):
    """Average number of words per sentence."""
    if not sentences:
        return 0
    lengths = [len(get_words(s)) for s in sentences]
    return sum(lengths) / len(lengths)


def keyword_frequency(text, top_n=10, stopwords=None):
    """Return top_n most common words excluding stopwords."""
    if stopwords is None:
        stopwords = set(
            [
                'the', 'and', 'is', 'in', 'to', 'a', 'of', 'that', 'it', 'on',
                'for', 'with', 'as', 'this', 'are', 'an', 'be', 'by', 'or', 'we',
                'your', 'you'
            ]
        )
    words = [w for w in get_words(text) if w not in stopwords]
    return Counter(words).most_common(top_n)


def readability_checks(text):
    """Simple, rules-based readability checks.
    Returns a dict with basic metrics and flags.
    """
    sentences = sentence_split(text)
    avg_sent_len = avg_sentence_length(sentences)
    total_words = word_count(text)
    long_sentences = [s for s in sentences if len(get_words(s)) > 20]

    # Very simple grade suggestion based on average sentence length
    if avg_sent_len < 12:
        difficulty = 'Easy (good for general audiences)'
    elif avg_sent_len < 20:
        difficulty = 'Moderate'
    else:
        difficulty = 'Hard (consider shortening sentences)'

    return {
        'total_words': total_words,
        'sentence_count': len(sentences),
        'average_sentence_length': round(avg_sent_len, 1),
        'long_sentences_count': len(long_sentences),
        'difficulty_estimate': difficulty,
    }


def build_prompt(summary):
    """Create a prompt to send to the LLM for SEO suggestions.
    The summary should include basic metrics and top keywords.
    """
    prompt = (
        "You are an SEO assistant. Given the content summary below, provide clear, "
        "actionable suggestions to improve on-page SEO, keyword usage, headings, "
        "meta description ideas, and readability. Keep the suggestions concise and "
        "beginner-friendly.\n\n"
        "Content summary:\n" + summary + "\n\n"
        "Return suggestions as bullet points."
    )
    return prompt


def call_llm(prompt, use_mock=False):
    """Call an LLM (OpenAI) or return a mock response if use_mock=True or API unavailable."""
    if use_mock or not openai or not os.getenv('OPENAI_API_KEY'):
        # Mock suggestions - useful for offline/demo mode
        return (
            "- Use a clear H1 that includes your main keyword.\n"
            "- Add a short meta description (140-160 chars) containing the keyword.\n"
            "- Use the top 3 keywords naturally in the first 100 words.\n"
            "- Break long paragraphs into smaller ones (2-3 sentences each).\n"
            "- Add subheadings (H2/H3) to organize content and include related keywords.\n"
            "- Include internal links to related pages and at least one external reference."
        )

    # If we reach here, attempt to call OpenAI ChatCompletion
    try:
        openai.api_key = os.getenv('OPENAI_API_KEY')
        # Use ChatCompletion for better results
        response = openai.ChatCompletion.create(
            model=os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'),
            messages=[
                {'role': 'system', 'content': 'You are a helpful SEO assistant.'},
                {'role': 'user', 'content': prompt},
            ],
            max_tokens=300,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        # Fallback to mock suggestions on failure
        return (
            "- (Fallback) Use a clear H1 with the main keyword.\n"
            "- (Fallback) Add a meta description (140-160 chars).\n"
            "- (Fallback) Use keywords in the first 100 words.\n"
            "- (Fallback) Shorten long sentences and add subheadings."
        )


# ------- Main script -------

def main(content_path, use_mock=False, top_n=8):
    print(f"Reading content from: {content_path}")
    text = read_file(content_path)

    # Basic metrics
    wc = word_count(text)
    sentences = sentence_split(text)
    readability = readability_checks(text)
    keywords = keyword_frequency(text, top_n=top_n)

    # Display results to user
    print('\n--- Basic SEO Metrics ---')
    print(f"Word count: {wc}")
    print(f"Sentence count: {readability['sentence_count']}")
    print(f"Average sentence length (words): {readability['average_sentence_length']}")
    print(f"Number of long sentences (>20 words): {readability['long_sentences_count']}")
    print(f"Difficulty estimate: {readability['difficulty_estimate']}")

    print('\nTop keywords:')
    for i, (kw, freq) in enumerate(keywords, start=1):
        print(f"{i}. {kw} — {freq}")

    # Build a short summary for the LLM
    top_keywords_text = ', '.join([kw for kw, _ in keywords[:5]])
    summary = (
        f"Word count: {wc}. "
        f"Top keywords: {top_keywords_text}. "
        f"Average sentence length: {readability['average_sentence_length']}. "
        f"Long sentences: {readability['long_sentences_count']}.")

    prompt = build_prompt(summary)
    print('\nSending summary to LLM (mock mode = ' + str(use_mock) + ')...')
    suggestions = call_llm(prompt, use_mock=use_mock)

    print('\n--- SEO Improvement Suggestions ---')
    print(suggestions)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple AI SEO Content Analyzer')
    parser.add_argument('--file', '-f', default='sample_content.txt', help='Path to the text file to analyze')
    parser.add_argument('--mock', action='store_true', help='Use mock mode (no API key needed)')
    parser.add_argument('--top', type=int, default=8, help='Number of top keywords to show')
    args = parser.parse_args()

    main(args.file, use_mock=args.mock, top_n=args.top)
