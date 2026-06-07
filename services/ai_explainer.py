from llm.prompts import (
    SYSTEM_PROMPT,
    build_prompt
)

from llm.ollama_client import (
    generate_response
)


def add_ai_explanations(results):

    final_results = []

    for row in results:

        change_type = row["type"]

        if change_type in ["Unchanged", "Added", "Removed"]:
            row["reason"] = ""

        else:

            prompt = build_prompt(
                row["day1"],
                row["day2"]
            )

            explanation = generate_response(
                SYSTEM_PROMPT,
                prompt
            )

            row["reason"] = explanation

        final_results.append(row)

    return final_results