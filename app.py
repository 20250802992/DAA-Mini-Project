import streamlit as st
import plotly.express as px
import pandas as pd
import random
import time

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="DAA Sorting Visualizer",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sorting Algorithm Visualizer")
st.subheader("Design and Analysis of Algorithms Mini Project")

st.markdown("""
This application demonstrates **Merge Sort** and **Bubble Sort**.
It visualizes sorting steps and compares the performance of both algorithms.
""")

st.divider()

# ==========================================
# MERGE SORT
# ==========================================

def merge_sort(arr):
    steps = []
    comparisons = [0]

    def sort(a):
        if len(a) <= 1:
            return a

        mid = len(a) // 2

        left = sort(a[:mid])
        right = sort(a[mid:])

        merged = []
        i = 0
        j = 0

        while i < len(left) and j < len(right):
            comparisons[0] += 1

            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        merged.extend(left[i:])
        merged.extend(right[j:])

        steps.append(merged.copy())

        return merged

    result = sort(arr.copy())

    if not steps or steps[-1] != result:
        steps.append(result.copy())

    return result, steps, comparisons[0]


# ==========================================
# OPTIMIZED BUBBLE SORT
# ==========================================

def bubble_sort(arr):
    a = arr.copy()
    steps = []
    comparisons = 0
    n = len(a)

    for i in range(n):
        swapped = False

        for j in range(0, n - i - 1):
            comparisons += 1

            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True

                if len(steps) < 500:
                    steps.append(a.copy())

        if not swapped:
            break

    if not steps or steps[-1] != a:
        steps.append(a.copy())

    return a, steps, comparisons


# ==========================================
# USER INPUT
# ==========================================

st.header("1. Enter Your Data")

input_method = st.radio(
    "Choose input method:",
    ["Enter numbers manually", "Generate random numbers"],
    horizontal=True
)

if input_method == "Enter numbers manually":

    number_input = st.text_input(
        "Enter numbers separated by commas:",
        value="45, 12, 78, 3, 56, 23, 9, 34"
    )

    try:
        numbers = [int(x.strip()) for x in number_input.split(",") if x.strip()]

        if not numbers:
            st.warning("Please enter at least one number.")
            numbers = []

        elif len(numbers) > 100:
            st.warning("Please enter a maximum of 100 numbers.")
            numbers = []

    except ValueError:
        st.error("Invalid input. Please enter integers separated by commas.")
        numbers = []

else:

    count = st.slider("Number of elements", 5, 100, 15)

    if st.button("Generate Random Numbers"):
        st.session_state.random_numbers = [
            random.randint(1, 100) for _ in range(count)
        ]

    if "random_numbers" not in st.session_state:
        st.session_state.random_numbers = [
            random.randint(1, 100) for _ in range(count)
        ]

    numbers = st.session_state.random_numbers

if numbers:
    st.write("**Original Array:**", numbers)

    st.divider()

    # ==========================================
    # ALGORITHM SELECTION
    # ==========================================

    st.header("2. Sorting Visualization")

    algorithm = st.selectbox(
        "Select Sorting Algorithm:",
        ["Merge Sort", "Bubble Sort"]
    )

    if st.button("Run Sorting Algorithm", type="primary"):

        if algorithm == "Merge Sort":
            result, steps, comparisons = merge_sort(numbers)
        else:
            result, steps, comparisons = bubble_sort(numbers)

        st.session_state.result = result
        st.session_state.steps = steps
        st.session_state.comparisons = comparisons
        st.session_state.selected_algorithm = algorithm

    if "result" in st.session_state:

        st.success(
            f"{st.session_state.selected_algorithm} completed successfully!"
        )

        st.write("**Sorted Array:**", st.session_state.result)

        st.metric(
            "Number of Comparisons",
            st.session_state.comparisons
        )

        st.subheader("Step-by-Step Visualization")

        steps = st.session_state.steps

        step_number = st.slider(
            "Select sorting step:",
            min_value=0,
            max_value=len(steps) - 1,
            value=len(steps) - 1
        )

        current_array = steps[step_number]

        chart_data = pd.DataFrame({
            "Position": list(range(len(current_array))),
            "Value": current_array
        })

        fig = px.bar(
            chart_data,
            x="Position",
            y="Value",
            title=f"Sorting Progress - Step {step_number + 1}",
            text="Value"
        )

        fig.update_layout(
            xaxis_title="Array Position",
            yaxis_title="Element Value"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.write("**Current Array:**", current_array)

    st.divider()

    # ==========================================
    # PERFORMANCE ANALYSIS
    # ==========================================

    st.header("3. Performance Comparison")

    st.write(
        "Compare Merge Sort and Bubble Sort using different input sizes."
    )

    if st.button("Run Performance Analysis"):

        sizes = [100, 300, 500, 700, 1000]

        merge_times = []
        bubble_times = []

        progress = st.progress(0)
        status = st.empty()

        for index, size in enumerate(sizes):

            test_data = [
                random.randint(1, 10000) for _ in range(size)
            ]

            start = time.perf_counter()
            merge_sort(test_data)
            merge_time = time.perf_counter() - start

            start = time.perf_counter()
            bubble_sort(test_data)
            bubble_time = time.perf_counter() - start

            merge_times.append(merge_time)
            bubble_times.append(bubble_time)

            progress.progress((index + 1) / len(sizes))
            status.write(f"Testing input size: {size}")

        performance_data = pd.DataFrame({
            "Input Size": sizes,
            "Merge Sort (seconds)": merge_times,
            "Bubble Sort (seconds)": bubble_times
        })

        st.session_state.performance_data = performance_data

    if "performance_data" in st.session_state:

        st.subheader("Performance Results")

        st.dataframe(
            st.session_state.performance_data,
            use_container_width=True
        )

        graph_data = st.session_state.performance_data.melt(
            id_vars="Input Size",
            var_name="Algorithm",
            value_name="Execution Time (seconds)"
        )

        fig = px.line(
            graph_data,
            x="Input Size",
            y="Execution Time (seconds)",
            color="Algorithm",
            markers=True,
            title="Merge Sort vs Bubble Sort Performance"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ==========================================
    # TIME AND SPACE COMPLEXITY
    # ==========================================

    st.header("4. Time and Space Complexity Analysis")

    complexity_data = pd.DataFrame({
        "Algorithm": ["Merge Sort", "Optimized Bubble Sort"],
        "Best Case": ["O(n log n)", "O(n)"],
        "Average Case": ["O(n log n)", "O(n²)"],
        "Worst Case": ["O(n log n)", "O(n²)"],
        "Space Complexity": ["O(n)", "O(1)"]
    })

    st.table(complexity_data)

    st.info(
        "Merge Sort uses the Divide and Conquer technique. "
        "It divides the array into smaller parts, sorts them, "
        "and merges them into a sorted array."
    )

    st.info(
        "Optimized Bubble Sort repeatedly compares adjacent elements "
        "and swaps them when they are in the wrong order. "
        "It stops early if no swaps are required."
    )

else:
    st.info("Enter valid numbers above to start the visualization.")

# ==========================================
# FOOTER
# ==========================================

st.divider()

st.markdown(
    "**DAA Mini Project | Sorting Algorithm Visualizer and Performance Analyzer**"
)

st.caption("Developed using Python, Streamlit, Pandas and Plotly.")
