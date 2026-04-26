# 🧛 DiscountDrakula

> *Sucks the best deals out of German supermarkets and turns them into a weekly meal plan.*

DiscountDrakula is a Python tool that scrapes the weekly supermarket prospects (Prospekte) from [kaufda.de](https://www.kaufda.de), then uses an AI API to generate a smart weekly meal plan and shopping list — built around what's actually on sale near you.

Built out of pure laziness and the desire to eat well without overpaying. 😄

---

## 🚀 What it does

1. **Scrapes** current discount offers from kaufda.de for chosen supermarkets in my area (correct the latitudes and longtitudes for your area)
2. **Extracts** relevant food items and deals from the flyers
3. **Filters** relevant food items from the deals
4. **Calls an AI API** to generate a weekly meal plan based on the available discounts
5. **Outputs** a ready-to-use meal plan + shopping list, optimized for what's cheap this week

---

## 🛠️ Tech Stack

- **Python** — core logic and scraping
- **Web scraping** — crawling kaufda.de for live supermarket offers
- **AI API** — meal plan generation based on available ingredients
- **Text-based I/O** — simple, no-nonsense output

---

## ⚙️ Setup

### Prerequisites

- Python 3.8+
- An API key for the AI service used for meal planning

### Installation

```bash
git clone https://github.com/YutingXia006/DiscountDrakula.git
cd DiscountDrakula
pip install -r requirements.txt
```

### Configuration

Add your API key, your coordinates and the supermarkets that interests you to your environment:

```bash
export API_KEY=your_api_key_here
export LAT=your_lattitude
export LNG=your_longtitude´
export MARKETS=REWE,Aldi,Lidl #(check how the market is written in kaufda.de)
```

Dietary preferences can be changed in build_recepie_prompt() in ai_interface.py, please read these before your first run.
Stuff in your pantry and/or fridge can be written into data/vorhandene_zutaten.txt.

### Run

```bash
python DiscountDrakula/main.py
```

---

## 📋 Example Output

``` md
# Wochenübersicht
| Tag | Frühstück | Mittagessen | Abendessen |
| --- | --- | --- | --- |
| Montag | Avocado-Toast mit Hähnchenbrust | Thunfisch-Salat mit Quinoa und Himbeeren | Schweinebauch-Alternativ: Grilled Hähnchenbrust mit Süßkartoffeln und Brokkoli |
| Dienstag | Griechischer Joghurt mit Nüssen und Beeren | Hähnchen-Curry mit Reis und Zwiebeln | Garnelen-Stir-Fry mit Zucchini und Langkornreis |
| Mittwoch | Smoothie-Bowl mit Banane, Spinat und Chiasamen | Rinder-Minutensteaks mit Salat und Vollkornbrot | Lachs-Filet mit Quinoa und grünem Spargel |
| Donnerstag | Omelett mit Pilzen und Spinat | Hühnerbrust mit Kartoffeln und grünem Bohnen | Seelachs-Filet mit Süßkartoffeln und Erbsen |
| Freitag | Chia-Samen-Pudding mit Kokosmilch und Mango | Hähnchen-Tikka mit Reis und Naan-Brot | Garnelen-Sushi mit Avocado und Sojasoße |
| Samstag | Frühstücks-Burrito mit Scrambled-Eiern und schwarzen Bohnen | Hühner-Caesar-Salat mit Croutons und Parmesan | Grilled Hähnchenbrust mit Quinoa und grünem Salat |
| Sonntag | Crepes mit Erdbeeren und Joghurt | Thunfisch-Sushi mit Avocado und Sojasoße | Hähnchen-Fajitas mit Zwiebeln und Paprika-freien Peperoni |

## Rezepte

### Montag: Avocado-Toast mit Hähnchenbrust
* Zubereitungszeit: 15 Minuten
* Kochzeit: 10 Minuten
* Zutaten:
 + 2 Slices Vollkornbrot (120g)
 + 1 reife Avocado (150g)
 ...

 ## Einkaufsliste
### Getreide
* Quinoa
* Vollkornbrot
* Reis
* Bulgur
### Obst
* Avocados
* Himbeeren
* Erdbeeren
...
```

---

## 💡 Motivation

Grocery shopping as a student is a constant balancing act between budget and eating something that isn't just instant noodles. This tool automates the boring part — finding what's on sale and figuring out what to cook with it.

---

## 🗺️ Roadmap

- [ ] Easier way to change dietary preferences
- [ ] Simple web UI (Streamlit)
- [ ] Automatic weekly scheduling / notifications

---

## 📄 License

MIT License — do whatever you want with it.
