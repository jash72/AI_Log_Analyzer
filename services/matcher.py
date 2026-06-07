from rapidfuzz import process
from rapidfuzz import fuzz

SIMILARITY_THRESHOLD = 90

def compare_logs(day1_logs, day2_logs):
    day1_set = set(day1_logs)
    day2_set = set(day2_logs)
    unchanged = day1_set.intersection(day2_set)
    removed_candidates = list(day1_set - unchanged)
    added_candidates = list(day2_set - unchanged)
    modified = []
    removed = []
    added_used = set()
    for old_line in removed_candidates:
        if len(added_candidates) == 0:
            removed.append(old_line)
            continue
        best_match = process.extractOne(
            old_line,
            added_candidates,
            scorer=fuzz.ratio
        )
        if best_match:
            new_line = best_match[0]
            score = best_match[1]
            if score >= SIMILARITY_THRESHOLD:
                modified.append({
                    "day1": old_line,
                    "day2": new_line,
                    "score": score,
                    "type": "Modified"
                })
                added_used.add(new_line)
            else:
                removed.append(old_line)
        else:
            removed.append(old_line)
    added = []
    for item in added_candidates:
        if item not in added_used:
            added.append(item)
    unchanged_result = []
    for item in unchanged:
        unchanged_result.append({
            "day1": item,
            "day2": item,
            "score": 100,
            "type": "Unchanged"
        })
    modified_result = modified
    removed_result = []
    for item in removed:
        removed_result.append({
            "day1": item,
            "day2": "",
            "score": 0,
            "type": "Removed"
        })
    added_result = []
    for item in added:
        added_result.append({
            "day1": "",
            "day2": item,
            "score": 0,
            "type": "Added"
        })
    final_result = (
        modified_result
        + added_result
        + removed_result
        + unchanged_result
    )
    summary = {
        "total_day1": len(day1_logs),
        "total_day2": len(day2_logs),
        "unchanged": len(unchanged_result),
        "modified": len(modified_result),
        "added": len(added_result),
        "removed": len(removed_result)
    }
    return summary, final_result