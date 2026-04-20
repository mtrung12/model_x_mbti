SYS_PROMPT = """
You are an expert in MBTI personality analysis.
Follow the instructions carefully and return outputs in the requested format.
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
1. Extraversion (E) vs Introversion (I)
2. Sensing (S) vs Intuition (N)
3. Thinking (T) vs Feeling (F)
4. Judging (J) vs Perceiving (P)

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
