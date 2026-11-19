# checks whether an answer is or isn't wrong (no numerical score, it either is or isn't)
from internal_services import prompt
import re

_ASK = prompt.ask

FORMAT = {
    'type': 'object',
    'properties': {
        'result': {
            'type': 'string',
            'enum': ['right', 'wrong']
        }
    },
    'required': ['result'],
    'additionalProperties': False
}

SYSTEM_PROMPT = """You are a grading assistant.

Given:
- Question
- Expected answer
- User answer

Determine whether a reasonable human grader would accept the user answer as correct based on the expected answer.

Return:
- "right"
- "wrong"

Guidelines:
- Grade against the expected answer, not your own knowledge.
- Focus on meaning, not exact wording.
- Accept paraphrases and equivalent wording.
- Ignore spelling, capitalization, grammar, punctuation, and formatting mistakes when the intended meaning is clear.
- Accept minor typos that do not change the intended answer.
- Accept descriptive additions that do not change the meaning.
- Accept common abbreviations, alternate phrasings, and equivalent names.
- Accept a surname alone only when it unambiguously identifies the expected person and no important information is lost.
- Accept answers that express the same definition or concept using different words.

Mark as "wrong" when:
- The answer contradicts the expected answer.
- The answer contains a different number, value, date, name, place, or fact.
- Essential information is missing.
- The answer is only partially correct for a question requiring multiple items.
- The answer includes significant incorrect information.
- The answer changes the meaning of the expected answer.
- The expected is a name and the user did not give the complete name, ignoring middle names.

For list or multi-part answers:
- Every essential item must be present.
- Missing any required item makes the answer "wrong".

For single-fact questions:
- The user must provide the expected fact, value, name, or answer.
- A related or partially correct answer is still "wrong" unless the answer completes more than 80% of the expected.

When uncertain:
- Prefer semantic equivalence over exact wording.
- Be slightly lenient only when the meaning remains fully correct.

Output only valid JSON matching the provided schema."""

def check(question: str, correct_answer: str, user_answer: str) -> bool:

    correct = correct_answer.strip().lower()
    user = user_answer.strip().lower()

    # Empty answers are wrong
    if not user:
        return False

    # Exact match
    if user == correct:
        return True

    # Ignore punctuation
    normalize = lambda s: re.sub(r'[^\w\s]', '', s).strip().lower()

    if normalize(user) == normalize(correct):
        return True

    # Ex: 2+2, expected 4, check if 4 == user_answer
    try:
        if float(correct) == float(user):
            return True
    except ValueError:
        pass

    # '7' vs '7 days'
    if correct.isdigit():
        m = re.match(r'^(\d+)', user)
        if m and m.group(1) == correct:
            return True

    # List comparison
    if ',' in correct or ' and ' in correct:

        def split_items(text: str):
            return {item.strip() for item in re.split(r",|\band\b", text.lower()) if item.strip()}

        expected = split_items(correct)
        supplied = split_items(user)

        if supplied < expected:
            return False

        if supplied == expected:
            return False

    user_prompt = (f'Question:\n{question}\n\nExpected Answer:\n{correct_answer}\n\nUser Answer:\n{user_answer}')

    result = True if _ASK(user_prompt, 'low', SYSTEM_PROMPT, FORMAT)['result'] == 'right' else False

    return result