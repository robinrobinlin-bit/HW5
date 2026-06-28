# Implementation Plan: 10 ML Algorithms Dynamic Learning Web App with AI Assistant

This plan outlines the updates to include an **AI Chat Assistant** in the local Next.js + FastAPI machine learning platform.

---

## 🏛️ Updated Architecture

We will add a chat pipeline to the existing structure:
1. **FastAPI Backend**:
   - New endpoint `POST /api/chat` accepting a user message history and returning an AI response.
   - Dual engine:
     - **Gemini API Engine**: If a `GEMINI_API_KEY` environment variable is available, it queries Google's Gemini LLM to answer machine learning questions.
     - **Local Expert Engine**: Otherwise, it uses a local semantic keyword matching database to provide expert answers about the 10 machine learning algorithms, equations, and hyperparameter tuning offline.
2. **Next.js Frontend**:
   - Add a floating, expandable chat widget (bottom-right corner) available globally across all pages.
   - Beautifully styled using CSS glassmorphism, slide-in animations, user vs. bot chat bubbles, and a typewriter typing state.

---

## 📋 User Review Required

> [!IMPORTANT]
> - **API Keys**: No API key is required to start! The local engine provides instant, highly detailed expert answers on ML algorithms by default.
> - **Real LLM Option**: If you want to use the live Gemini LLM, set the `GEMINI_API_KEY` environment variable on your shell before running the FastAPI backend.

---

##  Proposed Changes

### 1. Backend (FastAPI)
#### [MODIFY] `backend/main.py`
- Add `POST /api/chat` route.
- Implement the local QA matching algorithm covering:
  - Definition, pros, cons, and equations for all 10 algorithms.
  - Hyperparameter tuning advice (e.g. C, gamma, max_depth, n_clusters).
  - Machine learning topics (Overfitting, underfitting, training/test splits, metrics).
- Implement the optional Google Gemini SDK caller.

---

### 2. Frontend (Next.js)
#### [NEW] `frontend/components/ChatWidget.js`
- Core UI component for the floating chat window:
  - Collapsed/expanded states.
  - Input field with Enter-to-send support.
  - Real-time messages stream (user and assistant messages).
  - Typing indicator animation.

#### [MODIFY] `frontend/pages/_app.js`
- Include the global `<ChatWidget />` component to render the assistant on all views.

#### [MODIFY] `frontend/styles/globals.css`
- Add styling classes for the chat widget:
  - Floating action button (FAB).
  - Message bubble colors (Accent for user, Primary/Slate for AI).
  - Expand/collapse animations.
  - Typing loader dots.

---

## 🛠️ Verification Plan

### Automated Verification
- Backend connection: Post a test chat query to `http://localhost:8000/api/chat` using PowerShell to check response output.

### Manual Verification
- Open `http://localhost:3000`.
- Expand the AI assistant widget.
- Ask questions (e.g., "什麼是 SVM?", "隨機森林有什麼缺點?", "如何調整 K-Means 的 K 值?").
- Verify that responses are shown clearly in Traditional Chinese.
