import json
import random
import csv

# Step 1: Load Dataset from JSON
def load_json_dataset(file_path):
    with open(file_path, 'r') as file:
        dataset = json.load(file)
    return dataset

# Step 1: Load Dataset from CSV
def load_csv_dataset(file_path):
    dataset = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dataset.append({'text': row['text'], 'sentiment': int(row['sentiment_numeric'])})
    return dataset

# Step 2: Calculate Threat Scores
def calculate_threat_scores(dataset, is_json):
    threat_scores = []
    malicious_keywords = ['hack', 'fraud', 'illegal', 'weapon', 'drugs', 'exploit', 'phishing', 'scam', 'malware', 'virus', 'ransomware', 'botnet', 'cybercrime', 'identity theft', 'spam', 'spyware', 'trojan', 'rootkit', 'keylogger', 'data breach', 'pharma', 'counterfeit', 'money laundering', 'credit card fraud', 'child exploitation', 'terrorism', 'extortion', 'fraudulent', 'cyber attack', 'hacker forum', 'dark web', 'identity fraud', 'credit card theft', 'phishing scam', 'hijacking', 'cyber espionage', 'identity cloning', 'password theft', 'data theft', 'DDoS attack', 'cryptojacking', 'email spoofing', 'identity fraud', 'forgery', 'carding', 'illegal services', 'botnet', 'exploitation', 'cyber warfare', 'malvertising', 'social engineering', 'identity manipulation', 'data manipulation']

    for item in dataset:
        if is_json:
            title = item.get('title', '')
            if isinstance(title, dict):
                title = ' '.join(map(str, title.values()))  # Convert values to string before joining
            title = str(title).lower()  # Ensure title is converted to lowercase string
            description = item.get('description', '')
            if isinstance(description, dict):
                description = ' '.join(map(str, description.values()))  # Convert values to string before joining
            description = str(description).lower()  # Ensure description is converted to lowercase string
            word_frequency = item.get('word_frequency', {})
        else:
            title = item['text'].lower()
            description = ''
            word_frequency = {}

        # Count occurrence of malicious keywords in title
        title_threat_score = sum(title.count(keyword) for keyword in malicious_keywords)
        
        # Calculate threat score based on word frequency of malicious terms
        word_frequency_threat_score = sum(word_frequency.get(keyword, 0) for keyword in malicious_keywords)
        
        # Combine all threat scores
        total_threat_score = title_threat_score + word_frequency_threat_score

        # Adjust the threat score based on sentiment
        sentiment = item.get('sentiment', 2)  # Default sentiment to neutral (2) if not provided
        if sentiment == 0:  # Positive sentiment
            total_threat_score -= 1
        elif sentiment == 1:  # Negative sentiment
            total_threat_score += 1
        
        threat_scores.append(total_threat_score)
    
    return threat_scores

# Step 3: Generate Reports and Alerts
def generate_reports(dataset, threat_scores, is_json):
    # Define threshold for triggering alerts
    alert_threshold = 1  # Adjust as needed
    alerts = []
    for idx, score in enumerate(threat_scores):
        if score >= alert_threshold:
            if is_json:
                url = dataset[idx]['url']
            else:
                url = f'CSV Row {idx + 1}'
            alerts.append({
                'index': idx,
                'URL': url,
                'Threat Score': score,
            })
    
    if alerts:
        print("Alerts Detected:")
        for alert in alerts:
            print(f"URL: {alert['URL']}, Threat Score: {alert['Threat Score']}")
    else:
        print("No Alerts Detected.")

# Step 4: Main Function
def main():
    # Step 1: Load Dataset from JSON
    json_file_path = 'scraped_data.json'  # Provide the path to your JSON dataset file
    json_dataset = load_json_dataset(json_file_path)

    # Step 2: Load Dataset from CSV
    csv_file_path = 'data_1.csv'  # Provide the path to your CSV dataset file
    csv_dataset = load_csv_dataset(csv_file_path)

    # Step 3: Calculate Threat Scores for JSON and CSV datasets separately
    json_threat_scores = calculate_threat_scores(json_dataset, is_json=True)
    csv_threat_scores = calculate_threat_scores(csv_dataset, is_json=False)

    # Step 4: Generate Reports and Alerts for JSON and CSV datasets separately
    print("Alerts Detected in JSON Dataset:")
    generate_reports(json_dataset, json_threat_scores, is_json=True)
    
    print("\nAlerts Detected in CSV Dataset:")
    generate_reports(csv_dataset, csv_threat_scores, is_json=False)

# Entry point of the script
if __name__ == "__main__":
    main()
