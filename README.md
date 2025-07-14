📧 Email Phishing Detection Using Machine Learning

A smart system that detects phishing emails in real time using machine learning and sends instant alerts via Telegram. It integrates Gmail API, XGBoost classifier, and a Streamlit interface to offer a practical cybersecurity solution.

🚀 Project Overview

Phishing attacks are a major cybersecurity concern, often tricking users into revealing sensitive information. This project addresses the problem by using a machine learning-based system to detect phishing emails. It automatically reads unread emails from Gmail, analyzes the content, classifies the email as *phishing* or *legitimate*, and sends alerts through Telegram.

🧠 Features

- ✅ XGBoost-based email phishing classification
- ✅ Real-time email scanning using Gmail API
- ✅ Streamlit web interface for testing
- ✅ Telegram bot notifications on detection
- ✅ TF-IDF vectorization for text analysis
- ✅ Scheduled scans using the `schedule` library

🛠️ Tech Stack

- Language: Python 3.x  
- Machine Learning: XGBoost, scikit-learn  
- Text Vectorization: TF-IDF  
- APIs: Gmail API, Telegram Bot API  
- Frontend: Streamlit  
- Scheduler: schedule, time  
- Storage: Pickle (`.pkl` files)

🗂️ Folder Structure

📁 EmailPhishingDetector/
├── train_model.py # Train and save model
├── phishing_model.pkl # Saved XGBoost model
├── vectorizer.pkl # Saved TF-IDF vectorizer
├── read_gmail.py # Gmail API integration
├── telegram_notifier.py # Sends Telegram alerts
├── app.py # Streamlit UI
├── credentials.json # Gmail OAuth credentials
├── token.pickle # Gmail OAuth token
├── emails.csv # Dataset
├── README.md # Project documentation

📊 How It Works

1. Collect and label emails in `emails.csv`
2. Train model using XGBoost + TF-IDF
3. Authenticate with Gmail API using `credentials.json`
4. Read unread emails via Gmail
5. Predict using trained model
6. Notify users of phishing via Telegram bot
7. Streamlit app allows manual testing

📈 Results

- Achieved **95%+ accuracy** on test data
- Accurately detected phishing emails with suspicious links/words
- Successfully sent real-time Telegram alerts


## 📷 Screenshots
<img width="1920" height="1080" alt="Screenshot (93)" src="https://github.com/user-attachments/assets/0157059e-3bd1-417d-8983-f99fdb26fefa" />
<img width="1920" height="1080" alt="Screenshot (94)" src="https://github.com/user-attachments/assets/6dd7e8a6-1593-4104-bc14-517141763934" />
<img width="1920" height="1080" alt="Screenshot (95)" src="https://github.com/user-attachments/assets/413afe2e-e0e3-485b-97dc-37b3614be132" />
<img width="1444" height="978" alt="Screenshot 2025-07-14 235044" src="https://github.com/user-attachments/assets/9813b255-9151-46f6-84ac-3de6a35a15c3" />

---

## 🔮 Future Scope

- Add browser extension for inbox-level alerts  
- Use deep learning (BERT/LSTM) for better language understanding  
- Enable multi-language phishing detection  
- Add reporting dashboard for monitoring phishing attempts  

---

## 📚 References

1. [A Machine Learning Approach to Phishing Email Detection – IJCA](https://doi.org/10.5120/ijca2017912961)  
2. [Detecting Phishing Emails using ML – IRJET](https://www.irjet.net/archives/V6/i4/IRJET-V6I4196.pdf)  
3. [Phishing Email Detection – IEEE Paper](https://ieeexplore.ieee.org/document/9400545)  
4. [Springer: ML in Phishing Detection](https://link.springer.com/chapter/10.1007/978-981-15-6403-1_67)  
5. [Elsevier: Procedia Computer Science](https://doi.org/10.1016/j.procs.2020.03.175)

---

## 🙋‍♂️ Author

- **Name:** Pragatishvar A  
- **Email:** *praga.jv@gmail.com*  
- **GitHub:** [https://github.com/Praga-925](https://github.com/Praga-925))  
- **LinkedIn:** *[www.linkedin.com/in/pragatishvar-a-72b863325]*

---

## 📜 License

This project is for educational and research purposes only. Free to modify and share with credit.
