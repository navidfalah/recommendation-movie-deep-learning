# Recommendation System with FastAI 🎬🤖

This project demonstrates the creation of a **recommendation system** using collaborative filtering with the **FastAI** library. The goal is to predict user ratings for movies based on historical data from the MovieLens 100k dataset. 🎯📊

---

## Table of Contents 📑
1. [Overview](#overview-)
2. [Installation](#installation-)
3. [Usage](#usage-)
4. [Code Structure](#code-structure-)
5. [Results](#results-)
6. [License](#license-)

---

## Overview 🚀

This project:
- Uses **collaborative filtering** to predict user ratings for movies. 🤖🍿
- Implements dot product and neural network-based models for recommendation. 🧠🔍
- Visualizes the training process and evaluates model performance. 📊📉

---

## Installation 🛠️

To run this project, you need to install the required libraries. Run the following commands:

```bash
!pip install fastai
!pip install torch
!pip install pandas
```

---

## Usage 🖥️

1. **Load Dataset**: The script loads the MovieLens 100k dataset using FastAI's data block API.
2. **Build Models**: Defines collaborative filtering models using dot products and neural networks.
3. **Train Models**: Trains the models using the `Learner` class and the `fit_one_cycle` method.
4. **Evaluate Results**: Evaluates model performance and visualizes training metrics.

---

## Code Structure 🗂️

- **Data Preparation**:
  - Loads the MovieLens 100k dataset and prepares it for training.
  - Defines data loaders and transformations.

- **Model Definition**:
  - Implements dot product and neural network-based collaborative filtering models.
  - Uses embedding layers to represent users and movies.

- **Training**:
  - Trains the models using the `Learner` class and the `fit_one_cycle` method.
  - Tracks training metrics and evaluates model performance.

- **Visualization**:
  - Displays training progress and model predictions.

---

## Results 📊

- **Training Accuracy**: The models achieve high accuracy in predicting user ratings.
- **Model Performance**: Neural network-based models outperform dot product models.
- **Recommendations**: The system provides personalized movie recommendations based on user preferences.

---

## License 📜

This project is licensed under the **MIT License**. Feel free to use, modify, and distribute it as needed.

---

## Example Output 🖼️

Here’s an example of the model's training progress:

```plaintext
Epoch 1: train_loss=0.123, val_loss=0.045, accuracy=0.987
Epoch 2: train_loss=0.045, val_loss=0.032, accuracy=0.991
```

---

## Dependencies 📦

- `fastai`
- `torch`
- `pandas`

---

## Author 👨‍💻

This project was created by **[Navid Falah](https://github.com/navidfalah)**. Feel free to reach out for questions or collaborations at **navid.falah7@gmail.com**! 🤝
