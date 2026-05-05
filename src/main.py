import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration with custom theme
st.set_page_config(
    page_title="Fashion Review Analytics",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    h1 {
        color: #2c3e50;
        font-weight: 700;
    }
    .stButton>button {
        background-color: #3498db;
        color: white;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Load dataset
df = pd.read_excel(r"C:\Users\KRITTIKA M G\Desktop\dev\Fashion_Product_Reviews_Sample.xlsx")

# Header section with gradient
st.markdown("""
    <div style='background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                padding: 30px; border-radius: 10px; margin-bottom: 30px;'>
        <h1 style='color: white; text-align: center; margin: 0;'>
            👗 Fashion Review Analytics Dashboard
        </h1>
        <p style='color: white; text-align: center; font-size: 18px; margin: 10px 0 0 0;'>
            Comprehensive insights into customer reviews, ratings & sentiment analysis
        </p>
    </div>
""", unsafe_allow_html=True)

# Sidebar with enhanced styling
st.sidebar.markdown("## 🎨 Filter Your Data")
st.sidebar.markdown("---")

# Initialize session state for filters
if 'reset_filters' not in st.session_state:
    st.session_state.reset_filters = False

# Reset filters if button was clicked
if st.session_state.reset_filters:
    st.session_state.reset_filters = False
    st.session_state.clear()

categories = st.sidebar.multiselect(
    "📦 Select Category",
    options=df["Category"].unique(),
    default=None,
    key='categories'
)

# Filter products based on selected categories
if categories:
    available_products = df[df["Category"].isin(categories)]["Product_Name"].unique()
else:
    available_products = df["Product_Name"].unique()

products = st.sidebar.multiselect(
    "👕 Select Product(s)",
    options=available_products,
    default=None,
    key='products'
)

# Add rating filter
rating_range = st.sidebar.slider(
    "⭐ Rating Range",
    min_value=1,
    max_value=5,
    value=(1, 5),
    key='rating_range'
)

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Reset Filters"):
    st.session_state.reset_filters = True
    st.rerun()

# Apply filters
filtered_df = df.copy()
if categories:
    filtered_df = filtered_df[filtered_df["Category"].isin(categories)]
if products:
    filtered_df = filtered_df[filtered_df["Product_Name"].isin(products)]
filtered_df = filtered_df[(filtered_df["Rating"] >= rating_range[0]) & (filtered_df["Rating"] <= rating_range[1])]

# Display review count
st.markdown(f"<h3 style='text-align: center; color: #34495e;'>📊 Displaying {len(filtered_df)} out of {len(df)} Reviews</h3>", unsafe_allow_html=True)
st.markdown("---")
# 📊 Key Metrics Row
st.markdown("### 📈 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_rating = round(filtered_df["Rating"].mean(), 2)
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 25px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <p style='color: rgba(255,255,255,0.8); font-size: 14px; margin: 0;'>⭐ Average Rating</p>
            <h2 style='color: white; margin: 10px 0 5px 0; font-size: 32px;'>{avg_rating}</h2>
            <p style='color: rgba(255,255,255,0.7); font-size: 12px; margin: 0;'>{avg_rating - 3:.2f} from baseline</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    total_reviews = len(filtered_df)
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 25px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <p style='color: rgba(255,255,255,0.8); font-size: 14px; margin: 0;'>📝 Total Reviews</p>
            <h2 style='color: white; margin: 10px 0 5px 0; font-size: 32px;'>{total_reviews}</h2>
            <p style='color: rgba(255,255,255,0.7); font-size: 12px; margin: 0;'>{round(total_reviews/len(df)*100, 1)}% of total</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    positive_pct = round((filtered_df["Sentiment"] == "Positive").sum() / len(filtered_df) * 100, 1)
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    padding: 25px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <p style='color: rgba(255,255,255,0.8); font-size: 14px; margin: 0;'>😊 Positive Sentiment</p>
            <h2 style='color: white; margin: 10px 0 5px 0; font-size: 32px;'>{positive_pct}%</h2>
            <p style='color: rgba(255,255,255,0.7); font-size: 12px; margin: 0;'>{positive_pct - 50:.1f}% from neutral</p>
        </div>
    """, unsafe_allow_html=True)

with col4:
    avg_review_length = round(filtered_df["Review_Text"].str.len().mean(), 0)
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
                    padding: 25px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <p style='color: rgba(255,255,255,0.8); font-size: 14px; margin: 0;'>📏 Avg Review Length</p>
            <h2 style='color: white; margin: 10px 0 5px 0; font-size: 32px;'>{int(avg_review_length)}</h2>
            <p style='color: rgba(255,255,255,0.7); font-size: 12px; margin: 0;'>characters</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# 📊 Charts Section
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 🎯 Sentiment Distribution")
    sentiment_counts = filtered_df["Sentiment"].value_counts()
    
    # Create interactive pie chart with Plotly
    fig1 = px.pie(
        values=sentiment_counts.values,
        names=sentiment_counts.index,
        color=sentiment_counts.index,
        color_discrete_map={'Positive':'#2ecc71', 'Neutral':'#f39c12', 'Negative':'#e74c3c'},
        hole=0.4
    )
    fig1.update_layout(
        showlegend=True,
        height=400,
        margin=dict(t=0, b=0, l=0, r=0)
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    st.markdown("### ⭐ Rating Distribution")
    rating_counts = filtered_df["Rating"].value_counts().sort_index()
    
    # Create colorful bar chart
    fig2 = px.bar(
        x=rating_counts.index,
        y=rating_counts.values,
        labels={'x': 'Rating', 'y': 'Count'},
        color=rating_counts.values,
        color_continuous_scale='viridis'
    )
    fig2.update_layout(
        showlegend=False,
        height=400,
        xaxis=dict(tickmode='linear')
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
# Second row of charts
col_left2, col_right2 = st.columns(2)

with col_left2:
    st.markdown("### 📦 Average Rating by Category")
    avg_rating_cat = filtered_df.groupby("Category")["Rating"].mean().sort_values(ascending=False)
    
    fig3 = px.bar(
        x=avg_rating_cat.values,
        y=avg_rating_cat.index,
        orientation='h',
        labels={'x': 'Average Rating', 'y': 'Category'},
        color=avg_rating_cat.values,
        color_continuous_scale='blues'
    )
    fig3.update_layout(
        showlegend=False,
        height=400
    )
    st.plotly_chart(fig3, use_container_width=True)

with col_right2:
    st.markdown("### 🎨 Sentiment by Category")
    sentiment_cat = filtered_df.groupby(['Category', 'Sentiment']).size().reset_index(name='Count')
    
    fig4 = px.bar(
        sentiment_cat,
        x='Category',
        y='Count',
        color='Sentiment',
        barmode='group',
        color_discrete_map={'Positive':'#2ecc71', 'Neutral':'#f39c12', 'Negative':'#e74c3c'}
    )
    fig4.update_layout(height=400)
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# Full width chart
st.markdown("### 🔥 Product Performance Heatmap")
product_sentiment = pd.crosstab(filtered_df['Product_Name'], filtered_df['Sentiment'])
if not product_sentiment.empty:
    fig5 = px.imshow(
        product_sentiment.T,
        labels=dict(x="Product", y="Sentiment", color="Count"),
        color_continuous_scale='RdYlGn',
        aspect='auto'
    )
    fig5.update_layout(height=400)
    st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")

# Sample Reviews Section
st.markdown("### 💬 Sample Customer Reviews")
tab1, tab2, tab3 = st.tabs(["😊 Positive", "😐 Neutral", "😞 Negative"])

with tab1:
    positive_reviews = filtered_df[filtered_df['Sentiment'] == 'Positive'].head(5)
    for idx, row in positive_reviews.iterrows():
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 15px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <strong style='color: white; font-size: 16px;'>⭐ {row['Rating']} - {row['Product_Name']} ({row['Category']})</strong><br>
            <em style='color: #f0f0f0; font-size: 14px;'>"{row['Review_Text']}"</em>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    neutral_reviews = filtered_df[filtered_df['Sentiment'] == 'Neutral'].head(5)
    for idx, row in neutral_reviews.iterrows():
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 20px; border-radius: 15px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <strong style='color: white; font-size: 16px;'>⭐ {row['Rating']} - {row['Product_Name']} ({row['Category']})</strong><br>
            <em style='color: #f0f0f0; font-size: 14px;'>"{row['Review_Text']}"</em>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    negative_reviews = filtered_df[filtered_df['Sentiment'] == 'Negative'].head(5)
    for idx, row in negative_reviews.iterrows():
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); padding: 20px; border-radius: 15px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <strong style='color: white; font-size: 16px;'>⭐ {row['Rating']} - {row['Product_Name']} ({row['Category']})</strong><br>
            <em style='color: #f0f0f0; font-size: 14px;'>"{row['Review_Text']}"</em>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #7f8c8d; padding: 20px;'>
        <p>✨ Fashion Review Analytics Dashboard | Powered by Streamlit & Plotly ✨</p>
    </div>
""", unsafe_allow_html=True)
