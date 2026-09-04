"""User profile controls for the ClimaCare AI frontend."""

import streamlit as st


def render_profile() -> dict[str, str]:
    """Render profile controls and return the current selections."""
    st.markdown("#### Help us personalize your care")
    st.caption("These details stay in this local app and help tailor future environmental guidance.")

    age_column, health_column, occupation_column = st.columns(3)
    with age_column:
        age_group = st.selectbox(
            "Age Group",
            ["Child", "Adult", "Senior"],
            index=1,
            key="age_group",
        )
    with health_column:
        health_condition = st.selectbox(
            "Health Condition",
            ["None", "Asthma", "Respiratory condition", "Heart condition"],
            key="health_condition",
        )
    with occupation_column:
        occupation = st.selectbox(
            "Occupation",
            ["Office Worker", "Outdoor Worker", "Student", "Athlete", "Other"],
            key="occupation",
        )

    profile = {
        "age_group": age_group,
        "health_condition": health_condition,
        "occupation": occupation,
    }
    st.session_state["profile"] = profile
    return profile
