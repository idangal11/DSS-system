# 🧠 Clinical Decision Support System (CDSS)

## 📘 Overview
This project was developed as part of the **"Temporal Reasoning and Knowledge-Based Systems in Medical Informatics"** course at **Ben-Gurion University of the Negev**.  
The goal was to design and implement a **Clinical Decision Support System (CDSS)** capable of performing **context-sensitive temporal reasoning** for simulated medical data, based on a structured knowledge base.

---

## 🏗️ System Architecture
The system is composed of the following main components:

1. **Knowledge Base (KB)**  
   Contains medical concepts and relationships derived from a clinical treatment protocol.  
   The ontology defines patient *states* (e.g., *Hemoglobin-state*, *Hematological-state*, *Systemic-toxicity*) and links them to clinical recommendations.

2. **Database (DB)**  
   Stores patient data — simulated measurements for 10 patients (5 males, 5 females).  
   Includes values such as *Hemoglobin-level*, *WBC-level*, *Systemic Toxicity Grade*, and timestamps.

3. **Inference Engine (DSS Engine)**  
   Performs reasoning over the data and knowledge base.  
   Supports:
   - **Retrieval queries** (e.g., get patient measurement at a given time)
   - **Historical queries**
   - **Insert / Update / Delete operations**
   - **Temporal reasoning** — determining intervals where patients were in a certain state
   - **Recommendation generation** based on current medical state

4. **User Interface (UI)**  
   Provides a simple interface for:
   - Querying the database and patient states  
   - Visualizing temporal changes in states  
   - Displaying recommendations based on patient condition

---

## 🧩 Key Functionalities

### 🔍 Query Examples
- **Retrieve value**  
  > “What was *WBC* for patient *Jacob Cohen* on May 18, 2016, at 8:00?”

- **Retrieve historical values**  
  > “Show *WBC* history for patient *Jacob Cohen* between May 18–21, 2016.”

- **Insert or update data**  
  > “Update *WBC* value for *Jacob Cohen* on May 24, 2016, at 10:00 to 8000.”

- **Delete record**  
  > “Delete latest *Arterial PaCO2* measurement for patient *Jack Spoon* on May 17, 2016.”

- **State queries**  
  > “When was *Jacob Cohen* in a *Mild Anemia* state?”

---

## 🩸 Knowledge Representation

### Example — Hemoglobin Classification Tables

| Gender | Hemoglobin Level (mg/100cc) | Hemoglobin State |
|:--------|:------------------------------|:------------------|
| Male | 0–9 | Severe Anemia |
| Male | 9–11 | Moderate Anemia |
| Male | 11–13 | Mild Anemia |
| Male | 13–16 | Normal Hemoglobin |
| Male | 16+ | Polyhemia |

The system also supports 2D classifications, combining *Hemoglobin* and *WBC* levels to derive *Hematological-states*.

---

## 💊 Treatment Recommendation Engine

Based on combinations of:
- **Gender**
- **Hemoglobin-state**
- **Hematological-state**
- **Systemic Toxicity (Grade I–IV)**

The system outputs recommendations such as:
- Blood pressure monitoring frequency  
- Medication dosage (e.g., Aspirin, Magnesium)  
- Exercise or diet consultations  
- Emergency alerts

---

## 🧮 Technologies Used
- **Python**  
- **SQLite / Excel (for DB simulation)**  
- **Pandas, NumPy**  
- **Custom Ontology Representation**

---

## 🏫 Course Details
**Course:** Temporal Reasoning and Knowledge-Based Systems in Medical Informatics  
**University:** Ben-Gurion University of the Negev  
**Project Type:** Mini-Project – CDSS Development  
**Instructor:** Prof. Yuval Shahar  

---

## ✍️ Author
**Idan Gal**  
M.Sc. in Software & Information Systems Engineering  
AI & Medical Informatics Researcher  
📍 Ben-Gurion University of the Negev  

---

## 📄 License
This project was developed for academic and educational purposes only.  
All patient data is simulated and does not represent real individuals.
