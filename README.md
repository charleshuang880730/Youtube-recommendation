### **YouTube Highlight Extraction & Recommendation Web App**  

This project is a backend system for extracting highlights and recommending key moments from YouTube videos based on subtitles and user comments. The system integrates natural language processing (NLP) and deep learning techniques to analyze and extract meaningful segments.  

### **Features**
- **Search & Recommendation APIs**: Built with Django and Django REST Framework to provide text-based search and recommendation.  
- **Whoosh Indexing**: Implements Whoosh for efficient text-based search across video subtitles and comments.  
- **Graph Neural Network (GNN)**: Utilizes Word2Vec embeddings and a GNN-based approach to refine recommendations.  
- **RESTful API Integration**: Custom APIs for querying and retrieving highlights from videos.  

---

## **🔧 Installation & Setup**
### **1. Clone the repository**

### **2. Install dependencies**
Make sure you have Python installed, then install the required packages:
```bash
pip install -r requirements.txt
```

### **3. Start the Django server**
```bash
python manage.py runserver
```
The server will start at `http://127.0.0.1:8000/path`.

---

## **📡 API Endpoints**
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/sendall?queryname=` | Search for video highlights based on query keywords |
| `GET` | `/sendpop?popularity=` | Retrieve popular video segments |
| `GET` | `/sendkey?keyword=` | Search for video comments related to a specific keyword |

---

### **📌 Notes**
- Ensure that the dataset and Whoosh index files are properly set up before running the API.
- The API server is designed for text-based search and highlight extraction.
- Future improvements may include switching from Whoosh to a database-based search system.
