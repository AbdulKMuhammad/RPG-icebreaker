# Stats Icebreaker - Life Scenario Simulator

An interactive Streamlit application that lets you build a character with custom stats and test how well your build performs against real-life scenarios. Allocate your points wisely across five key attributes and see if you can handle what life throws at you!

##  Features

- **Interactive Stat Builder**: Allocate 25 points across 5 different stats
  - Strength
  - Agility
  - Intelligence
  - Stamina
  - Luck

- **Visual Pentagram Chart**: See your stat distribution displayed as a radar chart

- **Scenario Simulation**: Test your build against 5 random real-life scenarios
  - 100 unique scenarios ranging from car troubles to work emergencies
  - 4 possible outcomes based on your performance:
    - ✅ **Passed Easily** - Your stats exceed requirements by 3+ points
    - 👍 **Passed** - Your stats meet or slightly exceed requirements
    - ⚠️ **Failed** - One or more stats fall short of requirements
    - ❌ **Failed Miserably** - One or more stats fall short by 3+ points

##  Prerequisites

- Python 3.9 or higher
- pip (Python package installer)

##  Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd windsurf-project
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
```

### 3. Activate the Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## How It Works

### Step 1: Build Your Character
1. Use the sliders on the left to allocate your 25 stat points
2. The pentagram chart updates in real-time to show your build
3. The system enforces the 25-point limit - as you increase one stat, others become limited

### Step 2: Run a Simulation
1. Click the **"🎯 Run Simulation"** button
2. The app randomly selects 5 scenarios from the database
3. Your stats are compared against each scenario's requirements

### Step 3: View Results
Each scenario shows:
- The situation you're facing
- Your outcome (passed easily, passed, failed, or failed miserably)
- A detailed narrative of what happens
- A breakdown showing how each of your stats compared to the requirements

### Example Scenario

**Scenario:** "Your car won't start on a morning you have an important appointment"

**Requirements:**
- Strength: 2
- Agility: 4
- Intelligence: 3
- Stamina: 3
- Luck: 3

**Your Stats:**
- Strength: 5 (+3) ✅
- Agility: 6 (+2) ✅
- Intelligence: 4 (+1) ✅
- Stamina: 5 (+2) ✅
- Luck: 5 (+2) ✅

**Outcome: PASSED EASILY** ✅
*"You pop the hood with confidence, wiggle a loose battery cable back into place, and the engine roars to life on the first try. You're on the road with time to spare."*

## 📁 Project Structure

```
RPG-icebreaker/
├── app.py                 # Main Streamlit application
├── scenarios.json         # 100 life scenarios with stat requirements
├── outcomes.json          # Outcome narratives for each scenario
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── .gitignore            # Git ignore rules
```

## 🎲 Game Mechanics

### Stat Allocation
- You have exactly **25 points** to distribute
- Each stat can range from **0 to 25**
- The total must equal 25 (enforced by the UI)

### Evaluation Logic
The simulation evaluates your **weakest performing stat** against each scenario:

1. Calculate the difference between your stat and the requirement for each attribute
2. Find your worst-performing stat (minimum difference)
3. Determine outcome based on that minimum:
   - `min_diff >= 3`: Passed Easily
   - `min_diff >= 0`: Passed
   - `min_diff >= -3`: Failed
   - `min_diff < -3`: Failed Miserably

This creates strategic depth - you must decide whether to specialize in certain stats or maintain a balanced build.

##  Technologies Used

- **Streamlit** - Web application framework
- **Plotly** - Interactive radar chart visualization
- **Python** - Core programming language

##  Strategy Tips

- **Balanced Build**: Distribute points evenly to handle a variety of scenarios
- **Specialized Build**: Max out specific stats to dominate certain scenario types
- **Min-Maxing**: Identify which stats appear most frequently and prioritize those
- **Zero Stats**: Setting a stat to 0 is risky but allows more points elsewhere

##  Contributing

Feel free to fork this project and add your own scenarios! Each scenario needs:
1. An entry in `scenarios.json` with stat requirements (must sum to 20)
2. Four outcome narratives in `outcomes.json` (passed_easily, passed, failed, failed_miserably)

##  License

This project is open source and available for personal and educational use.

## 🎉 Have Fun!

Remember, there's no "perfect" build - different stat distributions will excel in different scenarios. Experiment with different builds and see which playstyle suits you best!
