# MilkQu - Web-Based Machine Learning App for Milk Quality Prediction

MilkQu is an innovative web-based application powered by machine learning, designed to help users predict the quality of milk accurately and efficiently. This app provides real-time predictions based on multiple milk quality parameters, enabling users to make informed decisions about milk storage, processing, and consumption.

## Features

- **User-Friendly Interface**: Simple and intuitive design for ease of use.
- **Comprehensive Parameter Analysis**: Evaluate milk quality based on multiple parameters like pH, temperature, color, taste, odor, fat content, and turbidity.
- **Real-Time Prediction**: Get instant results indicating milk quality (High, Medium, or Low).
- **Prediction History**: Keep track of all your previous predictions for future reference.
- **Detailed Insights**: Additional relevant information is provided for better understanding of milk quality.

## How It Works

Follow these steps to predict milk quality:

1. **Enter Identity**: Start by providing your identity for record purposes.
2. **Input Parameters**:
   - **pH**: Enter the pH value for acidity measurement.
   - **Temperature**: Specify the temperature to determine storage or processing conditions.
   - **Color**: Indicate any visual changes in the milk.
   - **Taste**: Detect acidity or flavor changes in the milk.
   - **Odor**: Evaluate the freshness of the milk based on smell.
   - **Fat**: Determine the nutritional value and consistency of the milk.
   - **Turbidity**: Measure milk clarity as an indicator of quality.
3. **Submit for Prediction**:
   - Click the **‘Predict Milk Quality’** button to initiate the prediction process.
4. **View Results**:
   - Wait a moment while the system processes your input.
   - The prediction results will display in real-time, including the milk quality (High, Medium, or Low) and additional insights.
5. **Check Prediction History**:
   - Access the **Prediction History** section to review all your past predictions.

## Installation

Follow these steps to set up the MilkQu application locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/bimbingan-skripsi-jidan/prediction-milkqu-app.git
   ```
2. Navigate to the project directory:
   ```bash
   cd prediction-milkqu-app
   ```
3. Install dependencies:
   ```bash
   pip install streamlit
   ```
4. Start the development server:
   ```bash
   streamlit run app.py
   ```

## Usage

Once the application is running, open your browser and navigate to `http://localhost:8501/`. Follow the steps described in the "How It Works" section to predict milk quality.

## Contributing

We welcome contributions to enhance MilkQu. To contribute:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Add some feature"
   ```
4. Push the changes to your forked repository:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, feel free to contact us via email at <wildanavi2@gmail.com>.

---

Thank you for using MilkQu! We hope it helps you ensure the best quality of milk for your needs.