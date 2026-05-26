def calculate_environment_score(temperature, humidity):
    score = 100
    recommendations = []

    if temperature < 18:
        score -= 25
        recommendations.append("Room is too cold.")
    elif temperature > 26:
        score -= 25
        recommendations.append("Room is too warm.")

    if humidity < 30:
        score -= 20
        recommendations.append("Air is too dry.")
    elif humidity > 60:
        score -= 20
        recommendations.append("Humidity is too high.")

    score = max(score, 0)

    if not recommendations:
        recommendations.append("Study environment is comfortable.")

    return score, recommendations


if __name__ == "__main__":
    score, tips = calculate_environment_score(22, 45)

    print(f"Environment Score: {score}/100")
    for tip in tips:
        print(f"- {tip}")
