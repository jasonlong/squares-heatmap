import urllib.request, ssl, re, json, time

ssl._create_default_https_context = ssl._create_unverified_context
years = [2015, 2016, 2017, 2018, 2019, 2021, 2022, 2023, 2024, 2025]
all_games = {}

for year in years:
    url = f"https://www.sports-reference.com/cbb/postseason/men/{year}-ncaa.html"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        html = urllib.request.urlopen(req, timeout=15).read().decode("utf-8")
    except Exception as e:
        print(f"{year}: FAILED ({e})")
        continue
    
    # Find ALL boxscore links with scores (both bracket and First Four)
    pattern = re.findall(r"<a href='(/cbb/boxscores/[^']+)'>(\d+)</a>|<a href=\"(/cbb/boxscores/[^\"]+)\">(\d+)</a>", html)
    
    game_scores = {}
    for m in pattern:
        url_path = m[0] or m[2]
        score = m[1] or m[3]
        if url_path not in game_scores:
            game_scores[url_path] = []
        game_scores[url_path].append(int(score))
    
    games = []
    for url_path, scores in game_scores.items():
        if len(scores) == 2:
            s1, s2 = scores
            games.append([max(s1, s2), min(s1, s2)])
        elif len(scores) > 2:
            print(f"  {year} WARNING: {url_path} has {len(scores)} scores: {scores}")
    
    all_games[year] = games
    print(f"{year}: {len(games)} games")
    time.sleep(0.5)

with open("/Users/jason/dev/squares-heatmap/scores.json", "w") as f:
    json.dump(all_games, f, indent=2)

print(f"\nTotal: {sum(len(g) for g in all_games.values())} games")
