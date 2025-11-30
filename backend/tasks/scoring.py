from datetime import date


def detect_cycle(graph):
    visited = set()
    stack = set()

    def dfs(node):
        if node in stack:
            return True
        if node in visited:
            return False
        visited.add(node)
        stack.add(node)
        for nxt in graph.get(node, []):
            if dfs(nxt):
                return True
        stack.remove(node)
        return False

    for n in graph:
        if dfs(n):
            return True
    return False


def calculate_scores(tasks, weights):
    today = date.today()

    graph = {t["id"]: t["dependencies"] for t in tasks}
    if detect_cycle(graph):
        raise ValueError("Circular dependency detected")

    dep_count = {t["id"]: 0 for t in tasks}
    for t in tasks:
        for d in t["dependencies"]:
            if d in dep_count:
                dep_count[d] += 1

    scored = []
    for t in tasks:
        days = (t["due_date"] - today).days
        urgency = 10 if days < 0 else max(0, 10 - days)
        effort_score = 10 - min(t["estimated_hours"], 10)
        dep_score = dep_count[t["id"]]

        score = (
            weights["urgency"] * urgency +
            weights["importance"] * t["importance"] +
            weights["effort"] * effort_score +
            weights["dependency"] * dep_score
        )

        scored.append({**t, "score": round(score, 2)})

    return sorted(scored, key=lambda x: x["score"], reverse=True)
