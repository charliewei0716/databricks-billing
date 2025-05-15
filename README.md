# Databricks Billing

![](https://img.shields.io/github/stars/charliewei0716/databricks-billing?style=social)

This Databricks Billing Solution is a web application that integrates the [Databricks AI/BI Dashboard]([https://docs.databricks.com/aws/en/dashboards](https://docs.databricks.com/aws/en/ai-bi/#aibi-dashboards)) with the [Mosaic AI Agent](https://docs.databricks.com/aws/en/generative-ai/agent-framework/build-genai-apps#-mosaic-ai-agent-framework) chat interface. It leverages [Databricks System Tables](https://docs.databricks.com/aws/en/admin/system-tables/) and cloud infrastructure cost data as its data sources, presenting both DBU and infrastructure costs at the job-level. This optimizes the current issue in the official [usage dashboards](https://docs.databricks.com/aws/en/admin/account-settings/usage) where cloud infrastructure costs are invisible.

The same data also serves as a source for [Databricks AI/BI Genie](https://docs.databricks.com/aws/en/ai-bi/#aibi-genie), combining RAG based on the Databricks Documentation to build a multi-agent assistant. This enables the assistant to answer non-technical users’ questions about the dashboard in natural language, retrieve historical cost data from different perspectives, and ultimately provide RI purchase recommendations based on predicted DBU usage.

![image](/assets/app_ui.png)

# Key Features

- Data
  - Completed data fusion integration process for Databricks system tables and cloud infrastructure cost.
  - Used [`AI_FORECAST`](https://docs.databricks.com/gcp/en/sql/language-manual/functions/ai_forecast) to predict DBU and VM usage for the coming year.
  - Built an index table for RAG using the [Databricks Documentation Dataset](https://marketplace.databricks.com/details/03bbb5c0-983d-4523-833a-57e994d76b3b/Databricks_Databricks-Documentation-Dataset) from Databricks Marketplace.
- AI/BI Dashboard
  - Presented DBU cost and infrastructure cost at the job level.
  - Optimized the DBU overview dashboard with [cross-filtering](https://docs.databricks.com/aws/en/dashboards#apply-cross-filtering) functionality.
  - Automatically refreshed the dashboard after ETL in workflows using [dashboard tasks](https://docs.databricks.com/aws/en/jobs/dashboard).
  - Accelerated dashboard loading and saved [SQL warehouse](https://docs.databricks.com/aws/en/compute/sql-warehouse/) costs through [embedded credentials](https://docs.databricks.com/aws/en/dashboards/share#data-for-shared-dashboards) and [caching mechanisms](https://docs.databricks.com/aws/en/dashboards/caching#caching-and-data-freshness).
- AI/BI Genie
  - Created billing genie by preparing table & column comments, sample questions, and general instructions.
  - Improved Genie’s accuracy by using [value dictionaries](https://docs.databricks.com/aws/en/genie/sample-values).
  - Utilized [Genie API](https://docs.databricks.com/api/workspace/genie).
- Agent
  - Built and deployed multi-agent architecture using [LangGraph](https://www.langchain.com/langgraph) with supervisor structure on [Mosaic AI Model Serving](https://docs.databricks.com/aws/en/machine-learning/model-serving/).
  - Created an Agent using the [GenieAgent](https://api-docs.databricks.com/python/databricks-ai-bridge/latest/databricks_langchain.html#databricks_langchain.GenieAgent) class to connect to the Genie room.
  - Developed a ReAct agent for document retrieval via [Mosaic AI Vector Search](https://docs.databricks.com/aws/en/generative-ai/vector-search).
- Apps
  - [Embedded dashboard](https://docs.databricks.com/aws/en/dashboards/embed) into custom web applications.
  - Developed web applications using [Streamlit](https://streamlit.io/) and deployed them on [Databricks Apps](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/).

# Architecture

![image](/assets/architecture.gif)
