// Teacher Agent Web Portal Orchestrator

class App {
  constructor() {
    this.profile = null;
    this.curriculum = [];
    this.customLessons = [];
    this.activeLesson = null;
    this.selectedGradeFilter = "JK";
    this.selectedFile = null;
    
    this.init();
  }

  async init() {
    this.setupEventListeners();
    await this.loadProfile();
    await this.loadCurriculum();
    await this.loadRecommendations();
    await this.loadPortfolio();
  }

  setupEventListeners() {
    // Nav Tabs
    document.querySelectorAll(".nav-tab-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const tab = btn.dataset.tab;
        this.switchTab(tab);
        window.soundManager.playPop();
      });
    });

    // Dropzone upload
    const dropzone = document.getElementById("dropzone");
    const fileInput = document.getElementById("worksheet-file-input");

    if (dropzone && fileInput) {
      dropzone.addEventListener("click", () => fileInput.click());

      dropzone.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropzone.classList.add("dragover");
      });

      dropzone.addEventListener("dragleave", () => {
        dropzone.classList.remove("dragover");
      });

      dropzone.addEventListener("drop", (e) => {
        e.preventDefault();
        dropzone.classList.remove("dragover");
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
          this.handleFileSelected(e.dataTransfer.files[0]);
        }
      });

      fileInput.addEventListener("change", (e) => {
        if (e.target.files && e.target.files[0]) {
          this.handleFileSelected(e.target.files[0]);
        }
      });
    }

    // Evaluate submit button
    const evalBtn = document.getElementById("btn-submit-eval");
    if (evalBtn) {
      evalBtn.addEventListener("click", () => this.submitEvaluation());
    }

    // Custom Generator form submit
    const genForm = document.getElementById("custom-gen-form");
    if (genForm) {
      genForm.addEventListener("submit", (e) => {
        e.preventDefault();
        this.submitCustomGeneration();
      });
    }

    // Profile Settings Form
    const profileForm = document.getElementById("profile-form");
    if (profileForm) {
      profileForm.addEventListener("submit", (e) => {
        e.preventDefault();
        this.saveProfileSettings();
      });
    }

    // Grade Switcher in Skills tab
    document.querySelectorAll(".grade-filter-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        document.querySelectorAll(".grade-filter-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        this.selectedGradeFilter = btn.dataset.grade;
        this.renderSkillsGrid();
        window.soundManager.playPop();
      });
    });
  }

  switchTab(tabId) {
    document.querySelectorAll(".nav-tab-btn").forEach(btn => {
      btn.classList.toggle("active", btn.dataset.tab === tabId);
    });

    document.querySelectorAll(".tab-view").forEach(view => {
      view.classList.toggle("active", view.id === `tab-${tabId}`);
    });

    // Stop speaking if switching tabs
    window.soundManager.stopSpeaking();
  }

  async loadProfile() {
    try {
      const res = await fetch("/api/profile");
      const data = await res.json();
      this.profile = data.profile;
      
      // Update UI badges
      document.getElementById("header-user-name").textContent = this.profile.name;
      document.getElementById("header-grade-tag").textContent = this.profile.grade;
      document.getElementById("header-star-count").textContent = this.profile.total_stars;
      document.getElementById("hero-child-name").textContent = this.profile.name;
      document.getElementById("hero-child-grade").textContent = this.profile.grade;
      document.getElementById("hero-star-count").textContent = this.profile.total_stars;
      document.getElementById("hero-completed-count").textContent = this.profile.worksheets_completed;
      document.getElementById("hero-streak-count").textContent = this.profile.streak_days;

      // Fill settings form
      if (document.getElementById("input-child-name")) {
        document.getElementById("input-child-name").value = this.profile.name;
        document.getElementById("input-child-grade").value = this.profile.grade;
        document.getElementById("input-child-age").value = this.profile.age;
      }
    } catch (e) {
      console.error("Failed to load profile", e);
    }
  }

  async loadCurriculum() {
    try {
      const res = await fetch("/api/curriculum");
      const data = await res.json();
      this.curriculum = data.nodes;
      this.renderSkillsGrid();
      this.populateLessonSelect();
    } catch (e) {
      console.error("Failed to load curriculum", e);
    }
  }

  renderSkillsGrid() {
    const grid = document.getElementById("skills-grid");
    if (!grid) return;

    let filtered = this.curriculum;
    if (this.selectedGradeFilter && this.selectedGradeFilter !== "ALL") {
      filtered = this.curriculum.filter(s => s.grade === this.selectedGradeFilter);
    }

    if (filtered.length === 0) {
      grid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 2rem;">No skills found for this grade.</div>`;
      return;
    }

    grid.innerHTML = filtered.map(skill => {
      let badgeClass = "badge-locked";
      let statusIcon = "🔒";
      let statusText = "Locked";

      if (skill.status === "mastered") {
        badgeClass = "badge-mastered";
        statusIcon = "⭐";
        statusText = "Mastered!";
      } else if (skill.status === "available") {
        badgeClass = "badge-available";
        statusIcon = "✨";
        statusText = "Ready to Learn";
      }

      return `
        <div class="skill-card status-${skill.status}">
          <div>
            <div class="skill-header">
              <span class="skill-icon">${skill.icon || "📚"}</span>
              <div>
                <h4 class="skill-title">${this.escapeHtml(skill.title)}</h4>
                <span class="tag tag-grade">${skill.grade}</span>
              </div>
            </div>
            <p class="skill-desc">${this.escapeHtml(skill.description)}</p>
          </div>
          <div class="skill-footer">
            <div class="status-badge ${badgeClass}">${statusIcon} ${statusText}</div>
            <button class="btn btn-secondary" style="padding: 0.35rem 0.75rem; font-size: 0.8rem;" onclick="app.previewAndPrintLesson('${skill.id}')">
              🖨️ Print Sheet
            </button>
          </div>
        </div>
      `;
    }).join("");
  }

  populateLessonSelect() {
    const select = document.getElementById("eval-lesson-select");
    if (!select) return;

    let customOptions = "";
    if (this.customLessons && this.customLessons.length > 0) {
      customOptions = `<optgroup label="✨ Custom Generated Worksheets">` +
        this.customLessons.map(c => `<option value="${c.id}">[Custom] ${this.escapeHtml(c.title)}</option>`).join("") +
        `</optgroup>`;
    }

    select.innerHTML = `<option value="">-- Choose Completed Worksheet --</option>` +
      customOptions +
      `<optgroup label="📚 Standard Curriculum">` +
      this.curriculum.map(s => `
        <option value="${s.id}">[${s.grade}] ${this.escapeHtml(s.title)}</option>
      `).join("") +
      `</optgroup>`;
  }

  async loadRecommendations() {
    try {
      const res = await fetch("/api/recommendations");
      const data = await res.json();
      const recs = data.recommendations || [];

      const container = document.getElementById("daily-rec-container");
      if (!container) return;

      if (recs.length === 0) {
        container.innerHTML = `<p style="color: var(--text-muted);">Explore the Skill Tree to pick a lesson!</p>`;
        return;
      }

      const primary = recs[0];
      container.innerHTML = `
        <div class="card recommendation-card">
          <div>
            <div class="rec-header">
              <div class="rec-icon">${primary.icon || "🌟"}</div>
              <div class="rec-details">
                <h3>${this.escapeHtml(primary.title)}</h3>
                <p>${this.escapeHtml(primary.description)}</p>
                <div class="rec-meta">
                  <span class="tag tag-grade">${primary.grade}</span>
                  <span class="tag tag-domain">${primary.domain}</span>
                  <span class="tag tag-reason">💡 ${this.escapeHtml(primary.reason)}</span>
                </div>
              </div>
            </div>
          </div>
          <div class="rec-actions">
            <button class="btn btn-primary btn-lg" onclick="app.previewAndPrintLesson('${primary.id}')">
              🖨️ Print Today's Worksheet
            </button>
            <button class="btn btn-secondary" onclick="app.switchTab('evaluate'); document.getElementById('eval-lesson-select').value='${primary.id}';">
              📸 Upload & Grade
            </button>
          </div>
        </div>
      `;
    } catch (e) {
      console.error("Failed to load recommendations", e);
    }
  }

  async previewAndPrintLesson(lessonId) {
    try {
      window.soundManager.playPop();
      const res = await fetch(`/api/lessons/${lessonId}`);
      if (!res.ok) throw new Error("Could not fetch lesson");
      const lesson = await res.json();
      this.activeLesson = lesson;

      // Render worksheet into preview modal or worksheet container
      const container = document.getElementById("worksheet-preview-area");
      container.innerHTML = window.worksheetRenderer.renderToHtml(lesson, this.profile ? this.profile.name : "Akira");

      // Switch to Worksheet Studio Tab
      this.switchTab("studio");

      // Scroll smoothly to preview
      container.scrollIntoView({ behavior: "smooth" });
    } catch (e) {
      alert("Error loading worksheet: " + e.message);
    }
  }

  printCurrent() {
    if (!this.activeLesson) {
      alert("Please select or generate a worksheet first before printing!");
      return;
    }
    this.switchTab("studio");
    window.soundManager.playPop();
    window.print();
  }

  async submitCustomGeneration() {
    const topic = document.getElementById("gen-topic").value;
    const domain = document.getElementById("gen-domain").value;
    const grade = document.getElementById("gen-grade").value;
    const customPrompt = document.getElementById("gen-prompt").value;

    const btn = document.getElementById("btn-generate-custom");
    const originalText = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = `<span>✨ Akira's Teacher is creating worksheet...</span>`;

    try {
      const res = await fetch("/api/lessons/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          grade: grade,
          domain: domain,
          topic: topic,
          child_name: this.profile ? this.profile.name : "Akira",
          custom_prompt: customPrompt
        })
      });

      if (!res.ok) throw new Error("Server could not generate lesson. Please try again.");
      const lesson = await res.json();
      this.activeLesson = lesson;

      // Track in customLessons list and update evaluate dropdown
      if (!this.customLessons) this.customLessons = [];
      const existingIdx = this.customLessons.findIndex(l => l.id === lesson.id);
      if (existingIdx >= 0) {
        this.customLessons[existingIdx] = lesson;
      } else {
        this.customLessons.unshift(lesson);
      }
      this.populateLessonSelect();
      const evalSelect = document.getElementById("eval-lesson-select");
      if (evalSelect) evalSelect.value = lesson.id;

      // Render worksheet into preview container
      const container = document.getElementById("worksheet-preview-area");
      if (container) {
        container.innerHTML = window.worksheetRenderer.renderToHtml(lesson, this.profile ? this.profile.name : "Akira");
        
        // Trigger glowing pulse highlight animation
        container.classList.remove("worksheet-highlight-pulse");
        void container.offsetWidth; // Reflow
        container.classList.add("worksheet-highlight-pulse");

        // Smooth scroll to the worksheet
        setTimeout(() => {
          container.scrollIntoView({ behavior: "smooth", block: "start" });
        }, 60);
      }

      // Play joyful chime after successful render
      window.soundManager.playChime();
    } catch (e) {
      console.error("Custom worksheet generation error:", e);
      alert("Error generating worksheet: " + e.message);
    } finally {
      btn.disabled = false;
      btn.innerHTML = originalText;
    }
  }

  handleFileSelected(file) {
    this.selectedFile = file;
    const preview = document.getElementById("image-preview-elem");
    const previewContainer = document.getElementById("preview-container");
    const dropzonePrompt = document.getElementById("dropzone-prompt");

    const reader = new FileReader();
    reader.onload = (e) => {
      preview.src = e.target.result;
      previewContainer.style.display = "block";
      dropzonePrompt.style.display = "none";
    };
    reader.readAsDataURL(file);
    window.soundManager.playPop();
  }

  clearSelectedFile() {
    this.selectedFile = null;
    document.getElementById("worksheet-file-input").value = "";
    document.getElementById("preview-container").style.display = "none";
    document.getElementById("dropzone-prompt").style.display = "block";
  }

  async submitEvaluation() {
    if (!this.selectedFile) {
      alert("Please choose or snap a photo of the completed worksheet first!");
      return;
    }

    const lessonId = document.getElementById("eval-lesson-select").value || "jk_trace_straight_lines";
    const btn = document.getElementById("btn-submit-eval");
    const originalText = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = `<span>🌟 Akira's Teacher is evaluating work...</span>`;

    const formData = new FormData();
    formData.append("image", this.selectedFile);
    formData.append("lesson_id", lessonId);

    try {
      const res = await fetch("/api/evaluate", {
        method: "POST",
        body: formData
      });

      if (!res.ok) throw new Error("Evaluation request failed");
      const data = await res.json();
      const evalResult = data.evaluation;

      // Play fanfare or chime
      if (evalResult.stars >= 4) {
        window.soundManager.playFanfare();
      } else {
        window.soundManager.playChime();
      }

      this.renderEvaluationResult(evalResult);
      await this.loadProfile();
      await this.loadCurriculum();
      await this.loadPortfolio();
    } catch (e) {
      alert("Error evaluating worksheet: " + e.message);
    } finally {
      btn.disabled = false;
      btn.innerHTML = originalText;
    }
  }

  renderEvaluationResult(ev) {
    const container = document.getElementById("eval-result-container");
    container.style.display = "block";

    let starsStr = "";
    for (let i = 0; i < 5; i++) {
      starsStr += i < ev.stars ? "⭐" : "☆";
    }

    const observationsHtml = ev.detailed_observations.map(obs => `
      <div class="obs-item">
        <strong>${this.escapeHtml(obs.item_label)}:</strong> ${this.escapeHtml(obs.observed)}
        ${obs.tip ? `<div style="font-size: 0.85rem; color: #64748b; margin-top: 2px;">💡 ${this.escapeHtml(obs.tip)}</div>` : ''}
      </div>
    `).join("");

    const recsHtml = (ev.recommended_next_lessons || []).map(r => `
      <button class="btn btn-secondary" style="font-size: 0.85rem; padding: 0.4rem 0.8rem;" onclick="app.previewAndPrintLesson('${r.id}')">
        ${r.icon || '📝'} ${this.escapeHtml(r.title)}
      </button>
    `).join("");

    container.innerHTML = `
      <div class="eval-card">
        <div class="eval-banner">
          <div>
            <h2>${this.escapeHtml(ev.praise_title)}</h2>
            <p>${this.escapeHtml(ev.praise_message)}</p>
          </div>
          <div style="text-align: right;">
            <div class="stars-row">${starsStr}</div>
            <div style="font-weight: 700; font-size: 1.1rem; opacity: 0.9;">${ev.overall_score_percent}% Mastery</div>
          </div>
        </div>

        <!-- Kid Voice Box -->
        <div class="voice-box">
          <div>
            <div style="font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: #a21caf; margin-bottom: 4px;">Akira's Teacher's Voice Note 🎙️</div>
            <div class="voice-text">"${this.escapeHtml(ev.voice_feedback)}"</div>
          </div>
          <button class="btn btn-primary" onclick="window.soundManager.speakFeedback('${this.escapeQuotes(ev.voice_feedback)}')">
            🔊 Listen
          </button>
        </div>

        <!-- Detailed Observations -->
        <div style="margin-bottom: 1.25rem;">
          <h4 style="margin-bottom: 0.5rem; font-family: var(--font-heading);">🔍 Stroke & Answer Observations:</h4>
          <div class="observations-list">
            ${observationsHtml}
          </div>
        </div>

        <!-- Parent Coaching Tip -->
        <div class="parent-tip-box" style="margin-bottom: 1.5rem;">
          <strong>👨‍👩‍👧 Note for Parent:</strong> ${this.escapeHtml(ev.parent_coaching_tip)}
        </div>

        <!-- Recommended Next Steps -->
        <div style="border-top: 1px solid var(--border-color); padding-top: 1.25rem;">
          <h4 style="margin-bottom: 0.5rem; font-family: var(--font-heading);">🚀 Recommended Next Lessons to Print:</h4>
          <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
            ${recsHtml}
          </div>
        </div>
      </div>
    `;

    container.scrollIntoView({ behavior: "smooth" });

    // Speak automatically on completion!
    window.soundManager.speakFeedback(ev.voice_feedback);
  }

  async loadPortfolio() {
    try {
      const res = await fetch("/api/portfolio");
      const data = await res.json();
      const submissions = data.submissions || [];

      const grid = document.getElementById("portfolio-grid");
      if (!grid) return;

      if (submissions.length === 0) {
        grid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 3rem;">No completed worksheets yet. Print a worksheet and upload your child's work to start the memory vault!</div>`;
        return;
      }

      grid.innerHTML = submissions.map(sub => {
        let starsStr = "";
        for (let i = 0; i < (sub.stars || 5); i++) starsStr += "⭐";

        const dateFormatted = new Date(sub.submitted_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });

        return `
          <div class="portfolio-card">
            <div class="portfolio-img-wrap" onclick="window.open('${sub.image_path}', '_blank')">
              <img src="${sub.image_path}" alt="Worksheet by ${sub.child_name}" loading="lazy" />
            </div>
            <div class="portfolio-body">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
                <span class="tag tag-grade">${sub.grade}</span>
                <span style="font-size: 0.8rem; color: var(--text-muted);">${dateFormatted}</span>
              </div>
              <h4 style="font-family: var(--font-heading); margin-bottom: 0.25rem;">${this.escapeHtml(sub.praise_title)}</h4>
              <div style="font-size: 1.1rem; margin-bottom: 0.5rem;">${starsStr}</div>
              <p style="font-size: 0.85rem; color: var(--text-muted); line-height: 1.3;">${this.escapeHtml(sub.praise_message)}</p>
            </div>
          </div>
        `;
      }).join("");
    } catch (e) {
      console.error("Failed to load portfolio", e);
    }
  }

  async saveProfileSettings() {
    const name = document.getElementById("input-child-name").value;
    const grade = document.getElementById("input-child-grade").value;
    const age = parseFloat(document.getElementById("input-child-age").value) || 4.0;

    const updated = {
      ...this.profile,
      name: name,
      grade: grade,
      age: age
    };

    try {
      const res = await fetch("/api/profile", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updated)
      });
      if (res.ok) {
        window.soundManager.playChime();
        await this.loadProfile();
        await this.loadCurriculum();
        await this.loadRecommendations();
        alert("Child Profile & Grade Settings updated!");
      }
    } catch (e) {
      alert("Error saving settings: " + e.message);
    }
  }

  escapeHtml(str) {
    if (!str) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  escapeQuotes(str) {
    if (!str) return "";
    return String(str).replace(/'/g, "\\'").replace(/"/g, '\\"');
  }
}

window.app = new App();
