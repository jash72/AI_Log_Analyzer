SYSTEM_PROMPT = """
You are an expert Infrastructure Engineer.

You analyze network device logs and configuration changes.

Your task:
1. Identify what changed.
2. Explain why this might have happened.
3. Keep the explanation under 20 words.
4. Return ONLY the explanation.
"""


def build_prompt(old_log, new_log):

    prompt = f"""
Old Configuration:
{old_log}

New Configuration:
{new_log}

Explain the change.
"""

    return prompt