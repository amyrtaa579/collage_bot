def is_branch_specialty(specialty: dict) -> bool:
    """
    Проверяет, относится ли специальность к филиалу (Стрежевской).
    Возвращает True, если в description есть маркеры филиала.
    """
    description = specialty.get("description") or ""
    branch_phrases = [
        "Обучение реализуется в Стрежевском филиале",
        "Реализуется в Стрежевском филиале"
    ]
    return any(phrase in description for phrase in branch_phrases)