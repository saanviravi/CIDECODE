import json
import random

# Step 1: Load Dataset
def load_dataset(file_path):
    with open(file_path, 'r') as file:
        dataset = json.load(file)
    return dataset

# Step 2: Calculate Threat Scores
def calculate_threat_scores(dataset):
    threat_scores = []
    malicious_keywords = ['hack', 'fraud', 'illegal', 'weapon', 'drugs', 'exploit', 'phishing', 'scam', 'malware', 'virus', 'ransomware', 'botnet', 'cybercrime', 'identity theft', 'spam', 'spyware', 'trojan', 'rootkit', 'keylogger', 'data breach', 'pharma', 'counterfeit', 'money laundering', 'credit card fraud', 'child exploitation', 'terrorism', 'extortion', 'fraudulent', 'cyber attack', 'hacker forum', 'dark web', 'identity fraud', 'credit card theft', 'phishing scam', 'hijacking', 'cyber espionage', 'identity cloning', 'password theft', 'data theft', 'DDoS attack', 'cryptojacking', 'email spoofing', 'identity fraud', 'forgery', 'carding', 'illegal services', 'botnet', 'exploitation', 'cyber warfare', 'malvertising', 'social engineering', 'identity manipulation', 'data manipulation']

    for item in dataset:
        title = item.get('title', '')
        if isinstance(title, dict):
            title = ' '.join(map(str, title.values()))  # Convert values to string before joining
        title = str(title).lower()  # Ensure title is converted to lowercase string
        description = item.get('description', '')
        if isinstance(description, dict):
            description = ' '.join(map(str, description.values()))  # Convert values to string before joining
        description = str(description).lower()  # Ensure description is converted to lowercase string
        word_frequency = item.get('word_frequency', {})
        
        # Count occurrence of malicious keywords in title
        title_threat_score = sum(title.count(keyword) for keyword in malicious_keywords)
        
        # Count occurrence of malicious keywords in description
        description_threat_score = sum(description.count(keyword) for keyword in malicious_keywords)
        
        # Calculate threat score based on word frequency of malicious terms
        word_frequency_threat_score = sum(word_frequency.get(keyword, 0) for keyword in malicious_keywords)
        
        # Combine all threat scores
        total_threat_score = title_threat_score + description_threat_score + word_frequency_threat_score
        
        threat_scores.append(total_threat_score)
    
    return threat_scores


# Step 3: Generate Reports and Alerts
def generate_reports(dataset, threat_scores):
    # Define threshold for triggering alerts
    alert_threshold = 1  # Adjust as needed
    alerts = []
    for idx, score in enumerate(threat_scores):
        if score >= alert_threshold:
            alerts.append({
                'index': idx,
                'URL': dataset[idx]['url'],
                'Threat Score': score,
                # Add more information as needed
            })
    
    if alerts:
        print("Alerts Detected:")
        for alert in alerts:
            print(f"URL: {alert['URL']}, Threat Score: {alert['Threat Score']}")
    else:
        print("No Alerts Detected.")


# Step 4: Main Function
def main():
    # Step 1: Load Dataset
    file_path = 'scraped_data.json'  # Provide the path to your dataset
    dataset = load_dataset(file_path)

    # Step 2: Select a random sample of URLs from the dataset
    random_urls = random.sample(dataset, k=5)  # Change the value of k as needed
    
    # Step 3: Calculate Threat Scores for the random sample
    threat_scores = calculate_threat_scores(random_urls)

    # Step 4: Generate Reports and Alerts for the random sample
    generate_reports(random_urls, threat_scores)

# Entry point of the script
if __name__ == "__main__":
    main()
