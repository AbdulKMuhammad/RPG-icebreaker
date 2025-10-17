import streamlit as st
import plotly.graph_objects as go
import json
import random

def create_radar_chart(stats, stat_names):
    # Close the loop by appending the first element to the end
    stats = stats + [stats[0]]
    stat_names = stat_names + [stat_names[0]]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=stats,
        theta=stat_names,
        fill='toself',
        name='Stats',
        line=dict(color='#1f77b4')
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 25],
                tickvals=[5, 10, 15, 20, 25],
                ticktext=['5', '10', '15', '20', '25'],
                showline=False
            ),
            angularaxis=dict(
                rotation=90,
                direction="clockwise"
            )
        ),
        showlegend=False,
        title={
            'text': 'Choose your own build',
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 24}
        },
        height=600,
        margin=dict(l=80, r=80, t=100, b=80)
    )
    
    return fig

def load_scenarios():
    """Load scenarios from JSON file"""
    try:
        with open('scenarios.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("scenarios.json file not found!")
        return []

def load_outcomes():
    """Load outcomes from JSON file"""
    try:
        with open('outcomes.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("outcomes.json file not found!")
        return []

def evaluate_scenario(user_stats, scenario_stats, stat_names):
    """Evaluate how user stats compare to scenario requirements"""
    # Calculate differences for each stat
    differences = []
    for i, stat_name in enumerate(stat_names):
        stat_key = stat_name.lower()
        user_val = user_stats[i]
        scenario_val = scenario_stats.get(stat_key, 0)
        diff = user_val - scenario_val
        differences.append(diff)
    
    # Find the minimum difference (worst performing stat)
    min_diff = min(differences)
    
    # Determine outcome based on minimum difference
    if min_diff >= 3:
        return "passed_easily"
    elif min_diff >= 0:
        return "passed"
    elif min_diff >= -3:
        return "failed"
    else:
        return "failed_miserably"

def run_simulation(user_stats, stat_names):
    """Run simulation with 5 random scenarios"""
    scenarios = load_scenarios()
    outcomes_data = load_outcomes()
    
    if not scenarios or not outcomes_data:
        return None
    
    # Select 5 random scenarios
    selected_scenarios = random.sample(scenarios, min(5, len(scenarios)))
    
    results = []
    for scenario in selected_scenarios:
        outcome_type = evaluate_scenario(user_stats, scenario, stat_names)
        
        # Find matching outcome
        outcome_text = ""
        for outcome in outcomes_data:
            if outcome['id'] == scenario['id']:
                outcome_text = outcome.get(outcome_type, "No outcome available")
                break
        
        results.append({
            'scenario': scenario['scenario'],
            'outcome_type': outcome_type,
            'outcome_text': outcome_text,
            'scenario_stats': {
                'strength': scenario['strength'],
                'agility': scenario['agility'],
                'intelligence': scenario['intelligence'],
                'stamina': scenario['stamina'],
                'luck': scenario['luck']
            }
        })
    
    return results

def main():
    st.set_page_config(
        page_title="Choose your own build",
        page_icon="⭐",
        layout="wide"
    )
    
    st.title("Stat Visualizer")
    st.write("Adjust the sliders to allocate your stats. Maximum total: 25 points.")
    
    # Default stat names (can be customized)
    stat_names = ['Strength', 'Agility', 'Intelligence', 'Stamina', 'Luck']
    MAX_TOTAL_STATS = 25
    
    # Initialize session state for stats if not exists
    if 'stats' not in st.session_state:
        st.session_state.stats = [5, 5, 5, 5, 5]  # Default values that sum to 25
    
    # Create columns for sliders and chart
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.header("Stats Configuration")
        
        # Calculate current total
        current_total = sum(st.session_state.stats)
        remaining_points = MAX_TOTAL_STATS - current_total
        
        # Display total stats
        if remaining_points < 0:
            st.error(f"⚠️ Over limit by {abs(remaining_points)} points!")
        elif remaining_points == 0:
            st.success(f"✅ All {MAX_TOTAL_STATS} points allocated")
        else:
            st.info(f"📊 Points remaining: {remaining_points}/{MAX_TOTAL_STATS}")
        
        st.markdown("---")
        
        # Create sliders for each stat
        for i, name in enumerate(stat_names):
            # Calculate max value for this slider (current value + remaining points)
            # Ensure max is always at least equal to current value to avoid min >= max error
            max_for_slider = max(st.session_state.stats[i], min(25, st.session_state.stats[i] + remaining_points))
            
            new_value = st.slider(
                f"{name}", 
                min_value=0, 
                max_value=max_for_slider, 
                value=st.session_state.stats[i],
                key=f"stat_{i}"
            )
            
            # Update session state if value changed
            if new_value != st.session_state.stats[i]:
                st.session_state.stats[i] = new_value
                st.rerun()
    
    with col2:
        # Create and display the radar chart
        fig = create_radar_chart(st.session_state.stats, stat_names)
        st.plotly_chart(fig, use_container_width=True)
    
    # Simulation section
    st.markdown("---")
    st.header("🎲 Test Your Build")
    st.write("Run a simulation to see how your stats perform against random life scenarios!")
    
    col_sim1, col_sim2, col_sim3 = st.columns([1, 1, 2])
    
    with col_sim1:
        if st.button("🎯 Run Simulation", type="primary", use_container_width=True):
            st.session_state.simulation_results = run_simulation(st.session_state.stats, stat_names)
    
    with col_sim2:
        if st.button("🔄 Clear Results", use_container_width=True):
            st.session_state.simulation_results = None
    
    # Display simulation results
    if 'simulation_results' in st.session_state and st.session_state.simulation_results:
        st.markdown("---")
        st.subheader("📊 Simulation Results")
        
        for i, result in enumerate(st.session_state.simulation_results, 1):
            # Determine color and emoji based on outcome
            if result['outcome_type'] == 'passed_easily':
                color = "green"
                emoji = "✅"
                outcome_label = "PASSED EASILY"
            elif result['outcome_type'] == 'passed':
                color = "blue"
                emoji = "👍"
                outcome_label = "PASSED"
            elif result['outcome_type'] == 'failed':
                color = "orange"
                emoji = "⚠️"
                outcome_label = "FAILED"
            else:  # failed_miserably
                color = "red"
                emoji = "❌"
                outcome_label = "FAILED MISERABLY"
            
            with st.expander(f"{emoji} Scenario {i}: {result['scenario']}", expanded=True):
                st.markdown(f"**Outcome:** :{color}[{outcome_label}]")
                st.write(result['outcome_text'])
                
                # Show scenario requirements
                st.markdown("**Scenario Requirements:**")
                req_cols = st.columns(5)
                for idx, stat_name in enumerate(stat_names):
                    stat_key = stat_name.lower()
                    scenario_val = result['scenario_stats'][stat_key]
                    user_val = st.session_state.stats[idx]
                    diff = user_val - scenario_val
                    
                    with req_cols[idx]:
                        if diff >= 3:
                            st.metric(stat_name, f"{scenario_val}", f"+{diff}", delta_color="normal")
                        elif diff >= 0:
                            st.metric(stat_name, f"{scenario_val}", f"+{diff}", delta_color="normal")
                        elif diff >= -3:
                            st.metric(stat_name, f"{scenario_val}", f"{diff}", delta_color="inverse")
                        else:
                            st.metric(stat_name, f"{scenario_val}", f"{diff}", delta_color="inverse")

if __name__ == "__main__":
    main()
