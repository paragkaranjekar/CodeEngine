# CodeEngine
Try it out at: https://codeengine-tra0.onrender.com/
# Question Search Tool

This project is a question search tool that helps users find questions from platforms like LeetCode and Codeforces based the search query and sorts them according to relevance to query and difficulty level.
The tool utilizes Flask for the backend and TF-IDF for ranking the search results in preference order.
The questions data from LeetCode and Codeforces has been preprocessed for efficient searching using the TF-IDF algorithm. The preprocessed data includes the question text, difficulty level, and other relevant data.

## Features

- User-friendly web interface for searching questions
- Support for LeetCode and Codeforces for retrieving question data
- TF-IDF-based ranking to sort search results by relevance
- Support for sorting according to difficulty level of questions
- Flask backend for handling user requests and serving search results
