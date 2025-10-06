

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
import random



def linear_search(arr, key):
   
    for i in range(len(arr)):
        if arr[i] == key:
            return i
    return -1

def binary_search_with_steps(arr, key):
    
    steps = []
    
    arr.sort() 
    low = 0
    high = len(arr) - 1
    
    while low <= high:
        mid = (low + high) // 2
        steps.append(f"Low: {low}, High: {high}, Mid: {mid} (Value: {arr[mid]})")
        
        if arr[mid] == key:
            steps.append(f"✅ Found {key} at index {mid}.")
            return mid, steps
        elif arr[mid] < key:

            low = mid + 1
        else:
           
            high = mid - 1
            
    steps.append(f"❌ {key} not found in the list.")
    return -1, steps



def iterative_max_min(arr):
   
    if not arr:
        return None, None
    
    maximum = arr[0]
    minimum = arr[0]
    
    for num in arr:
        if num > maximum:
            maximum = num
        if num < minimum:
            minimum = num
    return maximum, minimum

def divide_conquer_max_min(arr):
   
    if len(arr) == 1:
        return arr[0], arr[0]
    elif len(arr) == 2:
        return (arr[0], arr[1]) if arr[0] > arr[1] else (arr[1], arr[0])
    
  
    mid = len(arr) // 2
  
    max1, min1 = divide_conquer_max_min(arr[:mid])
    max2, min2 = divide_conquer_max_min(arr[mid:])
    
   
    final_max = max(max1, max2)
    final_min = min(min1, min2)
    
    return final_max, final_min

# -------------------- Streamlit App UI --------------------

st.set_page_config(layout="wide")
st.title("🔍 Fast Finder & Analyzer Tool")
st.write("An ADA project to compare and analyze search and optimization algorithms.")

st.sidebar.title("Data Input")
input_method = st.sidebar.radio("Choose how to provide data:", ["Upload CSV", "Generate Random Data"])

numbers = []

if input_method == "Upload CSV":
    uploaded_file = st.sidebar.file_uploader("Choose CSV file", type=["csv"])
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            # Assuming the first column has the numeric data
            numbers = pd.to_numeric(df.iloc[:, 0], errors='coerce').dropna().tolist()
            st.success(f"Successfully loaded {len(numbers)} numbers from the CSV.")
        except Exception as e:
            st.error(f"Error reading file: {e}")

elif input_method == "Generate Random Data":
    data_size = st.sidebar.slider("How many numbers to generate?", 100, 10000, 1000)
    numbers = [random.randint(1, 100000) for _ in range(data_size)]
    st.success(f"Generated a list of {len(numbers)} random numbers.")

# Only show the rest of the app if we have data
if numbers:
    st.write("### Dataset Preview (first 10 elements):")
    st.write(numbers[:10])

    # Using tabs for better organization
    tab1, tab2 = st.tabs(["🔢 Algorithm Analysis", "📊 Dataset Overview"])

    with tab1:
        st.header("Algorithm Performance Comparison")
        
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Binary Search vs. Linear Search")
            search_value = st.number_input("Enter a number to search for:", value=numbers[len(numbers)//2] if numbers else 0)

            if st.button("Run Search Comparison"):
                st.write("---")
                # --- Linear Search ---
                st.markdown("#### Linear Search ($O(n)$)")
                start_time = time.perf_counter()
                linear_result = linear_search(numbers, search_value)
                end_time = time.perf_counter()
                linear_time = (end_time - start_time) * 1000  # in milliseconds
                
                if linear_result != -1:
                    st.success(f"Found {search_value} at index {linear_result}.")
                else:
                    st.error(f"{search_value} not found.")
                st.info(f"**Execution Time:** {linear_time:.4f} ms")

                # --- Binary Search ---
                st.markdown("#### Binary Search ($O(log \, n)$)")
                sorted_numbers = sorted(numbers) # Binary search needs a sorted list
                start_time = time.perf_counter()
                binary_result, steps = binary_search_with_steps(sorted_numbers, search_value)
                end_time = time.perf_counter()
                binary_time = (end_time - start_time) * 1000 # in milliseconds

                if binary_result != -1:
                    st.success(f"Found {search_value} at index {binary_result} in the *sorted* list.")
                else:
                    st.error(f"{search_value} not found.")
                st.info(f"**Execution Time:** {binary_time:.4f} ms")
                
                # Show the steps for visualization
                with st.expander("See Binary Search Steps"):
                    for step in steps:
                        st.text(step)

        with col2:
            st.subheader("Max-Min Finding Comparison")

            if st.button("Run Max-Min Comparison"):
                st.write("---")
                # --- Iterative Method ---
                st.markdown("#### Iterative Method ($O(n)$)")
                start_time = time.perf_counter()
                iter_max, iter_min = iterative_max_min(numbers)
                end_time = time.perf_counter()
                iter_time = (end_time - start_time) * 1000
                st.write(f"📈 **Maximum:** {iter_max}")
                st.write(f"📉 **Minimum:** {iter_min}")
                st.info(f"**Execution Time:** {iter_time:.4f} ms")

                # --- Divide and Conquer Method ---
                st.markdown("#### Divide & Conquer Method")
                start_time = time.perf_counter()
                dq_max, dq_min = divide_conquer_max_min(numbers)
                end_time = time.perf_counter()
                dq_time = (end_time - start_time) * 1000
                st.write(f"📈 **Maximum:** {dq_max}")
                st.write(f"📉 **Minimum:** {dq_min}")
                st.info(f"**Execution Time:** {dq_time:.4f} ms")

    with tab2:
        st.header("Dataset Overview")
        maximum, minimum = iterative_max_min(numbers)
        average = sum(numbers) / len(numbers)
        
        st.info(f"📈 Maximum: {maximum}")
        st.info(f"📉 Minimum: {minimum}")
        st.info(f"⚖️ Average: {average:.2f}")

        # Visualization
        fig, ax = plt.subplots(1, 2, figsize=(12, 5))

        # Bar chart for max, min, average
        ax[0].bar(['Max', 'Min', 'Average'], [maximum, minimum, average], color=['#FF5733','#337BFF','#33FF57'])
        ax[0].set_title('Max, Min, and Average Values')
        ax[0].set_ylabel('Value')

        # Histogram of dataset
        ax[1].hist(numbers, bins=20, color='#8E44AD', edgecolor='black')
        ax[1].set_title('Distribution of Numbers in the Dataset')
        ax[1].set_xlabel('Value')
        ax[1].set_ylabel('Frequency')

        st.pyplot(fig)

st.sidebar.markdown("---")

st.sidebar.write("ADA Mini Project")
