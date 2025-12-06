import streamlit as st
import importlib

# --- Page Config ---
st.set_page_config(
    page_title="Algo Visualizer",
    page_icon="📊",
    layout="wide"
)

# --- Sidebar Navigation ---
st.sidebar.title("Algorithm Visualizer")

# Map display names to module names
apps = {
    "Dutch National Flag Sort (0,1,2 Sorting)": "dnf_visualizer",
    # Add future visualizers here:
    # "Merge Sort": "merge_sort_visualizer",
}

# Use a single control (radio) for navigation
choice = st.sidebar.radio("Select an algorithm:", list(apps.keys()))

# --- Routing Logic ---
def load_visualizer(module_name: str):
    try:
        module = importlib.import_module(module_name)
        if hasattr(module, "main"):
            module.main()        # call the main() function of visualizer
        else:
            st.error(f"Module '{module_name}' has no main() entrypoint.")
    except Exception as e:
        st.error(f"Failed to load visualizer `{module_name}`: {e}")

# --- Main Area ---
if choice:
    module_name = apps[choice]
    load_visualizer(module_name)
