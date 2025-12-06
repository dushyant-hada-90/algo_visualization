import streamlit as st

def main():
    st.title("Dutch National Flag Algorithm Visualizer")
    # keep your entire visualizer logic as it is below...

    # st.set_page_config(page_title="DNF Visualizer", layout="wide")

    def dnf_step(nums, low, mid, high):
        """Perform one DNF step and return updated state + descriptive message."""

        if mid > high:
            message = (
                f"Pointers → low={low}, mid={mid}, high={high}<br>"
                f"Termination Condition: mid > high.<br>"
                f"Algorithm completed."
            )
            return nums, low, mid, high, True, message

        value = nums[mid]

        # Case 0 → swap with low
        if value == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            message = (
                f"Pointers → low={low}, mid={mid}, high={high}<br>"
                f"nums[mid] = 0 → swap(low={low}, mid={mid})<br>"
                f"Result → low → {low+1}, mid → {mid+1}"
            )
            return nums, low + 1, mid + 1, high, False, message

        # Case 1 → move mid
        elif value == 1:
            message = (
                f"Pointers → low={low}, mid={mid}, high={high}<br>"
                f"nums[mid] = 1 → no swap, move mid → {mid+1}"
            )
            return nums, low, mid + 1, high, False, message

        # Case 2 → swap with high
        else:
            nums[mid], nums[high] = nums[high], nums[mid]
            message = (
                f"Pointers → low={low}, mid={mid}, high={high}<br>"
                f"nums[mid] = 2 → swap(mid={mid}, high={high})<br>"
                f"Result → high → {high-1} (mid stays)"
            )
            return nums, low, mid, high - 1, False, message

    # -------------------------------------------------------------------
    # Initialization
    # -------------------------------------------------------------------

    st.write("Step forward or backward through the algorithm with pointer tracking and full logs.")

    st.subheader("Initialize Array")

    col1, col2 = st.columns([3, 1])

    with col1:
        user_input = st.text_input(
            "Enter array (comma-separated 0, 1, 2):",
            "2,0,2,1,1,0"
        )

    with col2:
        init_clicked = st.button("Initialize", use_container_width=True)

    # Handle Initialization
    if init_clicked:
        try:
            arr = [int(x.strip()) for x in user_input.split(",")]

            if not all(x in [0, 1, 2] for x in arr):
                st.error("Array must contain only 0, 1, and 2.")
            else:
                st.session_state.history = []
                st.session_state.index = 0
                st.session_state.done = False

                init_state = {
                    "arr": arr,
                    "low": 0,
                    "mid": 0,
                    "high": len(arr) - 1,
                    "msg": f"Initialized array: {arr}",
                    "done": False
                }

                st.session_state.history.append(init_state)
                st.success("Array initialized successfully.")

        except Exception:
            st.error("Invalid input. Enter values like: 2,0,2,1,1,0")

    # -------------------------------------------------------------------
    # First Load Default State (only set defaults if missing)
    # -------------------------------------------------------------------
    if "history" not in st.session_state:
        default_arr = [2, 0, 2, 1, 1, 0]
        st.session_state.history = [{
            "arr": default_arr,
            "low": 0,
            "mid": 0,
            "high": len(default_arr) - 1,
            "msg": f"Initialized array: {default_arr}",
            "done": False
        }]
        st.session_state.index = 0

    # -------------------------------------------------------------------
    # Active state (run every time)
    # -------------------------------------------------------------------
    state = st.session_state.history[st.session_state.index]
    arr = state["arr"]
    low, mid, high = state["low"], state["mid"], state["high"]

    # -------------------------------------------------------------------
    # Visualization: Array
    # -------------------------------------------------------------------
    st.subheader("Current Array State")

    cols = st.columns(len(arr))
    colors = {0: "#4DA8DA", 1: "#F5A623", 2: "#D64541"}

    for i, col in enumerate(cols):
        with col:
            st.markdown(
                f"""
                <div style="
                    padding:20px;
                    border-radius:10px;
                    text-align:center;
                    font-size:24px;
                    font-weight:600;
                    background:{colors[arr[i]]};
                    color:white;">
                    {arr[i]}
                </div>
                """, unsafe_allow_html=True
            )

    pointer_row = st.columns(len(arr))
    for i, col in enumerate(pointer_row):
        marker = ""
        if i == low: marker += "L"
        if i == mid: marker += "M"
        if i == high: marker += "H"
        with col:
            st.markdown(
                f"<div style='text-align:center; font-size:20px;'>{marker}</div>",
                unsafe_allow_html=True
            )

    # -------------------------------------------------------------------
    # Controls (Next / Previous)
    # -------------------------------------------------------------------
    st.subheader("Controls")

    btn_col1, btn_col2 = st.columns(2)

    with btn_col1:
        if st.button("⬅ Previous Step"):
            if st.session_state.index > 0:
                st.session_state.index -= 1

                # Remove all future states (so log + future steps disappear)
                st.session_state.history = st.session_state.history[:st.session_state.index + 1]


    with btn_col2:
        if st.button("➡ Next Step"):
            if state["done"]:
                st.info("Algorithm already completed.")
            else:
                # Perform next step
                new_arr = state["arr"][:]
                (
                    new_arr,
                    new_low,
                    new_mid,
                    new_high,
                    new_done,
                    explanation
                ) = dnf_step(new_arr, low, mid, high)

                new_state = {
                    "arr": new_arr,
                    "low": new_low,
                    "mid": new_mid,
                    "high": new_high,
                    "msg": explanation,
                    "done": new_done
                }

                # push to history
                st.session_state.history.append(new_state)
                st.session_state.index += 1

    # -------------------------------------------------------------------
    # Log Section
    # -------------------------------------------------------------------
    st.subheader("Detailed Step Log")

    visible_history = st.session_state.history[: st.session_state.index + 1]

    log_text = ""
    for i, s in enumerate(visible_history):
        prefix = f"<b>Step {i}:</b><br>"
        log_text += prefix + s["msg"] + "<br><br>"

    st.markdown(
        f"""
        <div style="
            height:280px;
            overflow-y:scroll;
            background:#111;
            color:#eee;
            padding:15px;
            font-family:monospace;
            border-radius:10px;
            line-height:1.4;
            font-size:14px;">
            {log_text}
        </div>
        """,
        unsafe_allow_html=True
    )

    # -------------------------------------------------------------------
    # Show Algorithm Code
    # -------------------------------------------------------------------
    st.subheader("Dutch National Flag Algorithm Code")

    st.code("""
def sortColors(nums):
    low, mid, high = 0, 0, len(nums)-1

    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1

        elif nums[mid] == 1:
            mid += 1

        else:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
""", language="python")


# Allow standalone execution
if __name__ == "__main__":
    main()
