from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pandas as pd  # Required for reading Excel
import os

app = FastAPI()

# ------------------------------
# CONFIGURATION
# ------------------------------
EXCEL_FILE_PATH = os.path.join(os.path.dirname(__file__), "question_bank.xlsx")

# ------------------------------
# Utility function to fetch questions + answers
# ------------------------------
def get_questions(file_path, grade, category, n=3):
    try:
        df = pd.read_excel(file_path, sheet_name="Questions")
        filtered = df[(df["Grade"] == grade) & (df["Category"] == category)]
        if len(filtered) < n:
            sample = filtered
        else:
            sample = filtered.sample(n)
        return sample[["Question", "Answer"]].to_dict(orient="records")
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return []

def get_sample_questions(file_path, grade):
    try:
        df = pd.read_excel(file_path, sheet_name="Questions")
        df = df[df["Grade"] == grade]
        result = []
        rules = {3: 3, 4: 2, 5: 1}
        for marks, count in rules.items():
            subset = df[df["Marks"] == marks]
            sample = subset.sample(count) if len(subset) >= count else subset
            result.extend(sample[["Question", "Answer", "Marks"]].to_dict(orient="records"))
        return result
    except Exception as e:
        print(f"Error: {e}")
        return []

# ------------------------------
# Home page route
# ------------------------------
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>StudyPointPro</title>
            <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
            <style>
                body { font-family: 'Poppins', sans-serif; margin: 0; padding: 0; background-color: #f2f4f6; color: #2c3e50; text-align: center; }
                header { background: linear-gradient(135deg, #4b6cb7, #182848); color: white; padding: 60px 20px; }
                header h1 { font-size: 2.5rem; margin: 0; }
                header p { font-size: 1.2rem; margin-top: 10px; }
                .section { max-width: 900px; margin: 40px auto; padding: 20px; background: #ffffff; border-radius: 12px; box-shadow: 0 3px 8px rgba(0,0,0,0.08); text-align: left; }
                .section h2 { text-align: center; color: #3b4a6b; margin-bottom: 20px; }
                ul { list-style-type: none; padding: 0; }
                ul li { margin: 8px 0; padding-left: 10px; }
                .button { display: inline-block; margin-top: 20px; padding: 12px 24px; background-color: #4b6cb7; color: white; font-weight: 600; border-radius: 8px; text-decoration: none; transition: background 0.3s ease; }
                .button:hover { background-color: #3b4a6b; }
                .testimonial { font-style: italic; margin: 15px 0; padding: 10px 20px; border-left: 4px solid #4b6cb7; background: #eaf0f6; border-radius: 8px; }
                .video-links a { display: block; margin: 6px 0; text-decoration: none; color: #4b6cb7; font-weight: 500; }
                footer { background: #1f2a38; color: white; padding: 20px; margin-top: 40px; }
                table { width: 100%; border-collapse: collapse; margin-top:10px; color:#2c3e50; }
                th { background:#4b6cb7; color:white; padding:8px; border:1px solid #999; }
                td { padding:8px; border:1px solid #999; text-align:left; }
                tr:nth-child(even) { background: #f0f2f5; }
                tr:nth-child(odd) { background: #e6ebf0; }
                .answer-btn { background:#4b6cb7; color:white; border:none; padding:4px 8px; border-radius:4px; cursor:pointer; }
                .answer-btn:hover { background:#3b4a6b; }
            </style>
        </head>
        <body>
            <header>
                <h1>Welcome to StudyPointPro</h1>
                <p>Your trusted hub for academic and competition math learning</p>
            </header>

            <section class="section">
                <h2>Math Courses Offered</h2>
                <ul>
                    <li><strong>Academic Math Classes</strong> – Grades 1–8</li>
                    <li><strong>Competition-Focused Classes:</strong>
                        <ul>
                            <li>Math Kangaroo (Elementary, Middle School)</li>
                            <li>TMSCA Math (Elementary, Middle School)</li>
                            <li>TMSCA Number Sense (Elementary, Middle School)</li>
                        </ul>
                    </li>
                    <li><strong>High School Classes:</strong>
                        <ul>
                            <li>Algebra 1</li>
                            <li>Geometry</li>
                        </ul>
                    </li>
                </ul>
                <a href="https://tinyurl.com/yc5vb7y5" target="_blank" class="button">Sign Up / Contact</a>
            </section>

            <section class="section">
                <h2>What Our Students Say</h2>
                <div class="testimonial">“StudyPointPro helped me gain confidence in math competitions!”</div>
                <div class="testimonial">“The classes are simple, clear, and very effective.”</div>
                <div class="testimonial">“Highly recommend for anyone preparing for Math Kangaroo or TMSCA.”</div>
            </section>

            <section class="section">
                <h2>Math Competition Resources</h2>
                <div class="video-links">
                    <h3 style="color:black;">Math Kangaroo</h3>
                    <a href="https://www.youtube.com/watch?v=sample1" target="_blank" style="display:block; margin-bottom:5px;">Math Kangaroo Sample Video 1</a>
                    <a href="https://www.youtube.com/watch?v=sample2" target="_blank" style="display:block; margin-bottom:10px;">Math Kangaroo Sample Video 2</a>

                    <div style="margin-top: 15px;">
                        <a href="#" onclick="document.getElementById('sample-form').style.display='block'; return false;" class="button" style="color:white;">
                            Try Sample Questions from Previous Papers
                        </a>
                    </div>

                    <div id="sample-form" style="display:none; margin-top:20px; text-align:left;">
                        <div style="display:flex; align-items:center; margin-bottom:10px;">
                            <label style="width:150px; color:black;">Select Grade:</label>
                            <div style="flex:1;">
                                <div>
                                    <label><input type="radio" name="grade" value="1"> 1</label>
                                    <label><input type="radio" name="grade" value="2"> 2</label>
                                    <label><input type="radio" name="grade" value="3"> 3</label>
                                    <label><input type="radio" name="grade" value="4"> 4</label>
                                    <label><input type="radio" name="grade" value="5"> 5</label>
                                    <label><input type="radio" name="grade" value="6"> 6</label>
                                </div>
                                <div style="margin-top:5px;">
                                    <label><input type="radio" name="grade" value="7"> 7</label>
                                    <label><input type="radio" name="grade" value="8"> 8</label>
                                    <label><input type="radio" name="grade" value="9"> 9</label>
                                    <label><input type="radio" name="grade" value="10"> 10</label>
                                    <label><input type="radio" name="grade" value="11"> 11</label>
                                    <label><input type="radio" name="grade" value="12"> 12</label>
                                </div>
                            </div>
                        </div>

                        <div style="display:flex; align-items:center; margin-bottom:10px;">
                            <label style="width:150px; color:black;">Select Question Type:</label>
                            <div style="flex:1; color:black;">
                                <label><input type="radio" name="marks" value="3"> 3-mark questions</label>
                                <label><input type="radio" name="marks" value="4"> 4-mark questions</label>
                                <label><input type="radio" name="marks" value="5"> 5-mark questions</label>
                            </div>
                        </div>

                        <button onclick="fetchSampleQuestions()" class="button">Get Questions</button>
                    </div>

                    <div id="questions-result" style="margin-top:20px; color:#2c3e50;"></div>

                    <script>
                        function fetchSampleQuestions() {
                            let grade = document.querySelector('input[name="grade"]:checked')?.value;
                            let marks = document.querySelector('input[name="marks"]:checked')?.value;
                            if (!grade || !marks) { alert("Please select both grade and question type!"); return; }
                            fetch(`/sample/${grade}`)
                                .then(response => response.json())
                                .then(data => {
                                    if (data.error) { document.getElementById("questions-result").innerHTML = `<p style="color:red;">${data.error}</p>`; return; }
                                    let filtered = data.questions.filter(q => q.Marks == marks);
                                    if (filtered.length === 0) { document.getElementById("questions-result").innerHTML = "<p style='color:#555;'>No questions found.</p>"; return; }
                                    let html = `<table style="width:100%; border-collapse: collapse; margin-top:10px; color:#2c3e50;">
                                        <thead>
                                            <tr style="background:#8fa4c0; color:white;">
                                                <th style="padding:8px; border:1px solid #999;">Question</th>
                                                <th style="padding:8px; border:1px solid #999;">
                                                    Answer 
                                                    <button onclick="showAllAnswers()" style="margin-left:10px; background:#7ea1c9; color:white; border:none; padding:4px 8px; border-radius:4px;">Show All Answers</button>
                                                </th>
                                            </tr>
                                        </thead>
                                        <tbody>`;
                                    filtered.forEach((q,index)=> {
                                        let rowColor = index%2===0 ? '#f0f2f5' : '#e6ebf0';
                                        html += `<tr style="background:${rowColor};">
                                            <td style="padding:8px; border:1px solid #999;">${q.Question}</td>
                                            <td id="answer-${index}" style="padding:8px; border:1px solid #999;">
                                                <button id="btn-${index}" data-answer="${q.Answer}" onclick="showAnswer(${index})" class="answer-btn">Show Answer</button>
                                            </td>
                                        </tr>`;
                                    });
                                    html += `</tbody></table>`;
                                    document.getElementById("questions-result").innerHTML = html;
                                });
                        }

                        function showAnswer(index) {
                            let cell = document.getElementById(`answer-${index}`);
                            let btn = document.getElementById(`btn-${index}`);
                            if (btn) { cell.innerHTML = btn.getAttribute("data-answer"); }
                        }

                        function showAllAnswers() {
                            document.querySelectorAll("[id^='answer-']").forEach(cell => {
                                let btn = cell.querySelector("button");
                                if (btn) { cell.innerHTML = btn.getAttribute("data-answer"); }
                            });
                        }
                    </script>
                </div>
            </section>

            <section class="section">
                <h2>About & Contact</h2>
                <p>At StudyPointPro, we believe in building strong foundations in mathematics while preparing students for academic success and competitions.</p>
                <a href="https://tinyurl.com/yc5vb7y5" target="_blank" class="button">Get in Touch</a>
            </section>

            <footer>
                <p>&copy; 2025 StudyPointPro. All rights reserved.</p>
            </footer>
        </body>
    </html>
    """

@app.get("/questions/{grade}/{category}")
def fetch_questions(grade: int, category: str, n: int = 3):
    questions = get_questions(EXCEL_FILE_PATH, grade=grade, category=category, n=n)
    if not questions:
        return {"error": "No questions found or Excel file missing."}
    return {"questions": questions}

@app.get("/sample/{grade}")
def sample_questions(grade: int):
    questions = get_sample_questions(EXCEL_FILE_PATH, grade)
    if not questions:
        return {"error": "No questions found for this grade."}
    return {"questions": questions}
