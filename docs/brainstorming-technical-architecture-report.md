# Technical Architecture Brainstorming Report

**Date:** 2025-12-04
**Status:** Completed

## 1. Objective

The goal of this session was to define the core technical architecture for the "School Project Management" simulation, a 2-hour, single-user, server-hosted experience.

## 2. Final Recommended Architecture

This following technology stack was decided upon to provide a modern, robust, and maintainable foundation for the project.

*   **Model:** Server-Hosted Application (Model A)
*   **Architecture:** Monolithic Backend with a Single-Page Application (SPA) Frontend.
*   ---
*   **Backend:**
    *   **Language:** Python
    *   **Framework:** FastAPI
*   **Frontend:**
    *   **Language:** JavaScript
    *   **Framework:** React
*   **Database:**
    *   **Type:** SQLite (managed on the server)

## 3. Decision Process & Rationale

### 3.1. Application Model: Server-Hosted

Initially, we considered a fully client-side application (Model B) that would store data in the browser. However, to ensure data persistence, safety from browser cache clearing, and to provide a more robust experience, we opted for a **Server-Hosted model (Model A)**. The application logic and data will reside on a server, and the user will interact through a web browser.

### 3.2. Architecture: Monolithic

We compared a Monolithic architecture against Microservices. For the scope of this project (a self-contained simulation), a **Monolithic architecture** was chosen to prioritize simplicity and speed of initial development.

### 3.3. Data Storage: SQLite

We discussed storing data in flat JSON files versus a database. To ensure transactional integrity (preventing save-file corruption), performance, and the ability to query data efficiently, a database was chosen. **SQLite** was selected as the ideal solution, as it provides the full power of a SQL database within a single file on the server, requiring no separate database server.

### 34. Backend Technology: Python & FastAPI

An investigation of the repository revealed an existing use of **Python** for utility scripts. To maintain consistency, Python was confirmed as the backend language.

The existing `server.py` was found to be a simple utility server. For the main application, a full-featured framework was deemed necessary. **FastAPI** was recommended for its high performance, ease of use, and automatic API documentation features.

### 3.5. Frontend Technology: React

For the frontend, we compared a traditional Server-Side Rendered (SSR) approach with a modern Single-Page Application (SPA). For a fluid and interactive simulation, the **SPA** approach was selected.

**React** was recommended as the framework of choice due to its vast ecosystem, extensive community support, and component-based architecture, which is ideal for building a complex simulation interface.
