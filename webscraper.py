from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
res = []

mydata = ['K/D Ratio', 'Kills', 'Win %', 'Wins', 'Best Killstreak', 'Losses', 'Ties', 'Current Win Streak', 'Deaths', 'Avg. Life', 'Assists', 'Score/min', 'Score/game', 'Score']

def clean_stats(stats,name):
    res = []
    for key, value in stats.items():
        res.extend([key, value])
    stats = {}
    stats['Player Name'] = name
    for i in range(len(res)):
        if res[i] in mydata:
            stats[res[i]] = res[i+1]
    return stats

def scrape_cod_stats(url, player_name):
    driver = webdriver.Chrome()

    try:
        driver.get(url)

        # Wait for the stats to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.name, span.value'))
        )

        # Extract stats
        all_spans = driver.find_elements(By.CSS_SELECTOR, 'span.name, span.value')
        stats = {'Player Name': player_name}
        for i in range(0, len(all_spans), 2):
            name = all_spans[i].text
            value = all_spans[i + 1].text if (i + 1) < len(all_spans) else None
            stats[name] = value
        
        stats = clean_stats(stats,player_name)
        return stats

    finally:
        driver.quit()

player_names = [
    'IIAxzd',
    'Bengie-Glo',
    'Pills_N_PotionX',
    'AshleyBenoit800',
    'ChosenOne-x',
    'Kewgoon',
    'XXGlo_man_xX',
    'Caelanvert',
    'TrueKing_K',
    'Jesus-Is-Kixg',
    'YT-DFG_FeDy',
    'Zombeex_JayB'
]


all_player_stats = []

for name in player_names:
    url = f'https://cod.tracker.gg/modern-warfare/profile/psn/{name}/mp'
    player_stats = scrape_cod_stats(url, name)
    all_player_stats.append(player_stats)


df = pd.DataFrame(all_player_stats)
df.to_excel('all_player_stats.xlsx', index=False)



        
