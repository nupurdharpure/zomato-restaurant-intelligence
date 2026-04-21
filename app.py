import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ── Page Config ────────────────────────────────────────────────
st.set_page_config(
    page_title="Zomato Restaurant Intelligence",
    page_icon="🍽️",
    layout="wide"
)

# ── Load Data ──────────────────────────────────────────────────
@st.cache_data
def load_data():
    import os
    # Works both locally and on Streamlit Cloud
    base_path = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_path, 'zomato_clean.csv')
    
    data = pd.read_csv(csv_path)
    data_rated = data[data['Aggregate rating'] > 0]
    data_india = data_rated[data_rated['Country Code'] == 1]
    return data_india

data = load_data()


# ── Sidebar Filters ────────────────────────────────────────────
st.sidebar.header("🔍 Filters")

# City filter
cities = ['All Cities'] + sorted(data['City'].unique().tolist())
selected_city = st.sidebar.selectbox("Select City", cities)

# Cuisine filter
cuisines = ['All Cuisines'] + sorted(data['Primary Cuisine'].unique().tolist())
selected_cuisine = st.sidebar.selectbox("Select Cuisine", cuisines)

# Price range filter
price_labels = {1: 'Budget (₹<500)', 2: 'Mid (₹500-1000)', 
                3: 'Premium (₹1000-2000)', 4: 'Luxury (₹2000+)'}
price_options = ['All Price Ranges'] + list(price_labels.values())
selected_price = st.sidebar.selectbox("Select Price Range", price_options)

# ── Apply Filters ──────────────────────────────────────────────
filtered_data = data.copy()
# Apply city filter
if selected_city != 'All Cities':
    filtered_data = filtered_data[filtered_data['City'] == selected_city]
# Apply cuisine filter
if selected_cuisine != 'All Cuisines':
    filtered_data = filtered_data[filtered_data['Primary Cuisine'] == selected_cuisine]
# Apply price filter
if selected_price != 'All Price Ranges':
    price_num = [k for k, v in price_labels.items() if v == selected_price][0]
    filtered_data = filtered_data[filtered_data['Price range'] == price_num]


# ── Title ──────────────────────────────────────────────────────
st.title("🍽️ Zomato Restaurant Intelligence Dashboard")
st.markdown("Analysing **6,500+ restaurants** across India — built with Python, SQL & Streamlit")
st.markdown("---")

# ── Metric Cards ───────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("🍴 Total Restaurants", f"{len(filtered_data):,}")
col2.metric("⭐ Avg Rating", f"{filtered_data['Aggregate rating'].mean():.2f}" if len(filtered_data) > 0 else "N/A")
col3.metric("💰 Avg Cost for Two", f"₹{filtered_data['Average Cost for two'].mean():.0f}" if len(filtered_data) > 0 else "N/A")
col4.metric("🚴 Offers Delivery", f"{(filtered_data['Has Online delivery']=='Yes').sum():,}")


st.markdown("---")

# ── Row 1: City + Cuisine Charts ───────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏙️ Restaurants by City")
    if selected_city == 'All Cities':
        city_counts = filtered_data['City'].value_counts().head(10).reset_index()
        city_counts.columns = ['City', 'Total']
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.barh(city_counts['City'], city_counts['Total'], color='#E23744')
        for bar in ax.patches:
            ax.text(bar.get_width() + 10, bar.get_y() + bar.get_height()/2,
                    f'{int(bar.get_width()):,}', va='center', fontsize=9)
        ax.invert_yaxis()
        ax.set_xlabel('Number of Restaurants')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    else:
        # If a city is selected show locality breakdown instead
        locality_counts = filtered_data['Locality'].value_counts().head(10).reset_index()
        locality_counts.columns = ['Locality', 'Total']
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.barh(locality_counts['Locality'], locality_counts['Total'], color='#E23744')
        ax.invert_yaxis()
        ax.set_xlabel('Number of Restaurants')
        ax.set_title(f'Top Localities in {selected_city}')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()


with col2:
    st.subheader("🍜 Top Cuisines")
    cuisine_counts = filtered_data['Primary Cuisine'].value_counts().head(10).reset_index()
    cuisine_counts.columns = ['Cuisine', 'Total']
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(cuisine_counts['Cuisine'], cuisine_counts['Total'], color='#FC8019')
    for bar in ax.patches:
        ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
                f'{int(bar.get_width()):,}', va='center', fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel('Number of Restaurants')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()    

st.markdown("---")

# ── Row 2: Price vs Rating ─────────────────────────────────────
st.subheader("💸 Does Spending More Mean Better Food?")

price_data = filtered_data.groupby('Price range')['Aggregate rating'].mean().reset_index()
price_data.columns = ['Price Range', 'Avg Rating']
price_data['Price Range'] = price_data['Price Range'].map({
    1: 'Budget', 2: 'Mid', 3: 'Premium', 4: 'Luxury'
})

fig, ax = plt.subplots(figsize=(10, 4))
color_map = {'Budget': '#2ecc71', 'Mid': '#3498db', 
             'Premium': '#9b59b6', 'Luxury': '#e74c3c'}
bar_colors = [color_map.get(p, '#95a5a6') for p in price_data['Price Range']]
bars = ax.bar(price_data['Price Range'], price_data['Avg Rating'],
              color=bar_colors, width=0.4)
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 0.01,
            f'{height:.2f}', ha='center', fontsize=11, fontweight='bold')
ax.set_ylim(2.5, 4.5)
ax.set_ylabel('Average Rating')
if len(filtered_data) > 0:
    avg = filtered_data['Aggregate rating'].mean()
    ax.axhline(y=avg, color='gray', linestyle='--', linewidth=1.5,
               label=f'Current avg: {avg:.2f}')
    ax.legend()
plt.tight_layout()
st.pyplot(fig)
plt.close()

st.markdown("---")

# ── Row 3: Rating Distribution ─────────────────────────────────
st.subheader("📊 Rating Distribution")

fig, ax = plt.subplots(figsize=(10, 4))
ax.hist(filtered_data['Aggregate rating'], bins=20,
        color='#E23744', edgecolor='white', linewidth=0.5)
if len(filtered_data) > 0:
    avg = filtered_data['Aggregate rating'].mean()
    ax.axvline(x=avg, color='#2c3e50', linestyle='--',
               linewidth=2, label=f'Average: {avg:.2f}')
    ax.legend()
ax.set_xlabel('Rating')
ax.set_ylabel('Number of Restaurants')
plt.tight_layout()
st.pyplot(fig)
plt.close()

st.markdown("---")

# ── Row 4: Top Restaurants Table ───────────────────────────────
st.subheader("🏆 Top Rated Restaurants")

top_restaurants = filtered_data[filtered_data['Votes'] > 100].sort_values(
    'Aggregate rating', ascending=False).head(10)[
    ['Restaurant Name', 'City', 'Primary Cuisine', 
     'Aggregate rating', 'Votes', 'Average Cost for two']
].reset_index(drop=True)
top_restaurants.index += 1
top_restaurants.columns = ['Name', 'City', 'Cuisine', 'Rating', 'Votes', 'Cost for Two']
st.dataframe(top_restaurants, use_container_width=True)


st.markdown("---")

# ── Row 5: Insight Cards ───────────────────────────────────────
st.subheader("💡 Key Insights")

i1, i2 = st.columns(2)
with i1:
    st.info("🏙️ **Delhi Dominates** — 62% of all Indian restaurants on Zomato are in Delhi NCR, making it the most food-dense region in the dataset.")
    st.info("💰 **Price = Quality** — Luxury restaurants (₹2000+) rate 16% higher than budget ones. Spending more does get you better food.")
with i2:
    st.info("🍛 **North Indian Oversaturation** — North Indian cuisine has 1,350 restaurants in Delhi but only a 3.27 avg rating — the most oversaturated market.")
    st.info("🚴 **Delivery Doesn't Mean Better** — Online delivery restaurants rate only 0.03 higher than non-delivery ones. Convenience ≠ quality.")

st.markdown("---")

# ── Footer ─────────────────────────────────────────────────────
st.markdown("Built by **Nupur Dharpure** | Data Source: Zomato via Kaggle | Tools: Python, Pandas, SQL, Streamlit")