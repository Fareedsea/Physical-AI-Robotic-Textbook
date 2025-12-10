"""
Response validation and confidence scoring for the Physical AI & Humanoid Robotics Textbook RAG system
Validates chatbot responses and provides confidence scores
"""

import logging
import re
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
import numpy as np
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine
import torch


logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of response validation"""
    is_valid: bool
    confidence_score: float
    issues: List[str]
    suggestions: List[str]


class ResponseValidator:
    """Validates RAG responses and calculates confidence scores"""

    def __init__(self,
                 embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
                 min_confidence: float = 0.3,
                 max_context_similarity: float = 0.9):
        self.min_confidence = min_confidence
        self.max_context_similarity = max_context_similarity

        # Load embedding model for similarity calculations
        self.embedding_model = SentenceTransformer(embedding_model_name)

    def validate_response(self,
                         query: str,
                         response: str,
                         sources: List[Dict[str, Any]],
                         context: Optional[str] = None) -> ValidationResult:
        """
        Validate a response based on various criteria

        Args:
            query: The original query
            response: The response to validate
            sources: Source documents used to generate the response
            context: Additional context that was provided to the model

        Returns:
            ValidationResult with validation results
        """
        issues = []
        suggestions = []

        # Check if response is empty
        if not response or not response.strip():
            issues.append("Response is empty")
            return ValidationResult(
                is_valid=False,
                confidence_score=0.0,
                issues=issues,
                suggestions=["Provide a meaningful response to the query"])

        # Calculate confidence score
        confidence_score = self._calculate_confidence_score(query, response, sources, context)

        # Check for hallucinations (response contradicting sources)
        hallucination_issues = self._check_for_hallucinations(response, sources)
        issues.extend(hallucination_issues)

        # Check for relevance to query
        relevance_issues = self._check_query_relevance(query, response)
        issues.extend(relevance_issues)

        # Check for coherence and completeness
        coherence_issues = self._check_coherence(response)
        issues.extend(coherence_issues)

        # Generate suggestions for improvement
        suggestions.extend(self._generate_suggestions(response, sources))

        # Determine if response is valid based on confidence and issues
        is_valid = confidence_score >= self.min_confidence and len(issues) == 0

        return ValidationResult(
            is_valid=is_valid,
            confidence_score=confidence_score,
            issues=issues,
            suggestions=suggestions
        )

    def _calculate_confidence_score(self,
                                   query: str,
                                   response: str,
                                   sources: List[Dict[str, Any]],
                                   context: Optional[str] = None) -> float:
        """
        Calculate confidence score based on multiple factors

        Args:
            query: The original query
            response: The response to score
            sources: Source documents used to generate the response
            context: Additional context that was provided to the model

        Returns:
            Confidence score between 0 and 1
        """
        scores = []

        # Score 1: Semantic similarity between query and response
        query_response_similarity = self._calculate_similarity(query, response)
        scores.append(query_response_similarity * 0.3)  # Weight 30%

        # Score 2: Semantic similarity between response and sources
        if sources:
            source_similarity = self._calculate_response_source_similarity(response, sources)
            scores.append(source_similarity * 0.4)  # Weight 40%
        else:
            scores.append(0.0)  # No sources means low confidence

        # Score 3: Coverage of query topics in response
        query_coverage = self._calculate_query_coverage(query, response)
        scores.append(query_coverage * 0.3)  # Weight 30%

        # Calculate weighted average
        confidence_score = sum(scores)

        # Ensure score is between 0 and 1
        confidence_score = max(0.0, min(1.0, confidence_score))

        return confidence_score

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two texts"""
        try:
            embeddings = self.embedding_model.encode([text1, text2])
            similarity = 1 - cosine(embeddings[0], embeddings[1])
            # Ensure similarity is between 0 and 1
            return max(0.0, min(1.0, (similarity + 1) / 2))
        except Exception:
            # Fallback to simple overlap if embedding fails
            words1 = set(text1.lower().split())
            words2 = set(text2.lower().split())
            if not words1 and not words2:
                return 1.0
            if not words1 or not words2:
                return 0.0
            overlap = len(words1.intersection(words2))
            total = len(words1.union(words2))
            return overlap / total if total > 0 else 0.0

    def _calculate_response_source_similarity(self, response: str, sources: List[Dict[str, Any]]) -> float:
        """Calculate similarity between response and source documents"""
        if not sources:
            return 0.0

        source_contents = []
        for source in sources:
            content = source.get('content') or source.get('metadata', {}).get('content', '')
            if content:
                source_contents.append(content)

        if not source_contents:
            return 0.0

        # Calculate similarity with each source and take the maximum
        similarities = [
            self._calculate_similarity(response, source_content)
            for source_content in source_contents
        ]

        return max(similarities) if similarities else 0.0

    def _calculate_query_coverage(self, query: str, response: str) -> float:
        """Calculate how well the response covers the query topics"""
        query_words = set(query.lower().split())
        response_words = set(response.lower().split())

        if not query_words:
            return 1.0

        covered_words = query_words.intersection(response_words)
        coverage = len(covered_words) / len(query_words)

        # Boost score if response contains key phrases from query
        query_lower = query.lower()
        response_lower = response.lower()

        # Look for exact phrase matches
        phrase_bonus = 0.0
        for word in query_words:
            if len(word) > 3 and word in response_lower:  # Only consider words longer than 3 chars
                phrase_bonus += 0.1

        coverage = min(1.0, coverage + phrase_bonus)
        return coverage

    def _check_for_hallucinations(self, response: str, sources: List[Dict[str, Any]]) -> List[str]:
        """Check if the response contains information not supported by sources"""
        issues = []

        if not sources:
            return issues

        # Combine all source content
        all_source_content = " ".join([
            source.get('content') or source.get('metadata', {}).get('content', '')
            for source in sources
            if source.get('content') or source.get('metadata', {}).get('content')
        ]).lower()

        # Look for specific claims in response that aren't in sources
        sentences = re.split(r'[.!?]+', response)
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10:  # Only check meaningful sentences
                sentence_lower = sentence.lower()
                # Check if this sentence contains information not in sources
                if sentence_lower not in all_source_content:
                    # Use embedding similarity as a secondary check
                    similarity = self._calculate_similarity(sentence, all_source_content)
                    if similarity < 0.3:  # Low similarity indicates potential hallucination
                        issues.append(f"Response may contain unsupported information: '{sentence[:100]}...'")

        return issues

    def _check_query_relevance(self, query: str, response: str) -> List[str]:
        """Check if the response is relevant to the query"""
        issues = []

        # Calculate similarity between query and response
        similarity = self._calculate_similarity(query, response)

        if similarity < 0.2:  # Low similarity
            issues.append("Response appears to be irrelevant to the query")

        return issues

    def _check_coherence(self, response: str) -> List[str]:
        """Check if the response is coherent and well-structured"""
        issues = []

        # Check for very short responses
        words = response.split()
        if len(words) < 5:
            issues.append("Response is too brief to be informative")

        # Check for excessive repetition
        word_counts = {}
        for word in words:
            clean_word = word.lower().strip('.,!?;:"')
            if len(clean_word) > 3:  # Only count meaningful words
                word_counts[clean_word] = word_counts.get(clean_word, 0) + 1

        max_repetition = max(word_counts.values()) if word_counts else 0
        if max_repetition > len(words) * 0.3:  # If one word appears in more than 30% of the response
            issues.append("Response contains excessive repetition")

        # Check for incomplete sentences
        if response.strip().endswith(('however', 'but', 'because', 'although')):
            issues.append("Response appears to be incomplete")

        return issues

    def _generate_suggestions(self, response: str, sources: List[Dict[str, Any]]) -> List[str]:
        """Generate suggestions for improving the response"""
        suggestions = []

        if len(response.split()) < 10:
            suggestions.append("Consider providing a more detailed response with specific examples from the textbook")

        if not sources:
            suggestions.append("Include references to specific textbook chapters or sections when answering")

        return suggestions


class ConfidenceScorer:
    """Calculates confidence scores for RAG responses"""

    def __init__(self,
                 embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
                 weights: Dict[str, float] = None):
        self.embedding_model = SentenceTransformer(embedding_model_name)

        # Default weights for different confidence factors
        self.weights = weights or {
            'semantic_similarity': 0.3,
            'source_support': 0.4,
            'query_coverage': 0.2,
            'coherence': 0.1
        }

    def score_response(self,
                      query: str,
                      response: str,
                      sources: List[Dict[str, Any]],
                      context: Optional[str] = None) -> float:
        """
        Score a response based on multiple confidence factors

        Args:
            query: The original query
            response: The response to score
            sources: Source documents used to generate the response
            context: Additional context that was provided to the model

        Returns:
            Confidence score between 0 and 1
        """
        scores = {}

        # Semantic similarity between query and response
        scores['semantic_similarity'] = self._semantic_similarity_score(query, response)

        # Source support (how well sources support the response)
        scores['source_support'] = self._source_support_score(response, sources)

        # Query coverage (how well response addresses the query)
        scores['query_coverage'] = self._query_coverage_score(query, response)

        # Coherence (how well-structured and logical the response is)
        scores['coherence'] = self._coherence_score(response)

        # Calculate weighted average
        total_score = sum(
            scores[metric] * self.weights[metric]
            for metric in scores
            if metric in self.weights
        )

        return min(1.0, max(0.0, total_score))  # Clamp between 0 and 1

    def _semantic_similarity_score(self, query: str, response: str) -> float:
        """Calculate semantic similarity score between query and response"""
        return self._calculate_similarity(query, response)

    def _source_support_score(self, response: str, sources: List[Dict[str, Any]]) -> float:
        """Calculate how well sources support the response"""
        if not sources:
            return 0.0

        source_contents = [
            source.get('content') or source.get('metadata', {}).get('content', '')
            for source in sources
            if source.get('content') or source.get('metadata', {}).get('content')
        ]

        if not source_contents:
            return 0.0

        # Calculate average similarity between response and all sources
        similarities = [
            self._calculate_similarity(response, source_content)
            for source_content in source_contents
        ]

        return sum(similarities) / len(similarities) if similarities else 0.0

    def _query_coverage_score(self, query: str, response: str) -> float:
        """Calculate how well response covers the query"""
        query_words = set(query.lower().split())
        response_words = set(response.lower().split())

        if not query_words:
            return 1.0

        covered_words = query_words.intersection(response_words)
        return len(covered_words) / len(query_words)

    def _coherence_score(self, response: str) -> float:
        """Calculate coherence score based on response structure"""
        words = response.split()

        # Base score on response length (longer responses tend to be more coherent)
        if len(words) < 5:
            return 0.3
        elif len(words) < 15:
            return 0.6
        else:
            return 0.8  # Assume well-structured if it's reasonably long

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two texts"""
        try:
            embeddings = self.embedding_model.encode([text1, text2])
            similarity = 1 - cosine(embeddings[0], embeddings[1])
            # Ensure similarity is between 0 and 1
            return max(0.0, min(1.0, (similarity + 1) / 2))
        except Exception:
            # Fallback to simple overlap if embedding fails
            words1 = set(text1.lower().split())
            words2 = set(text2.lower().split())
            if not words1 and not words2:
                return 1.0
            if not words1 or not words2:
                return 0.0
            overlap = len(words1.intersection(words2))
            total = len(words1.union(words2))
            return overlap / total if total > 0 else 0.0


# Global validator instance
_response_validator: Optional[ResponseValidator] = None


def get_response_validator() -> ResponseValidator:
    """Get the global response validator instance"""
    global _response_validator
    if _response_validator is None:
        _response_validator = ResponseValidator()
    return _response_validator


def validate_response(query: str,
                     response: str,
                     sources: List[Dict[str, Any]],
                     context: Optional[str] = None) -> ValidationResult:
    """Validate a response using the global validator"""
    validator = get_response_validator()
    return validator.validate_response(query, response, sources, context)


def score_response(query: str,
                 response: str,
                 sources: List[Dict[str, Any]],
                 context: Optional[str] = None) -> float:
    """Score a response using the global scorer"""
    scorer = ConfidenceScorer()
    return scorer.score_response(query, response, sources, context)


if __name__ == "__main__":
    # Example usage
    print("Testing response validation and confidence scoring...")

    validator = ResponseValidator()

    # Example query and response
    query = "What is Physical AI?"
    response = "Physical AI combines robotics and artificial intelligence to create embodied systems that interact with the physical world. It involves sensors, actuators, and control systems working together."
    sources = [
        {
            "content": "Physical AI combines robotics and artificial intelligence to create embodied systems...",
            "metadata": {"title": "Introduction to Physical AI", "chapter": "Chapter 1"}
        }
    ]

    # Validate the response
    result = validator.validate_response(query, response, sources)

    print(f"Validation result: is_valid={result.is_valid}")
    print(f"Confidence score: {result.confidence_score:.3f}")
    print(f"Issues: {result.issues}")
    print(f"Suggestions: {result.suggestions}")

    # Test with a low-confidence response
    low_conf_response = "I don't know the answer to that question."
    low_conf_result = validator.validate_response(query, low_conf_response, sources)
    print(f"\nLow-confidence result: is_valid={low_conf_result.is_valid}")
    print(f"Confidence score: {low_conf_result.confidence_score:.3f}")