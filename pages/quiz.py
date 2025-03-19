import streamlit as st
import json
import io
from fpdf import FPDF
from datetime import datetime
import math

st.set_page_config(
    layout="centered"
)

# Function to load quiz data from a JSON file
def load_quiz_data(json_file):
    try:
        with open(json_file, "r") as f:
            data = json.load(f)
        return data
    except Exception as e:
        st.error(f"Error loading quiz data: {e}")
        return []

# Load quiz data from the JSON file
quiz_data = load_quiz_data("utils/assets/quiz_data.json")

# Set page title
st.title("🤯 INFOGEST Protocol Quiz")
st.write("""
Before applying the INFOGEST protocol in practice, it's essential to ensure you fully understand its steps and principles. 
This quiz will test your knowledge and confirm that you have carefully reviewed the protocol.

At the end of the quiz, you will receive a certificate of completion, which you must submit to your supervisor as proof of your proficiency.
""")

# Ask for the user's name to personalize the certificate
user_name = st.text_input("**Enter your name:**", "")

main_placeholder = st.expander("Questions", expanded=True)
result_placeholder = st.container(border=True)

with main_placeholder:

    # Create a dictionary to store user answers in session state if not already present
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}

    # Create a list to store placeholders for feedback so they appear below each question.
    feedback_placeholders = []
    st.markdown("### Quiz Questions")

    # Initialize an attempt counter if it doesn't exist yet
    if "attempt_counter" not in st.session_state:
        st.session_state.attempt_counter = 0

    # Loop through quiz questions and create a feedback placeholder for each
    for idx, item in enumerate(quiz_data):
        st.markdown(f"**Question {idx + 1}:** {item['question']}")

        # Check if the question is numeric or multiple-choice
        if item.get("type") == "numeric":
            st.session_state.user_answers[idx] = st.number_input("Enter your answer:", key=f"q{idx}")
        elif item.get("type") == "text":
            st.session_state.user_answers[idx] = st.text_input("Enter your answer:", key=f"q{idx}")
        elif item.get("type") == "multiple-select":
            st.session_state.user_answers[idx] = st.multiselect("Select answers:", item["options"], key=f"q{idx}")

        else:
            st.session_state.user_answers[idx] = st.radio("Select one:", item["options"], key=f"q{idx}")

        # Create a placeholder to later display the feedback below the question
        placeholder = st.empty()
        feedback_placeholders.append(placeholder)

        if item.get("type") == "multiple-select":
            if len(item["options"]) == len(item["answer"]):
                if not (len(st.session_state.user_answers[idx]) == len(item["answer"])):
                    feedback_placeholders[idx].error("All the options must be selected.")

            else:
                if (len(st.session_state.user_answers[idx]) < 1):
                    feedback_placeholders[idx].error("At least 1 option must be selected.")


# Button to submit the quiz
if st.button("Submit Quiz"):
    if user_name.strip() == "":
        st.error("Please enter your name to register your quiz results!")
    else:
        # Increment the attempt counter on each submission
        st.session_state.attempt_counter += 1

        score = 0

        # Evaluate answers and update the corresponding feedback placeholders
        for idx, item in enumerate(quiz_data):
            user_answer = st.session_state.user_answers[idx]
            # For numeric questions, check within a tolerance value
            if item.get("type") == "numeric":
                correct_value = item["answer"]
                tolerance = item.get("tolerance", 0.0)
                if abs(user_answer - correct_value) <= tolerance:
                    score += 1
                    feedback_placeholders[idx].success("Correct answer")
                else:
                    feedback_placeholders[idx].info(f"**Explanation:** {item['explanation']}")
            else:
                correct_answer = item["answer"]
                if user_answer == correct_answer:
                    score += 1
                    feedback_placeholders[idx].success("Correct answer")
                else:
                    feedback_placeholders[idx].info(f"**Explanation:** {item['explanation']}")

        # Calculate grade as a percentage
        total_questions = len(quiz_data)
        grade = (score / total_questions) * 100

        # Update the result block at the top of the page with the attempt count
        result_placeholder.write(f"**{user_name}**, you scored **{score} out of {total_questions}**.")
        result_placeholder.write(f"Your grade is **{grade:.2f}%**.")
        result_placeholder.write(f"You have attempted the quiz **{st.session_state.attempt_counter} time(s)**.")

        # Define a passing grade threshold (e.g., 80%)
        passing_grade = 80

        # Check if the user passed
        if grade >= passing_grade:
            st.balloons()
            result_placeholder.success(
                f"Congratulations! You passed the INFOGEST quiz after {st.session_state.attempt_counter} attempt(s)!")


            # Define a custom PDF class with a drawn abstract background.
            class PDF(FPDF):
                def draw_star_golden_seal(self, cx, cy, size):
                    """
                    Draw a star-like golden seal composed of 8 squares rotated by 45° increments.
                    :param cx: center x-coordinate of the seal.
                    :param cy: center y-coordinate of the seal.
                    :param size: overall "bounding box" size for centering text.
                    """
                    # Define the side length of each square.
                    s = size * 0.6  # adjust factor as needed for visual appeal

                    # Set shiny gold for fill.
                    self.set_fill_color(255, 215, 0)  # Shiny gold
                    # Draw each of the 8 squares.
                    for i in range(8):
                        angle = math.radians(i * 11.25)
                        vertices = []
                        # Define square corners relative to center.
                        for dx, dy in [(-s / 2, -s / 2), (s / 2, -s / 2), (s / 2, s / 2), (-s / 2, s / 2)]:
                            # Rotate the corner around the origin.
                            rx = dx * math.cos(angle) - dy * math.sin(angle)
                            ry = dx * math.sin(angle) + dy * math.cos(angle)
                            vertices.append((cx + rx, cy + ry))
                        self.polygon(vertices, style="F")

                    # Draw outlines in darker gold.
                    self.set_line_width(1)
                    self.set_draw_color(218, 165, 32)  # Goldenrod
                    for i in range(8):
                        angle = math.radians(i * 11.25)
                        vertices = []
                        for dx, dy in [(-s / 2, -s / 2), (s / 2, -s / 2), (s / 2, s / 2), (-s / 2, s / 2)]:
                            rx = dx * math.cos(angle) - dy * math.sin(angle)
                            ry = dx * math.sin(angle) + dy * math.cos(angle)
                            vertices.append((cx + rx, cy + ry))
                        self.polygon(vertices, style="D")

                    # Place centered text within the seal.
                    # Reset position to top-left of a square bounding box that is size x size.
                    self.set_xy(cx - size / 2, cy - size / 2)
                    self.set_font("Helvetica", "B", 8)
                    self.set_text_color(255, 255, 255)
                    self.cell(size, size, "CERTIFIED", border=0, align="C")

                def header(self):
                    # Fill entire page with a light Alice Blue background.
                    self.set_fill_color(255, 255, 255)
                    self.rect(0, 0, self.w, self.h, 'F')

                    # Optionally, draw additional abstract horizontal lines.
                    self.set_line_width(0.8)
                    self.set_draw_color(200, 200, 255)
                    self.line(0, self.h * 0.3, self.w, self.h * 0.3)
                    self.line(0, self.h * 0.8, self.w, self.h * 0.8)

                    # Draw two star-like golden seals in the header.
                    self.draw_star_golden_seal(30, 30, 40)  # Top left seal.
                    self.draw_star_golden_seal(self.w - 30, 30, 40)  # Top right seal.

                    # Reset X position to left margin before drawing the title.
                    self.set_x(self.l_margin)
                    self.set_font("Helvetica", "B", 24)
                    self.set_text_color(0, 70, 140)
                    self.cell(0, 15, "Certificate of Achievement", ln=True, align="C")
                    self.ln(10)

                def footer(self):
                    # Position footer 15 mm from the bottom.
                    self.set_y(-25)
                    self.set_font("Helvetica", "I", 8)
                    self.set_text_color(128, 128, 128)
                    self.multi_cell(0, 8,"Issued by the SFP group, A. Mathys\nINFOGEST Protocol Quiz", align="C")

            pdf = PDF("L", "mm", "A4")
            pdf.add_page()

            # Set auto page break with a margin to avoid footer overlapping content.
            pdf.set_auto_page_break(auto=True, margin=25)

            # Certificate Title
            pdf.set_font("Helvetica", "B", 20)
            pdf.set_text_color(0, 70, 140)
            pdf.cell(0, 20, "From the Algae and Plant Nutrition and Health Team (SFP) and ETH Zurich", ln=True,
                     align="C")
            pdf.ln(10)

            # Certificate Body Content
            pdf.set_font("Helvetica", "", 16)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(0, 10, "This certifies that", align="C")
            pdf.ln(5)
            pdf.set_font("Helvetica", "B", 22)
            pdf.cell(0, 15, user_name, ln=True, align="C")
            pdf.ln(5)
            pdf.set_font("Helvetica", "", 16)
            pdf.multi_cell(0, 10, "has successfully passed the INFOGEST Protocol Quiz", align="C")
            pdf.ln(5)
            pdf.multi_cell(0, 10, f"with a grade of {grade:.2f}%.", align="C")
            pdf.ln(10)
            pdf.set_font("Helvetica", "I", 16)
            pdf.multi_cell(0, 10,
                           f"Congratulations on your achievement!\nYou passed the test after {st.session_state.attempt_counter} attempt(s).",
                           align="C")
            pdf.ln(30)  # Extra space so footer doesn't overlap the content.

            # Get the PDF output as a string, encode, and wrap in a BytesIO buffer.
            pdf_string = pdf.output(dest="S")
            pdf_buffer = io.BytesIO(pdf_string)

            # Display the download button.
            result_placeholder.markdown("### Download Your Certificate of Achievement")
            result_placeholder.download_button(
                label="Download Certificate",
                data=pdf_buffer,
                file_name=f"{user_name}_certificate_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )
        else:
            result_placeholder.error(
                "Unfortunately, you did not pass the quiz. Please review the material and try again.")