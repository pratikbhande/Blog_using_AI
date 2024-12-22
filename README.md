# AI News Blog Generator

## Project Overview
The **AI News Blog Generator** is a streamlined tool designed to automate the creation of high-quality blogs on AI-related topics. Users can either fetch the latest AI news or provide custom links to generate professional-grade blogs quickly and efficiently.

## Features
- **Fetch Latest AI News**: Utilizes the GNews API to retrieve the top 5 AI news articles daily.
- **Blog Generation from News**: Allows users to select any fetched news article to generate a blog.
- **Custom Link Support**: Users can input any AI-related news link to generate a detailed blog.
- **Lightweight Data Scraping**: Implements Jina for efficient and lightweight data extraction.
- **AI-Powered Blog Writing**: Leverages the GPT-4o-mini model to create insightful, structured, and polished blogs.

## How It Works
1. **Fetch AI News**:
   - The app retrieves the latest top 5 AI news articles from GNews.
   - Users can review the articles and select specific ones for blog creation.

2. **Custom News Input**:
   - Users can input their own AI-related news links.
   - The app scrapes the content and generates a blog based on the provided link.

3. **Blog Generation**:
   - Blogs are crafted with a structured format, including an introduction, key insights, practical applications, and a conclusion.
   - Ensures a professional tone and reader-friendly layout.

4. **Save Blogs**:
   - Generated blogs can be saved as text files for further use.

## Technologies Used
- **Python**: Core language for development.
- **Streamlit**: Provides an interactive user interface.
- **GNews API**: Fetches the latest AI news articles.
- **Jina**: Lightweight solution for data scraping.
- **GPT-4o-mini Model**: Generates high-quality, professional blogs.

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo-name/ai-news-blog-generator.git
   ```
2. Navigate to the project directory:
   ```bash
   cd ai-news-blog-generator
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage
1. Launch the Streamlit app.
2. Use the "Fetch Latest AI News" feature to retrieve and select AI news articles for blog generation.
3. Input custom AI-related news links to generate blogs.
4. View and save the generated blogs as text files.

## Contribution
Contributions are welcome! Please fork the repository, create a feature branch, and submit a pull request.

