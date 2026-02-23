# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Streamlit-based e-learning application for the INFOGEST Protocol, which teaches users about the standardized in vitro digestion method. The app provides educational content, interactive calculations, a quiz system, and protocol guidance for food digestion research.

## Running the Application

**Start the Streamlit app:**
```bash
streamlit run main.py
```

The application will be available at http://localhost:8501

## Dependencies

Install dependencies with:
```bash
pip install -r requirements.txt
```

Key dependencies:
- `streamlit==1.42.2` - Main web framework
- `streamlit-extras==0.5.5` - Additional Streamlit components
- `streamlit-pdf-viewer==0.0.21` - PDF viewing functionality
- `streamlit_autorefresh` - Auto-refresh for timer functionality
- `fpdf2==2.8.2` - PDF generation
- `pandas~=2.2.3` - Data manipulation for calculations
- `lucide` - Icon library

## Architecture

### Main Entry Point
- `main.py` - Configures the multi-page Streamlit navigation with organized sections:
  - **Get Started**: Introduction and fundamentals
  - **INFOGEST Protocol**: Step-by-step protocol guidance
  - **Evaluation**: Interactive quiz
  - **Tools**: Dashboard, file downloads, changelog

### Page Structure
All pages are located in `pages/` directory:

- `introduction.py` - Welcome page with project overview and INFOGEST background
- `fundamentals.py` - Core concepts and theory
- `first_steps.py` - Initial protocol steps
- `solution_prep.py` - Stock solution preparation guidance
- `sdf_prep.py` - Simulated digestive fluids preparation
- `quick_start.py` - Quick reference protocol guide
- `quiz.py` - Interactive quiz system using `utils/assets/quiz_data.json`
- `dashboard.py` - Interactive calculation tools with timer functionality
- `files.py` - File download resources
- `changelog.py` - Application updates and version history

### Key Features in dashboard.py

**Timer System:**
- Session state management for timer functionality
- Auto-refresh mechanism using `streamlit_autorefresh`
- Audio alerts with `utils/assets/Sencha.mp3`
- Pause/resume/reset controls with preset durations (2 min, 120 min)

**pH Adjustment Calculator:**
- Interactive dataframes for pH adjustment calculations
- Real-time calculations for acid/base volumes needed
- Multiple phase tracking (oral, gastric, intestinal)
- Dynamic recalculation based on food quantity changes

**HTML Integration:**
- Embeds custom HTML and Javascript content from `utils/infogest/index.html`
- CSS styling from `utils/infogest/design.css`
- Custom calculation interface within Streamlit tabs
- Modern 

### Assets and Resources
Located in `utils/assets/`:
- `quiz_data.json` - Comprehensive quiz questions with multiple question types
- `*.json` files for SDF concentration and volume data
- PDF protocols and reference materials
- Audio files for timer alerts
- Images for branding and educational content

### Data Structure
The quiz system supports multiple question types:
- `multiple-choice` - Single correct answer
- `multiple-select` - Multiple correct answers
- `numeric` - Numerical answers with tolerance

### Session State Management
Critical session state variables in dashboard.py:
- Timer states: `timer_running`, `remaining`, `alarm_active`, `paused`
- pH calculation data: `phdf` (dictionary of DataFrames), `sample_number`, `food`
- Volume calculations: `finalVolGastricPhase`

## Development Notes

- The app uses Streamlit's native navigation system (`st.navigation`)
- Heavy use of session state for maintaining data across interactions
- Custom CSS injection for styling and animations
- Component reusability through consistent page structure patterns
- No testing framework or linting configuration detected

## Claude Code Agent Usage Guidelines

When working on this project, leverage specialized agents for optimal results:

### 🐍 **Python Development**
- **Use `python-pro` agent** for:
  - Streamlit app enhancements and optimization
  - Data processing improvements in dashboard calculations
  - Quiz system logic and session state management
  - PDF generation and file handling features

### 🎨 **UI/UX Development**
- **Use `frontend-developer` agent** for:
  - Streamlit component development and layout improvements
  - Interactive dashboard enhancements
  - Responsive design for mobile/tablet users
  
- **Use `ui-designer` agent** for:
  - Visual design improvements and user interface enhancements
  - Color schemes, typography, and visual hierarchy
  - Component styling and branding consistency

- **Use `whimsy-injector` agent** PROACTIVELY after UI changes for:
  - Adding delightful interactions to quiz feedback
  - Enhancing timer alerts and notifications
  - Creating engaging loading states and transitions
  - Making error messages more user-friendly and memorable

### 🔬 **Scientific/Educational Content**
- **Use `ux-researcher` agent** for:
  - Analyzing quiz effectiveness and learning outcomes
  - User journey mapping for the protocol learning path
  - Educational flow optimization

- **Use `visual-storyteller` agent** for:
  - Creating infographics for protocol steps
  - Data visualization improvements in dashboards
  - Educational diagram creation and enhancement

### 🛠 **Technical Maintenance**
- **Use `debugger` agent** for:
  - Timer functionality issues
  - Session state problems
  - Calculation accuracy debugging
  - Browser compatibility issues

- **Use `code-reviewer` agent** for:
  - Code quality assessment before major releases
  - Security review of file upload/download features
  - Performance optimization recommendations

- **Use `error-detective` agent** for:
  - Analyzing user interaction logs
  - Investigating calculation discrepancies
  - Tracking down intermittent bugs

### 📊 **Data and Calculations**
- **Use `general-purpose` agent** for:
  - Complex enzyme calculation logic research
  - Scientific protocol research and validation
  - Multi-step mathematical validation tasks

### 🎯 **Specific Use Cases**

**Quiz Enhancement Project:**
```
1. Use ux-researcher to analyze current quiz effectiveness
2. Use ui-designer for new question type designs
3. Use python-pro for implementation
4. Use whimsy-injector for delightful feedback animations
5. Use code-reviewer for final quality assessment
```

**Dashboard Calculation Updates:**
```
1. Use python-pro for calculation logic improvements
2. Use frontend-developer for UI component updates
3. Use debugger for accuracy validation
4. Use whimsy-injector for enhanced user interactions
```

**Educational Content Overhaul:**
```
1. Use ux-researcher for learning path analysis
2. Use visual-storyteller for diagram and infographic creation
3. Use ui-designer for content presentation improvements
4. Use whimsy-injector for engaging micro-interactions
```

### 🚀 **Proactive Agent Usage**
- **Always use `whimsy-injector`** after any UI/UX changes to ensure delightful user experiences
- **Always use `code-reviewer`** after significant feature implementations
- **Always use `python-pro`** for Python optimization opportunities
- **Always use `frontend-developer`** for Streamlit component development