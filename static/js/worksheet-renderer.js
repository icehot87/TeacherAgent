// Vector SVG & Printable HTML Worksheet Renderer for All Grades (JK -> Grade 2+)
// Robust, type-safe, and developmentally structured for children.

class WorksheetRenderer {
  renderToHtml(lesson, childName = "Akira") {
    if (!lesson) {
      return `
        <div class="worksheet-page" id="printable-worksheet-content">
          <div style="text-align: center; padding: 3rem; color: var(--text-muted);">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📄</div>
            <p>Select any lesson or generate a custom worksheet to preview and print!</p>
          </div>
        </div>
      `;
    }

    const gradeTag = lesson.grade || "JK";
    const dateStr = new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    const isCustom = lesson.is_custom || (lesson.id && String(lesson.id).startsWith("custom_"));

    let exercisesHtml = "";
    if (lesson.exercises && Array.isArray(lesson.exercises) && lesson.exercises.length > 0) {
      exercisesHtml = lesson.exercises.map((ex, idx) => {
        try {
          return this.renderExercise(ex, idx + 1);
        } catch (err) {
          console.error("Error rendering exercise:", ex, err);
          return this.renderGenericExercise(ex, idx + 1);
        }
      }).join("");
    } else {
      exercisesHtml = `<div class="ws-exercise-box"><p>Standard practice exercise for ${this.escapeHtml(lesson.title || 'Learning Activity')}</p></div>`;
    }

    const customBadge = isCustom ? `
      <span style="background: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; padding: 0.2rem 0.55rem; border-radius: 999px; font-size: 0.75rem; font-weight: 700; display: inline-flex; align-items: center; gap: 0.3rem;">
        ✨ Custom AI Activity
      </span>
    ` : '';

    return `
      <div class="worksheet-page animate-fade-in" id="printable-worksheet-content" style="position: relative;">
        <!-- Worksheet Header -->
        <div class="ws-header">
          <div class="ws-title-group">
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem;">
              <h2>${this.escapeHtml(lesson.title || 'Learning Worksheet')}</h2>
              ${customBadge}
            </div>
            <p>${this.escapeHtml(lesson.subtitle || '')}</p>
          </div>
          <div class="ws-meta-fields">
            <div><strong>Name:</strong> <span class="ws-field-line">${childName ? this.escapeHtml(childName) : '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'}</span></div>
            <div><strong>Date:</strong> <span class="ws-field-line">${dateStr}</span></div>
            <div style="font-size: 0.85rem; color: #555;"><strong>Grade:</strong> ${this.escapeHtml(gradeTag)} &nbsp;|&nbsp; <strong>Stars:</strong> ⭐ ⭐ ⭐ ⭐ ⭐</div>
          </div>
        </div>

        <!-- Instructions -->
        <div style="background: #fdfbf7; border-left: 3px solid #f59e0b; padding: 0.6rem 0.8rem; margin-bottom: 1.25rem; font-size: 0.95rem; border-radius: 0 6px 6px 0;">
          <strong>🎯 Goal:</strong> ${this.escapeHtml(lesson.instructions_for_child || 'Complete each exercise carefully and do your best!')}
        </div>

        <!-- Exercises List -->
        <div class="ws-exercises-container">
          ${exercisesHtml}
        </div>

        <!-- Footer / Encouragement -->
        <div style="margin-top: 1.5rem; text-align: center; border-top: 1px dashed #ccc; padding-top: 0.75rem; font-size: 0.85rem; color: #666;">
          🌟 <em>Akira's Teacher: "${this.escapeHtml(lesson.instructions_for_parent || 'Take your time, enjoy your work, and do your best!')}"</em> 🌟
        </div>
      </div>
    `;
  }

  renderExercise(ex, num = 1) {
    if (!ex) return "";
    const promptText = ex.prompt || `Exercise ${num}`;
    const data = ex.data || {};
    let body = "";

    switch (ex.type) {
      case "trace_line":
        body = this.renderTraceLine(data);
        break;
      case "trace_letter":
        body = this.renderTraceLetter(data);
        break;
      case "trace_shape":
        body = this.renderTraceShape(data);
        break;
      case "count_items":
        body = this.renderCountItems(data);
        break;
      case "fill_pattern":
        body = this.renderPattern(data);
        break;
      case "cvc_box":
        body = this.renderCvcBox(data);
        break;
      case "math_problem":
        body = this.renderMathProblem(data);
        break;
      case "reading_passage":
        body = this.renderReadingPassage(data);
        break;
      case "circle_item":
        body = this.renderCircleItem(data);
        break;
      case "match_pair":
        body = this.renderMatchPair(data);
        break;
      default:
        body = this.renderGenericExercise(ex, num);
    }

    return `
      <div class="ws-exercise-box">
        <div class="ws-prompt">${num}. ${this.escapeHtml(promptText)}</div>
        <div class="ws-exercise-body">
          ${body}
        </div>
      </div>
    `;
  }

  renderTraceLine(data = {}) {
    const rawStyle = String(data.style || "horizontal").toLowerCase();
    const count = Math.min(Math.max(parseInt(data.count) || 3, 1), 6);
    const startIcon = data.start_icon || data.startIcon || data.icon || "⭐";
    const endIcon = data.end_icon || data.endIcon || "🏁";

    let rows = [];
    for (let i = 0; i < count; i++) {
      let pathD = "M 50,25 L 350,25";
      if (rawStyle.includes("wave") || rawStyle.includes("wavy") || rawStyle.includes("curve")) {
        pathD = "M 50,25 Q 100,5 150,25 T 250,25 T 350,25";
      } else if (rawStyle.includes("zigzag") || rawStyle.includes("mountain") || rawStyle.includes("peak")) {
        pathD = "M 50,35 L 100,10 L 150,35 L 200,10 L 250,35 L 300,10 L 350,35";
      } else if (rawStyle.includes("diagonal") || rawStyle.includes("slant")) {
        pathD = (i % 2 === 0) ? "M 50,10 L 350,40" : "M 50,40 L 350,10";
      } else if (rawStyle.includes("loop")) {
        pathD = "M 50,30 C 100,5 120,45 150,25 C 180,5 200,45 230,25 C 260,5 280,45 350,25";
      } else if (rawStyle.includes("vert")) {
        pathD = "M 50,25 L 350,25";
      }

      rows.push(`
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.6rem;">
          <span style="font-size: 1.6rem; min-width: 38px; text-align: center;">${startIcon}</span>
          <svg style="flex: 1; height: 48px; margin: 0 10px;" viewBox="0 0 400 50" preserveAspectRatio="none">
            <path d="${pathD}" fill="none" stroke="#222" stroke-width="2.5" stroke-dasharray="6,6" stroke-linecap="round" />
            <circle cx="50" cy="25" r="4" fill="#000" />
            <circle cx="350" cy="25" r="4" fill="#000" />
          </svg>
          <span style="font-size: 1.6rem; min-width: 38px; text-align: center;">${endIcon}</span>
        </div>
      `);
    }
    return rows.join("");
  }

  renderTraceLetter(data = {}) {
    const rawLet = String(data.letter || data.upper || "A").trim();
    const upper = (data.upper || (rawLet ? rawLet[0].toUpperCase() : "A")).toUpperCase();
    const lower = (data.lower || (rawLet ? rawLet[0].toLowerCase() : "a")).toLowerCase();
    const soundWord = data.sound_word || data.soundWord || data.word || "";
    const icon = data.icon || data.item_icon || data.emoji || "🍎";

    return `
      <div style="display: flex; align-items: center; justify-content: space-between; gap: 1.5rem; background: #fff; padding: 0.5rem;">
        <div style="display: flex; align-items: center; gap: 0.75rem; border-right: 2px dashed #000; padding-right: 1.25rem; min-width: 140px;">
          <span style="font-size: 2.8rem;">${icon}</span>
          <div>
            <div style="font-size: 1.5rem; font-weight: bold; font-family: 'Outfit', sans-serif;">${upper} ${lower}</div>
            <div style="font-size: 0.95rem; color: #444;">${this.escapeHtml(soundWord)}</div>
          </div>
        </div>
        <div style="flex: 1;">
          <!-- 3-line Handwriting Guide with Uppercase Letters -->
          <div style="border-top: 1.5px solid #000; border-bottom: 1.5px solid #000; position: relative; height: 55px; margin-bottom: 8px; display: flex; align-items: center; justify-content: space-around; background: #fafafa;">
            <div style="position: absolute; top: 50%; left: 0; right: 0; border-top: 1.5px dashed #999; pointer-events: none;"></div>
            <span style="font-size: 2.2rem; font-weight: 700; color: #000; z-index: 2;">${upper}</span>
            <span style="font-size: 2.2rem; color: #777; letter-spacing: 4px; border: 1.5px dashed #999; padding: 0 10px; border-radius: 4px; z-index: 2;">${upper}</span>
            <span style="font-size: 2.2rem; color: #777; letter-spacing: 4px; border: 1.5px dashed #999; padding: 0 10px; border-radius: 4px; z-index: 2;">${upper}</span>
            <span style="font-size: 2.2rem; color: #ccc; border: 1.5px dashed #bbb; padding: 0 18px; border-radius: 4px; z-index: 2;">&nbsp;</span>
          </div>

          <!-- 3-line Handwriting Guide with Lowercase Letters -->
          <div style="border-top: 1.5px solid #000; border-bottom: 1.5px solid #000; position: relative; height: 55px; display: flex; align-items: center; justify-content: space-around; background: #fafafa;">
            <div style="position: absolute; top: 50%; left: 0; right: 0; border-top: 1.5px dashed #999; pointer-events: none;"></div>
            <span style="font-size: 2.2rem; font-weight: 700; color: #000; z-index: 2;">${lower}</span>
            <span style="font-size: 2.2rem; color: #777; letter-spacing: 4px; border: 1.5px dashed #999; padding: 0 10px; border-radius: 4px; z-index: 2;">${lower}</span>
            <span style="font-size: 2.2rem; color: #777; letter-spacing: 4px; border: 1.5px dashed #999; padding: 0 10px; border-radius: 4px; z-index: 2;">${lower}</span>
            <span style="font-size: 2.2rem; color: #ccc; border: 1.5px dashed #bbb; padding: 0 18px; border-radius: 4px; z-index: 2;">&nbsp;</span>
          </div>
        </div>
      </div>
    `;
  }

  renderCountItems(data = {}) {
    const targetCount = Math.min(Math.max(parseInt(data.target_count || data.count || data.numeral || 3) || 3, 1), 10);
    const icon = data.item_icon || data.icon || data.item || "⭐";
    const numeral = String(data.numeral || targetCount);

    let iconsHtml = "";
    for (let i = 0; i < targetCount; i++) {
      iconsHtml += `<span style="font-size: 2.2rem; display: inline-block; margin: 4px;">${icon}</span>`;
    }

    return `
      <div style="display: flex; align-items: center; justify-content: space-between; gap: 1.5rem; flex-wrap: wrap;">
        <div style="border: 2px solid #000; border-radius: 8px; padding: 0.75rem 1.25rem; min-width: 200px; text-align: center; background: #fff;">
          ${iconsHtml}
        </div>
        <div style="display: flex; align-items: center; gap: 1rem;">
          <div style="font-size: 1.1rem; font-weight: bold;">Trace Number:</div>
          <div style="border: 2px dashed #000; border-radius: 8px; padding: 0.35rem 1.2rem; font-size: 2.2rem; font-weight: bold; color: #555; letter-spacing: 8px; background: #fafafa;">
            ${numeral} ${numeral} ${numeral}
          </div>
        </div>
      </div>
    `;
  }

  renderTraceShape(data = {}) {
    const rawShape = String(data.shape || "circle").toLowerCase();
    const name = data.name || (rawShape.charAt(0).toUpperCase() + rawShape.slice(1));

    let svgShape = `<circle cx="50" cy="50" r="38" stroke="#000" stroke-width="2.5" stroke-dasharray="6,6" fill="none"/>`;
    if (rawShape.includes("square")) {
      svgShape = `<rect x="15" y="15" width="70" height="70" stroke="#000" stroke-width="2.5" stroke-dasharray="6,6" fill="none"/>`;
    } else if (rawShape.includes("triangle")) {
      svgShape = `<polygon points="50,15 90,85 10,85" stroke="#000" stroke-width="2.5" stroke-dasharray="6,6" fill="none"/>`;
    } else if (rawShape.includes("star")) {
      svgShape = `<polygon points="50,10 62,38 92,38 67,56 77,85 50,67 23,85 33,56 8,38 38,38" stroke="#000" stroke-width="2.5" stroke-dasharray="5,5" fill="none"/>`;
    } else if (rawShape.includes("heart")) {
      svgShape = `<path d="M 50,30 A 18,18 0 0,0 20,45 C 20,70 50,85 50,85 C 50,85 80,70 80,45 A 18,18 0 0,0 50,30 Z" stroke="#000" stroke-width="2.5" stroke-dasharray="5,5" fill="none"/>`;
    } else if (rawShape.includes("diamond")) {
      svgShape = `<polygon points="50,12 88,50 50,88 12,50" stroke="#000" stroke-width="2.5" stroke-dasharray="5,5" fill="none"/>`;
    }

    return `
      <div style="display: flex; align-items: center; justify-content: space-around; gap: 1rem; flex-wrap: wrap;">
        <div style="text-align: center;">
          <svg width="105" height="105" viewBox="0 0 100 100">
            ${svgShape}
            <circle cx="50" cy="14" r="3.5" fill="#000"/>
          </svg>
          <div style="font-size: 1.1rem; font-weight: bold; margin-top: 0.25rem;">${this.escapeHtml(name)}</div>
        </div>
        <div style="border: 2px dashed #666; border-radius: 8px; width: 160px; height: 105px; display: flex; align-items: center; justify-content: center; font-size: 0.95rem; color: #666; text-align: center; padding: 8px; background: #fdfdfd;">
          Draw your own ${this.escapeHtml(name)} here! ✏️
        </div>
      </div>
    `;
  }

  renderPattern(data = {}) {
    let sequence = data.sequence || ["🍎", "🍌", "🍎", "🍌"];
    let choices = data.choices || ["🍎", "🍌", "🍇"];

    if (typeof sequence === "string") {
      sequence = sequence.split(/\s+/).filter(Boolean);
    }
    if (typeof choices === "string") {
      choices = choices.split(/\s+/).filter(Boolean);
    }
    if (!Array.isArray(sequence) || sequence.length === 0) {
      sequence = ["🍎", "🍌", "🍎", "🍌"];
    }
    if (!Array.isArray(choices) || choices.length === 0) {
      choices = ["🍎", "🍌", "🍇"];
    }

    const seqHtml = sequence.map(item => `
      <div style="font-size: 2rem; border: 2px solid #000; border-radius: 8px; padding: 0.35rem 0.75rem; min-width: 48px; text-align: center; background: #fff;">${item}</div>
    `).join("");

    const choiceHtml = choices.map(c => `
      <div style="font-size: 2rem; border: 2px dashed #000; border-radius: 50%; width: 56px; height: 56px; display: flex; align-items: center; justify-content: center; background: #fff;">${c}</div>
    `).join("");

    return `
      <div style="display: flex; flex-direction: column; gap: 1rem;">
        <div style="display: flex; align-items: center; gap: 0.6rem; justify-content: center; flex-wrap: wrap;">
          ${seqHtml}
          <div style="font-size: 2rem; border: 2.5px dashed #d97706; border-radius: 8px; padding: 0.35rem 0.85rem; background: #fffbeb; font-weight: bold; color: #b45309;">❓</div>
        </div>
        <div style="display: flex; align-items: center; justify-content: center; gap: 1.25rem; margin-top: 0.5rem; flex-wrap: wrap;">
          <span style="font-weight: bold; font-size: 1rem;">Circle Answer:</span>
          ${choiceHtml}
        </div>
      </div>
    `;
  }

  renderCvcBox(data = {}) {
    const icon = data.icon || data.image_hint || "🐱";
    let letters = data.letters;
    if (typeof letters === "string") {
      letters = letters.split("");
    } else if (!Array.isArray(letters)) {
      if (data.word) {
        letters = String(data.word).split("");
      } else {
        letters = ["C", "A", "T"];
      }
    }

    const boxes = letters.map(l => `
      <div style="border: 2px solid #000; border-radius: 6px; width: 65px; height: 75px; position: relative; display: flex; flex-direction: column; align-items: center; justify-content: center; background: #fff;">
        <div style="position: absolute; top: 50%; left: 0; right: 0; border-top: 1.5px dashed #999;"></div>
        <span style="font-size: 2.2rem; color: #777; border-bottom: 2px solid #000; width: 80%; text-align: center; font-weight: bold;">${this.escapeHtml(l)}</span>
        <div style="width: 8px; height: 8px; border-radius: 50%; background: #000; margin-top: 4px;"></div>
      </div>
    `).join("");

    return `
      <div style="display: flex; align-items: center; justify-content: space-around; gap: 1.5rem; flex-wrap: wrap;">
        <div style="font-size: 3.2rem; text-align: center;">${icon}</div>
        <div style="display: flex; gap: 0.75rem;">
          ${boxes}
        </div>
      </div>
    `;
  }

  renderMathProblem(data = {}) {
    const op1 = Math.min(Math.max(parseInt(data.operand1 || data.num1 || 2) || 2, 0), 10);
    const op2 = Math.min(Math.max(parseInt(data.operand2 || data.num2 || 1) || 1, 0), 10);
    const operator = data.operator || "+";
    const icon = data.icon || data.item_icon || "⭐";

    let g1 = "", g2 = "";
    for (let i = 0; i < op1; i++) g1 += icon;
    for (let i = 0; i < op2; i++) g2 += icon;

    return `
      <div style="display: flex; align-items: center; justify-content: space-around; font-size: 1.8rem; font-weight: bold; flex-wrap: wrap; gap: 0.75rem;">
        <div style="text-align: center;">
          <div style="font-size: 1.8rem; min-height: 35px;">${g1 || '0'}</div>
          <div style="font-size: 1.8rem;">${op1}</div>
        </div>
        <div style="font-size: 2.2rem; color: #2563eb;">${this.escapeHtml(operator)}</div>
        <div style="text-align: center;">
          <div style="font-size: 1.8rem; min-height: 35px;">${g2 || '0'}</div>
          <div style="font-size: 1.8rem;">${op2}</div>
        </div>
        <div style="font-size: 2.2rem;">=</div>
        <div style="border: 2.5px solid #000; border-radius: 8px; width: 70px; height: 70px; display: flex; align-items: center; justify-content: center; font-size: 2rem; color: #bbb; background: #fff;">
          ?
        </div>
      </div>
    `;
  }

  renderReadingPassage(data = {}) {
    const passage = data.passage || data.text || "I see the stars in the night sky. The rocket flies up high!";
    let questions = data.questions || [];
    if (!Array.isArray(questions)) questions = [];

    const qsHtml = questions.map((q, idx) => {
      const qText = typeof q === "string" ? q : (q.q || q.question || `Question ${idx + 1}`);
      let options = (q && Array.isArray(q.options)) ? q.options : ((q && Array.isArray(q.choices)) ? q.choices : ["Yes", "No"]);
      
      return `
        <div style="margin-top: 0.85rem; font-size: 1rem;">
          <strong>Q${idx + 1}: ${this.escapeHtml(qText)}</strong>
          <div style="display: flex; gap: 1.25rem; margin-top: 0.35rem; flex-wrap: wrap;">
            ${options.map(opt => `
              <label style="display: inline-flex; align-items: center; gap: 0.4rem; cursor: pointer; background: #f8fafc; padding: 0.25rem 0.6rem; border-radius: 6px; border: 1px solid #cbd5e1;">
                <span style="display: inline-block; width: 18px; height: 18px; border: 2px solid #000; border-radius: 4px; background: #fff;"></span>
                <span>${this.escapeHtml(opt)}</span>
              </label>
            `).join("")}
          </div>
        </div>
      `;
    }).join("");

    return `
      <div style="display: flex; flex-direction: column; gap: 0.75rem;">
        <div style="background: #fdfdfd; border: 2px solid #000; border-radius: 8px; padding: 1.1rem; font-size: 1.15rem; line-height: 1.6; font-family: 'Inter', sans-serif;">
          📖 <em>${this.escapeHtml(passage)}</em>
        </div>
        <div style="padding-left: 0.25rem;">
          ${qsHtml}
        </div>
      </div>
    `;
  }

  renderCircleItem(data = {}) {
    const items = Array.isArray(data.items) ? data.items : ["🦁", "🚀", "👑", "🦖"];
    const target = data.target || "the matching item";

    return `
      <div style="display: flex; align-items: center; justify-content: center; gap: 1.5rem; flex-wrap: wrap;">
        ${items.map(item => `
          <div style="font-size: 2.8rem; border: 2px dashed #000; border-radius: 12px; padding: 0.5rem 1rem; background: #fff; text-align: center;">
            ${item}
          </div>
        `).join("")}
      </div>
    `;
  }

  renderMatchPair(data = {}) {
    const pairs = Array.isArray(data.pairs) ? data.pairs : [
      { left: "A", right: "🍎" },
      { left: "B", right: "🐻" },
      { left: "C", right: "🐱" }
    ];

    return `
      <div style="display: flex; justify-content: space-around; gap: 2rem;">
        <div style="display: flex; flex-direction: column; gap: 1rem;">
          ${pairs.map(p => `<div style="font-size: 1.6rem; font-weight: bold; border: 1.5px solid #000; border-radius: 8px; padding: 0.4rem 1rem; min-width: 60px; text-align: center;">${this.escapeHtml(p.left)}</div>`).join("")}
        </div>
        <div style="display: flex; flex-direction: column; gap: 1rem;">
          ${pairs.map(p => `<div style="font-size: 1.6rem; border: 1.5px solid #000; border-radius: 8px; padding: 0.4rem 1rem; min-width: 60px; text-align: center;">${this.escapeHtml(p.right)}</div>`).join("")}
        </div>
      </div>
    `;
  }

  renderGenericExercise(ex, num = 1) {
    const prompt = ex && ex.prompt ? ex.prompt : `Practice Exercise ${num}`;
    return `
      <div style="padding: 1rem; font-size: 1.1rem; border: 1.5px dashed #cbd5e1; border-radius: 8px; background: #fafafa; min-height: 80px; display: flex; align-items: center; justify-content: center;">
        <span style="color: #475569;">✏️ ${this.escapeHtml(prompt)}</span>
      </div>
    `;
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
}

window.worksheetRenderer = new WorksheetRenderer();
