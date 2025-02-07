import streamlit as st
import pandas as pd

# Load Data with Error Handling and Caching
@st.cache_data
def load_data():
    try:
        with st.spinner("Loading data..."):
            # Load customer segmentation and recommendation data
            customer_data = pd.read_csv("data/merged_data.csv")  # Update with actual file path
        return customer_data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame to avoid crashes

# Load the dataset
customer_data = load_data()

# Streamlit UI
st.title("Customer Product Recommendation System")
st.write("📊 This app provides product recommendations based on customer segmentation.")

# Filter by Cluster
with st.sidebar:
    st.header("Filters")
    selected_cluster = st.selectbox("Filter by Cluster:", customer_data["cluster"].unique())

# Filtered Data
filtered_data = customer_data[customer_data["cluster"] == selected_cluster] if selected_cluster else customer_data

# User Input: Select Customer ID with Searchable Dropdown
customer_id = st.selectbox(
    "Select a Customer ID:",
    filtered_data["CustomerID"].unique(),
    index=0,  # Default to the first customer
    format_func=lambda x: f"Customer {x}"  # Display as "Customer XYZ"
)

# Display Customer Summary
if customer_id:
    customer_info = customer_data[customer_data["CustomerID"] == customer_id].iloc[0]
    customer_summary = customer_data[customer_data["CustomerID"] == customer_id].describe()

    st.subheader(f"Customer Summary for Customer {customer_id}")
    st.write("📝 **Customer Summary:**")
    st.write(customer_summary)

    st.subheader(f"Customer Segmentation: Cluster {customer_info['cluster']}")
    
    # Display Recommendations
    st.subheader("🔹 Recommended Products")
    recommendations = []
    for i in range(1, 4):  # Loop through 3 recommendations
        stock_code = customer_info[f"StockCode"]
        description = customer_info[f"Description"]
        if pd.notna(stock_code):
            recommendations.append(f"🛍 **{description}** (Stock Code: {stock_code})")

    if recommendations:
        st.markdown("\n".join(recommendations))
    else:
        st.write("✅ No new product recommendations available for this customer.")

# Visualize Customer Cluster Distribution
st.subheader("📊 Customer Cluster Distribution")
cluster_counts = customer_data["cluster"].value_counts()
st.bar_chart(cluster_counts)

# Add Tooltip or Explanation for Cluster
st.info("💡 Clusters represent different customer segments based on purchasing behavior. For example, Cluster 0 may represent high-spending customers.")

# Export Recommendations Button
if st.button("Export Recommendations"):
    recommendations_df = pd.DataFrame(recommendations, columns=["CustomerID", "Rec1_StockCode", "Rec1_Description", "Rec2_StockCode", "Rec2_Description", "Rec3_StockCode", "Rec3_Description"])
    recommendations_df.to_csv("recommendations.csv", index=False)
    st.success("Recommendations exported successfully!")

# Add a Feedback Mechanism
feedback = st.radio("Was this recommendation helpful?", ("Yes", "No"))
if feedback == "Yes":
    st.success("Thank you for your feedback!")
else:
    st.warning("We'll improve our recommendations!")
