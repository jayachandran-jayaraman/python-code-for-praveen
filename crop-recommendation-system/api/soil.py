def soil_season_score(crop, soil, season):
    score = 0
    if soil in crop["soil"]:
        score += 0.2
    if season == crop["season"]:
        score += 0.3
    return score
