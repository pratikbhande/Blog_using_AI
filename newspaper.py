import streamlit as st
import urllib.request
import json
import requests
import os
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = "sk-proj-pGNAhPvMLalbkFJI5atjbumZmgfmAIA"  # Replace with your OpenAI API key

def fetch_ai_news():
    """
    Fetches top AI news using the GNews API and returns a list of article links.
    """
    api_key = "4e21d7361fdd189f4243c9df6725fb60"  # Replace with your actual GNews API key 
    url = f"https://gnews.io/api/v4/search?q=f1+race&lang=en&country=us&max=5&sortby=publishedAt&apikey={api_key}"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode("utf-8"))
            articles = data.get("articles", [])
            links = [article.get("url") for article in articles if article.get("url")]
            return links
    except Exception as e:
        st.error(f"An error occurred while fetching AI news: {e}")
        return []

def scrape_jina_ai(url: str) -> str:
    """
    Scrapes the content of a given link using Jina AI.
    """
    try:
        response = requests.get("https://r.jina.ai/" + url)
        if response.status_code == 200:
            return response.text
        else:
            st.error(f"Failed to fetch the content from {url}. Status code: {response.status_code}")
            return ""
    except Exception as e:
        st.error(f"An error occurred while scraping {url}: {e}")
        return ""

def generate_blog(content: str, title: str) -> str:
    """
    Generates a professional-quality blog based on the scraped content.
    """
    chat = ChatOpenAI(model="gpt-4o-mini")
    messages = [
        SystemMessage(
            content="""You are a professional blog writer specializing in creating detailed, insightful, and engaging blogs. Use the provided content to generate a blog that follows this structure:

            1. A compelling Introduction: Briefly introduce the topic, setting the context and importance.
            2. Key Insights and Analysis: Provide in-depth analysis, key takeaways, and detailed insights derived from the content. Highlight any data, statistics, or case studies.
            3. Practical Applications and Use Cases: Showcase real-world applications or examples related to the topic.
            4. A Thoughtful Conclusion: Wrap up the blog by summarizing the main points, implications, and potential future developments.

            Ensure your writing is professional, conversational, and maintains a reader-friendly tone. Use subheadings and bullet points where appropriate to improve readability. Pay close attention to grammar, formatting, and style to align with high-quality publishing standards."""
        ),
        HumanMessage(content=f"Content: {content}\n\nGenerate a blog titled: {title}")
    ]
    response = chat(messages)
    return response.content

def generate_newspaper(summaries: list) -> str:
    """
    Generates a newspaper format with summaries of the links.
    """
    chat = ChatOpenAI(model="gpt-4o-mini")
    messages = [
        SystemMessage(
            content="""You are a professional content editor. Create an engaging newspaper format that includes summaries of multiple articles. Each section should have:
            
            1. A headline summarizing the article.
            2. A brief paragraph explaining the key details in an engaging manner.

            Ensure the tone is professional and easy to read, with proper structure and formatting."""
        ),
        HumanMessage(content="\n\n".join(f"Article {i+1}: {summary}" for i, summary in enumerate(summaries)))
    ]
    response = chat(messages)
    return response.content

def save_blog_to_file(title: str, blog: str):
    """
    Saves the generated blog to a text file.
    """
    filename = title.replace(" ", "_").lower() + ".txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(blog)
    st.success(f"Blog saved as {filename}")

# Streamlit App
st.title("AI News Blog Generator")

# State Management
if "links" not in st.session_state:
    st.session_state.links = []
if "blogs" not in st.session_state:
    st.session_state.blogs = {}
if "custom_blog" not in st.session_state:
    st.session_state.custom_blog = ""
if "newspaper" not in st.session_state:
    st.session_state.newspaper = ""

# Option 1: Latest AI News
if st.button("Fetch Latest AI News"):
    st.session_state.links = fetch_ai_news()

if st.session_state.links:
    st.subheader("Latest AI News Links")
    for i, link in enumerate(st.session_state.links, start=1):
        st.write(f"{i}. {link}")

    selected_links_input = st.text_input("Enter the numbers of the links you're interested in (e.g., 1,2,3):")

    if st.button("Generate Blogs for Selected Links"):
        try:
            indices = [int(num.strip()) - 1 for num in selected_links_input.split(",") if num.strip().isdigit()]
            valid_indices = [i for i in indices if 0 <= i < len(st.session_state.links)]

            if not valid_indices:
                st.error("No valid selections made.")
            else:
                for index in valid_indices:
                    url = st.session_state.links[index]
                    st.write(f"Scraping data from: {url}")
                    scraped_content = scrape_jina_ai(url)
                    if scraped_content:
                        title = f"Blog for Link {index + 1}"
                        blog = generate_blog(scraped_content, title)
                        st.session_state.blogs[title] = blog

        except Exception as e:
            st.error(f"An error occurred: {e}")

if st.session_state.blogs:
    for title, blog in st.session_state.blogs.items():
        st.text_area(title, blog, height=300)
        if st.button(f"Save {title}", key=f"save_{title}"):
            save_blog_to_file(title, blog)

# Option 2: Custom News Link
st.subheader("Input Your Own News Link")
custom_link = st.text_input("Enter a custom news link:")
if st.button("Generate Blog for Custom Link"):
    if custom_link:
        scraped_content = scrape_jina_ai(custom_link)
        if scraped_content:
            title = "Blog for Custom Link"
            st.session_state.custom_blog = generate_blog(scraped_content, title)

if st.session_state.custom_blog:
    st.text_area("Generated Blog", st.session_state.custom_blog, height=300)
    if st.button("Save Custom Blog"):
        save_blog_to_file("Blog for Custom Link", st.session_state.custom_blog)

# Option 3: Generate AI Newspaper
if st.button("Create AI Newspaper"):
    try:
        if not st.session_state.links:
            st.error("Please fetch AI news first.")
        else:
            summaries = []
            for url in st.session_state.links:
                scraped_content = scrape_jina_ai(url)
                if scraped_content:
                    summaries.append(scraped_content)

            if summaries:
                st.session_state.newspaper = generate_newspaper(summaries)
            else:
                st.error("No content available to create a newspaper.")
    except Exception as e:
        st.error(f"An error occurred while creating the newspaper: {e}")

if st.session_state.newspaper:
    st.text_area("AI Newspaper", st.session_state.newspaper, height=500)
    if st.button("Save AI Newspaper"):
        save_blog_to_file("AI_Newspaper", st.session_state.newspaper)































