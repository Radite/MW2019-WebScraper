from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

mydata = ['K/D Ratio', 'Kills', 'Win %', 'Wins', 'Best Killstreak', 'Losses', 'Ties', 'Current Win Streak', 'Deaths', 'Avg. Life', 'Assists', 'Score/min', 'Score/game', 'Score']


def parse_stat(value):
    try:
        # Remove known non-numeric characters and convert to float
        cleaned_value = value.replace('%', '').replace(',', '')
        return float(cleaned_value)
    except ValueError:
        # Check if the value is a string representation of a number (e.g., '12,345.67')
        try:
            return float(cleaned_value.replace(',', ''))
        except ValueError:
            # If still not convertible, return the original value
            return value
        
def clean_stats(stats,name):
    res = []
    for key, value in stats.items():
        res.extend([key, value])
    stats = {}
    stats['Player Name'] = name
    for i in range(len(res)):
        if res[i] in mydata:
            stats[res[i]] = parse_stat(res[i+1])
    return stats

def scrape_cod_stats(url, player_name):
    options = Options()
    options.headless = True  # Enable headless mode
    driver = webdriver.Chrome(options=options)

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
    except TimeoutException:
        print(f"Timeout while waiting for elements on {player_name}'s page.")
    except NoSuchElementException:
        print(f"Could not find expected elements on {player_name}'s page.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

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

print(df.describe())  # Descriptive statistics

# Data Visualization
sns.set(style="whitegrid")
# Horizontal Bar Plot for better readability
plt.figure(figsize=(12, 8))
sns.barplot(y='Player Name', x='K/D Ratio', data=df)
plt.title('K/D Ratios of Players')
plt.show()