# Databricks Billing

![](https://img.shields.io/github/stars/charliewei0716/databricks-billing?style=social)

This is a web application that integrates a [Databricks Dashboard](https://docs.databricks.com/aws/en/dashboards/) with a [Mosaic AI Agent](https://docs.databricks.com/aws/en/generative-ai/tutorials/agent-framework-notebook) chat interface. The billing dashboard serves as the main display, and it is generated using [Databricks System Tables](https://docs.databricks.com/aws/en/admin/system-tables/) and cloud infrastructure cost data as its sources. Additionally, a multi-agent assistant, built with [Databricks Genie](https://docs.databricks.com/aws/en/genie/) and [RAG](https://docs.databricks.com/aws/en/generative-ai/retrieval-augmented-generation), enables users to ask any questions about the dashboard in natural language and receive responses.

![image](/assets/app_ui.png)

# Key Features

- Data
  - Completed data fusion integration process for Databricks system tables and cloud infrastructure cost.
  - Used AI_FORECAST to predict DBU and VM usage for the coming year.
  - Built an index table for RAG using the [Databricks Documentation Dataset](https://marketplace.databricks.com/details/03bbb5c0-983d-4523-833a-57e994d76b3b/Databricks_Databricks-Documentation-Dataset) from Databricks Marketplace.
- AI/BI Dashboard
  - Presented DBU cost and infrastructure cost at the job level.
  - Optimized the DBU overview dashboard with cross-filtering functionality.
  - Automatically refreshed the dashboard after ETL in workflows using dashboard tasks.
  - Accelerated dashboard loading and saved SQL warehouse costs through embedded credentials and caching mechanisms.
- AI/BI Genie
  - Created billing genie by preparing table & column comments, sample questions, and general instructions.
  - Improved Genie’s accuracy by using value dictionaries.
  - Utilized Genie API.
- Agent
  - Built and deployed multi-agent architecture using LangGraph with supervisor structure on Databricks Model Serving.
  - Created an Agent using the GenieAgent class to connect to the Genie room.
  - Developed a ReAct agent for document retrieval via Vector Search.
- Apps
  - Embedded dashboard into custom web applications.
  - Developed web applications using Streamlit and deployed them on Databricks Apps.

# Architecture

![image](/assets/architecture.gif)
