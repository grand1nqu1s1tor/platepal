# Platepal: A Dining Concierge Chatbot

**Platepal** is a server-less, microservice-driven web application that acts as a Dining Concierge chatbot, offering personalized restaurant recommendations based on user preferences. This chatbot utilizes Natural Language Processing (NLP) to transform how users discover dining options by providing tailored suggestions through conversational interaction.

## 🚀 Features

- **Serverless Architecture**: Built on a microservices model, utilizing serverless technologies to minimize infrastructure management.
- **Restaurant Suggestions**: Provides restaurant recommendations based on user preferences, such as cuisine type, location, and price range.
- **Real-Time Interaction**: Uses NLP to converse naturally, allowing users to input preferences conversationally.
- **Email Notifications**: Sends restaurant recommendations to users via email, enhancing usability and convenience.

## ☁️ Cloud-Based Components

Platepal is built using **AWS Services** to deliver a scalable, serverless experience that efficiently serves user needs:

- **Scalability**: Capable of handling concurrent requests, adapting to varying user demands.
- **Cost Efficiency**: Leveraging the serverless model to only pay for what is used.
- **Highly Available**: Ensures that users can always interact with Platepal, regardless of load.

## 🛠 Tech Stack

**Frontend**: Deployed using Amazon S3, allowing a simple and scalable way to host the starter front-end application.

**Backend**: AWS Lambda functions in a microservice architecture to facilitate chatbot operations.

**Cloud Services & Infrastructure**:
- **Amazon S3**: For hosting the front-end application.
- **API Gateway**: Manages API calls, providing authorization and routing for incoming requests.
- **Amazon Lex**: Creates conversational interfaces that allow users to interact with Platepal through text.

**Lambda Functions**:
1. **LF0**: Facilitates chat operations using request/response models.
2. **LF1**: Validates user input and formats bot responses before responding.
3. **LF2**: Performs search operations to get restaurant suggestions and sends email notifications to users.

**Messaging & Notifications**:
- **Amazon SQS**: Collects information provided by users.
- **Amazon SNS**: Sends email notifications to users with restaurant recommendations.

**Database**:
- **DynamoDB**: Stores restaurant data scraped from Yelp.
- **ElasticSearch/OpenSearch**: Stores indices and cuisine data to facilitate search operations.

## ⚙️ Architecture Diagram

Below is an overview of the architecture design of Platepal. The diagram shows how different AWS components work together to serve user requests efficiently.

![Architecture Diagram](./platepal-architecture-diagram.png)

## ❓ How Does Platepal Work?

- **S3 Bucket**: Deploys the front-end for users to interact with the chatbot.
- **API Gateway**: Handles incoming API requests and routes them appropriately.
- **Amazon Lex**: Manages conversational logic and NLP to interact with users.
- **Lambda Functions**: Facilitate chat, validate user inputs, and perform restaurant searches.
- **DynamoDB**: Stores restaurant details.
- **ElasticSearch/OpenSearch**: Provides indexing for efficient search.
- **SNS**: Sends personalized restaurant recommendations to users.

## 🎥 Demo Video

Watch the [YouTube Demo Video](https://youtu.be/gcmoA_8cuAw) to see Platepal in action and understand its features and capabilities.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

Developed by the **Dipesh Parwani & Naman Soni** team.
The development was moved and completed locally via CLI.
RIP to this REPO.
