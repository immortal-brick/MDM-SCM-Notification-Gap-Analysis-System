# MDM–SCM Notification Gap Analysis System

## Overview
This project is an automated solution to identify notification delivery gaps between the **Meter Data Management (MDM)** system and the **Short Communication Manager (SCM)** system.  
It replaces manual reconciliation of large reports with a structured, rule-based and scalable approach.

The application allows users to upload required reports through a simple web interface and generates a consolidated gap analysis report automatically.

---

## Problem Statement
MDM notifications and SCM delivery records are generated as separate reports with no automated mechanism to verify whether each critical notification has been successfully delivered.  
Manual comparison of these reports is time-consuming, error-prone, and difficult to scale for large consumer datasets.

---

## Solution
An automated **MDM–SCM Notification Gap Analysis** system was developed using Python and Flask.  
The solution applies predefined mapping rules, removes duplicate records, performs consumer-level reconciliation, and generates a final report highlighting notification gaps.

---

## Key Features
- Web-based interface for uploading multiple reports
- Automated data ingestion and processing
- Filtering and deduplication of notifications
- Rule-based mapping between MDM notifications and SCM message types
- Consumer-level gap identification
- Consolidated final report generation
- Progress indicator for better user experience

---

## Impact
- Manual reconciliation time reduced from **~1 hour to under 5 minutes**
- **~90% reduction** in processing time
- Improved accuracy and consistency
- Reduced dependency on manual effort
- Enhanced audit and compliance readiness

---

## Tech Stack
- **Backend:** Python, Flask
- **Data Processing:** Pandas
- **Frontend:** HTML, CSS
- **Output:** Excel (XLSX)

---

## How to Run the Project

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/mdm-scm-notification-gap-analysis.git
cd mdm-scm-notification-gap-analysis

