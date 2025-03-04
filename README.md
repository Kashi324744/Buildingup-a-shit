# Buildup-a-sh**t
# Interactive Storytelling Game

## Overview
This project is a text-based interactive storytelling game where players make real-time decisions that shape the narrative. The game dynamically generates stories across different genres using Gemini AI and provides an engaging gameplay experience.

## Features
- **AI-Powered Storytelling** – Generates unique, engaging thriller-based scenarios using Gemini AI.
- **Choice-Driven Gameplay** – Players make real-time decisions that influence the story’s direction.
- **PDF Export & S3 Integration** – Saves the chat history as a PDF and uploads it to AWS S3 for easy access.
- **AWS EC2 Deployment** – Hosted on AWS EC2 for seamless accessibility.

## Technologies Used
- **Streamlit** – UI framework for building the interactive experience.
- **Google Gemini AI** – Generates dynamic stories and processes user actions.
- **AWS S3** – Stores exported game history PDFs.
- **AWS EC2** – Hosts the game for online access.
- **PDFKit** – Converts chat logs into PDF format.

## Installation & Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/interactive-story-game.git
   cd interactive-story-game
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up API keys in the script:
   - **Google Gemini AI API Key**
   - **AWS Access & Secret Key**
   - **S3 Bucket Name**
4. Run the application:
   ```sh
   streamlit run app.py
   ```

## Usage
1. Click on **🎲 New Story** to generate a fresh AI-powered scenario.
2. Type your action in the input box and submit to continue the narrative.
3. Use the **Export** button to save and upload the chat log as a PDF to AWS S3.

## Future Enhancements
- **Multiplayer Mode** – Enable collaborative or competitive storytelling.
- **Voice Input & Narration** – Players can speak choices, and AI narrates the story.
- **Personality Analysis** – AI evaluates decision patterns for unique insights.
- **AI-Generated Visuals** – Adds dynamic imagery to enhance immersion.

## Author
Kashish Khangarot

