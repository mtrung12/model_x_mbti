SYS_PROMPT = """
You are an expert in MBTI personality analysis. Use the MBTI dimension definitions below when making decisions. 

MBTI Dimension Guidelines:

Extraversion (E): Energized by interaction with the outer world of people and things. Attention is directed outward.

Introversion (I): Energized by reflection in the inner world of ideas and concepts. Attention is directed inward.

Sensing (S): Focuses on concrete, tangible information, specific details, and facts. Trusts experience and the five senses.

Intuition (N): Focuses on patterns, possibilities, and the big picture. Trusts insights and connections between facts.

Thinking (T): Makes decisions based on objective principles, logic, and impersonal analysis.

Feeling (F): Makes decisions based on personal values, relationships, and concern for people.

Judging (J): Prefers structure, plans, organization, and closure. Likes a controlled and decided environment.

Perceiving (P): Prefers flexibility, openness, adaptability, and exploring options. Likes to keep plans open.
"""

ZEROSHOT_USR_PROMPT = """
You are given a text written by a user.

From this text, extract the personality signals for four MBTI dimensions:

1. Social tendency: Extraversion (E) or Introversion (I)
2. Information processing: Sensing (S) or Intuition (N)
3. Decision-making: Thinking (T) or Feeling (F)
4. Lifestyle: Judging (J) or Perceiving (P)

Return the result as:

E/I:
S/N:
T/F:
J/P:

Text:
<text>
"""


ONESHOT_USR_PROMPT = """
Example:
Text:
{example_text}

Answer:
E/I: {example_EI}
S/N: {example_SN}
T/F: {example_TF}
J/P: {example_JP}

---
You are given a text written by a user.

From this text, extract the personality signals for four MBTI dimensions:

1. Social tendency: Extraversion (E) or Introversion (I)
2. Information processing: Sensing (S) or Intuition (N)
3. Decision-making: Thinking (T) or Feeling (F)
4. Lifestyle: Judging (J) or Perceiving (P)

Return the result as:

E/I:
S/N:
T/F:
J/P:

Text:
<text>
"""

COT_USR_PROMPT = """
You are analyzing a user's text to infer MBTI personality traits.

For each dimension, follow this reasoning process:
- Quote evidence from the text
- Explain what it implies
- Decide the letter

Dimensions:
1. Social tendency: Extraversion (E) or Introversion (I)
2. Information processing: Sensing (S) or Intuition (N)
3. Decision-making: Thinking (T) or Feeling (F)
4. Lifestyle: Judging (J) or Perceiving (P)

Text:
<text>

Answer in this format:

E/I:
Evidence:
Reasoning:
Letter:

S/N:
Evidence:
Reasoning:
Letter:

T/F:
Evidence:
Reasoning:
Letter:

J/P:
Evidence:
Reasoning:
Letter:
"""
