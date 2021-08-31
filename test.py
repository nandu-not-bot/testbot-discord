def add_suffix(score: int) -> str:
    if score >= 1000 and score < 10000:
        return str(round(score/1000, 1)) + "k"
    elif score >= 10000 and score < 1000000:
        return f"{str(score//1000)}k"
    elif score >= 1000000:
        return f"{str(round(score/1000000, 1))}M"
    else:
        return str(score)

print(add_suffix(int(input('- '))))