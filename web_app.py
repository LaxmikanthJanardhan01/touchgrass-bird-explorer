from flask import Flask, request, jsonify, render_template_string
import os
import subprocess
import sys
import tempfile
import json
import urllib.request
import urllib.error

app = Flask(__name__)

PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#091710">
<title>TouchGrass 45 Bird Explorer</title>
<style>
:root {
  --bg:#091710; --panel:#10251b; --panel2:#142d20;
  --green:#b6f28c; --text:#f2f7ed; --muted:#a0b5a3;
  --line:rgba(210,240,205,.13); --danger:#ffb7ac;
}
* {box-sizing:border-box}
body {
  margin:0; min-height:100vh; color:var(--text);
  background:
    radial-gradient(ellipse at 80% 0%,rgba(103,160,91,.14),transparent 38%),
    radial-gradient(ellipse at 0% 70%,rgba(49,110,68,.12),transparent 40%),
    var(--bg);
  font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;
}
button,input {font:inherit}
.wrap {width:min(100% - 36px,1000px);margin:auto}
nav {
  display:flex;align-items:center;justify-content:space-between;
  padding:24px 0;border-bottom:1px solid var(--line);gap:12px;
}
.brand {display:flex;align-items:center;gap:12px;font-weight:800;letter-spacing:.4px}
.logo {
  height:42px;width:42px;display:grid;place-items:center;
  background:var(--green);color:#10251a;border-radius:14px;
  font-size:14px;font-weight:900;
}
.brand small {display:block;color:var(--muted);font-size:10px;letter-spacing:2px;margin-top:3px}
.status {
  border:1px solid var(--line);border-radius:100px;padding:9px 12px;
  color:#c9efb6;font-size:12px;white-space:nowrap;
}
.status:before {content:"";display:inline-block;width:7px;height:7px;background:var(--green);border-radius:50%;margin-right:8px}
.hero {text-align:center;padding:65px 0 32px}
.eyebrow {color:var(--green);font-size:11px;font-weight:800;letter-spacing:2.8px}
h1 {font-size:clamp(36px,7vw,66px);line-height:1.05;letter-spacing:-2px;margin:18px 0}
h1 span {color:var(--green)}
.subtitle {color:var(--muted);max-width:540px;margin:0 auto;line-height:1.75;font-size:15px}
.layout {display:grid;grid-template-columns:1.1fr .9fr;gap:18px;padding:22px 0 50px}
.panel {
  border:1px solid var(--line);background:linear-gradient(155deg,rgba(20,45,32,.94),rgba(13,31,22,.94));
  border-radius:24px;padding:25px;min-width:0;
}
.panel h2 {font-size:19px;margin:0 0 8px}
.desc {font-size:13px;line-height:1.6;color:var(--muted);margin:0 0 22px}
.drop {
  min-height:220px;border:1px dashed rgba(182,242,140,.38);border-radius:18px;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  text-align:center;padding:22px;background:rgba(182,242,140,.035);cursor:pointer;
  transition:.2s;
}
.drop:hover,.drop.drag {border-color:var(--green);background:rgba(182,242,140,.09)}
.upload-icon {
  width:54px;height:54px;border-radius:17px;background:#203c29;
  display:grid;place-items:center;color:var(--green);font-size:25px;margin-bottom:16px;
}
.drop strong {font-size:15px}
.drop p {color:var(--muted);font-size:12px;margin:9px 0 0;line-height:1.6}
#fileInput {display:none}
.file-name {margin:13px 0 0;color:var(--green);font-size:12px;overflow-wrap:anywhere}
.btn {
  margin-top:18px;width:100%;padding:15px 18px;border:0;border-radius:13px;
  background:var(--green);color:#122319;font-weight:850;cursor:pointer;
  transition:transform .2s,opacity .2s;
}
.btn:hover:not(:disabled) {transform:translateY(-2px)}
.btn:disabled {opacity:.55;cursor:wait}
.hint {color:var(--muted);font-size:11px;text-align:center;margin:13px 0 0}
.result-panel {min-height:320px}
.result-empty {
  min-height:230px;display:flex;align-items:center;justify-content:center;
  flex-direction:column;text-align:center;padding:20px;color:var(--muted);
}
.result-symbol {
  display:grid;place-items:center;width:64px;height:64px;border-radius:22px;
  background:#1c3825;color:var(--green);font-size:29px;margin-bottom:16px;
}
.result-empty strong {color:#e5efe1;font-size:14px}
.result-empty p {font-size:12px;line-height:1.65;max-width:230px}
#resultContent {display:none}
.result-label {color:var(--green);font-size:10px;letter-spacing:2px;font-weight:800;margin:18px 0 10px}
#resultText {
  white-space:pre-wrap;overflow-wrap:anywhere;font:13px/1.8 ui-monospace,SFMono-Regular,Consolas,monospace;
  background:rgba(0,0,0,.19);border:1px solid var(--line);border-radius:14px;
  padding:16px;margin:0;color:#e4f0df;
}
#resultText.error {color:var(--danger)}
.spinner {
  display:inline-block;width:15px;height:15px;border:2px solid rgba(18,35,25,.3);
  border-top-color:#122319;border-radius:50%;animation:spin .7s linear infinite;
  vertical-align:middle;margin-right:8px;
}
@keyframes spin {to{transform:rotate(360deg)}}
.steps {display:flex;flex-direction:column;gap:17px;margin-top:22px}
.step {display:flex;align-items:flex-start;gap:12px}
.step-num {
  flex-shrink:0;width:30px;height:30px;border:1px solid var(--line);
  color:var(--green);display:grid;place-items:center;border-radius:10px;font-size:12px;
}
.step strong {display:block;font-size:13px;margin:2px 0 5px}
.step span {color:var(--muted);font-size:12px;line-height:1.5}
footer {border-top:1px solid var(--line);padding:20px 0 28px;text-align:center;color:var(--muted);font-size:11px;line-height:1.8}
@media(max-width:700px) {
 .wrap {width:min(100% - 24px,520px)}
 nav {padding:17px 0}.status {font-size:10px;padding:8px}
 .hero {padding:48px 0 22px}h1 {letter-spacing:-1.4px}
 .layout {grid-template-columns:1fr;padding-top:15px;gap:14px}
 .panel {padding:19px;border-radius:20px}
 .drop {min-height:185px}
}
</style>
</head>
<body>
<div class="wrap">
<nav>
  <div class="brand">
    <div class="logo">TG</div>
    <div>TOUCHGRASS<small>FIELD INTELLIGENCE</small></div>
  </div>
  <div class="status">AI ENGINE READY</div>
</nav>

<header class="hero">
  <div class="eyebrow">AI-POWERED BIRD IDENTIFICATION</div>
  <h1>Listen closer.<br><span>Discover more.</span></h1>
  <p class="subtitle">Turn birdsong into discoveries. Upload a recording and let AI help identify the birds behind the sound.</p>
</header>

<main class="layout">
<section class="panel" id="myObservation" style="grid-column:1/-1">
<h2>My Observation</h2>
<p class="desc">Write what you personally saw in nature. AI will organize your notes.</p>
<textarea id="observationText" maxlength="2000" rows="4" placeholder="Example: I heard a bird singing near a tree. The sound was clear and repeated several times." style="width:100%;padding:14px;border-radius:12px;background:#091710;color:#f2f7ed;border:1px solid rgba(210,240,205,.25);font:inherit;resize:vertical"></textarea>
<button class="btn" id="voiceBtn" type="button" style="margin-top:10px">Speak Your Observation</button>
<p id="voiceStatus" class="desc">Tap the microphone and speak. Voice support depends on your mobile browser.</p>
<button class="btn" id="journalBtn" type="button">Generate Journal Notes</button>
<pre id="journalResult" style="white-space:pre-wrap;overflow-wrap:anywhere;margin-top:14px"></pre>
</section>


  <section class="panel">
    <h2>Explore a birdsong</h2>
    <p class="desc">Choose an audio recording from your device to begin identification.</p>

    <div class="drop" id="dropArea" role="button" tabindex="0" aria-label="Choose an audio file">
      <div class="upload-icon" aria-hidden="true"><svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg></div>
      <strong>Drop your audio here</strong>
      <p>or tap to browse your device<br>MP3, WAV, OGG, FLAC, AIFF</p>
      <div class="file-name" id="fileName"></div>
    </div>
    <input id="fileInput" type="file" accept="audio/*">
    <button class="btn" id="identifyBtn" type="button">Identify bird</button>
    <p class="hint">For best results, use a clear recording with minimal background noise.</p>
  </section>

  <section class="panel result-panel">
    <h2>Identification results</h2>
    <p class="desc">Your analysis will appear here.</p>
    <div id="emptyState" class="result-empty">
      <div class="result-symbol" aria-hidden="true"><svg viewBox="0 0 24 24" width="34" height="34" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12h3l3-7 4 14 4-14 3 7h3"/></svg></div>
      <strong>Ready when you are</strong>
      <p>Your bird predictions will appear here once the recording has been analysed.</p>
    </div>
    <div id="resultContent">
      <div class="result-label" id="resultLabel">ANALYSIS OUTPUT</div>
      <pre id="resultText"></pre>
    </div>
    <div class="steps">
      <div class="step"><div class="step-num">01</div><div><strong>Upload a recording</strong><span>Select a supported bird audio file.</span></div></div>
      <div class="step"><div class="step-num">02</div><div><strong>AI listens</strong><span>BirdNET analyses the sound for possible species.</span></div></div>
      <div class="step"><div class="step-num">03</div><div><strong>Discover the result</strong><span>Review the model's predictions and scores.</span></div></div>
    </div>
  </section>
</main>

<footer>
  TOUCHGRASS BIRD EXPLORER 250 POWERED BY BIRDNET<br>
  Audio analysis runs through your local UNO Q server.
</footer>
</div>

<script>
const input = document.getElementById('fileInput');
const drop = document.getElementById('dropArea');
const fileName = document.getElementById('fileName');
const button = document.getElementById('identifyBtn');
const empty = document.getElementById('emptyState');
const resultContent = document.getElementById('resultContent');
const resultText = document.getElementById('resultText');
const resultLabel = document.getElementById('resultLabel');

function chooseFile(file) {
  if (!file) return;
  const allowed = /\.(mp3|wav|ogg|flac|aiff|aif)$/i;
  if (!allowed.test(file.name)) {
    fileName.textContent = 'Unsupported format. Please choose MP3, WAV, OGG, FLAC or AIFF.';
    input.value = '';
    return;
  }
  fileName.textContent = 'Selected: ' + file.name;
  empty.style.display = 'none';
  resultContent.style.display = 'block';
  resultLabel.textContent = 'READY TO ANALYSE';
  resultText.className = '';
  resultText.textContent = 'Your recording is ready. Tap Identify bird';
}
input.addEventListener('change', () => chooseFile(input.files[0]));
drop.addEventListener('click', () => input.click());
drop.addEventListener('keydown', e => {
  if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); input.click(); }
});
drop.addEventListener('dragover', e => { e.preventDefault(); drop.classList.add('drag'); });
drop.addEventListener('dragleave', () => drop.classList.remove('drag'));
drop.addEventListener('drop', e => {
  e.preventDefault();
  drop.classList.remove('drag');
  if (e.dataTransfer.files.length) {
    try { input.files = e.dataTransfer.files; } catch (_) {}
    chooseFile(e.dataTransfer.files[0]);
  }
});

button.addEventListener('click', analyze);

async function analyze() {
  const file = input.files[0];
  if (!file) {
    empty.style.display = 'none';
    resultContent.style.display = 'block';
    resultLabel.textContent = 'AUDIO REQUIRED';
    resultText.className = 'error';
    resultText.textContent = 'Please select an audio recording first.';
    return;
  }

  const data = new FormData();
  data.append('audio', file);
  button.disabled = true;
  button.innerHTML = '<span class="spinner"></span>Analysing birdsong...';
  empty.style.display = 'none';
  resultContent.style.display = 'block';
  resultLabel.textContent = 'BIRDNET ANALYSIS IN PROGRESS';
  resultText.className = '';
  resultText.textContent = 'Listening to your recording...\\nThis can take a little while, especially on the first run.';

  try {
    const response = await fetch('/identify', {method:'POST', body:data});
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || 'Bird analysis failed.');
    resultLabel.textContent = 'ANALYSIS COMPLETE';
    resultText.textContent = (result.result || 'No result returned.') + String.fromCharCode(10,10) + 'AI NATURE JOURNAL' + String.fromCharCode(10) + (result.journal || 'Journal unavailable.');
  } catch (error) {
    resultLabel.textContent = 'ANALYSIS ISSUE';
    resultText.className = 'error';
    resultText.textContent = error.message || 'Connection error. Please try again.';
  } finally {
    button.disabled = false;
    button.textContent = 'Identify bird';
  }
}

document.getElementById('journalBtn').addEventListener('click', async () => {
  const observation = document.getElementById('observationText').value.trim();
  const output = document.getElementById('journalResult');
  const btn = document.getElementById('journalBtn');

  if (!observation) {
    output.textContent = 'Please write your observation first.';
    return;
  }

  btn.disabled = true;
  btn.textContent = 'Generating notes...';
  output.textContent = 'Local Qwen AI is writing your journal...';

  try {
    const response = await fetch('/journal', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({observation: observation})
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Journal generation failed.');
    output.textContent = data.journal || 'No journal returned.';
  } catch (err) {
    output.textContent = 'Error: ' + err.message;
  } finally {
    btn.disabled = false;
    btn.textContent = 'Generate Journal Notes';
  }
});


const voiceBtn = document.getElementById("voiceBtn");
const voiceStatus = document.getElementById("voiceStatus");
const observationText = document.getElementById("observationText");

voiceBtn.addEventListener("click", () => {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    voiceStatus.textContent = "Voice recognition is not supported in this browser. Try Chrome.";
    return;
  }
  const recognition = new SpeechRecognition();
  recognition.lang = "hi-IN";
  recognition.continuous = false;
  recognition.interimResults = false;
  voiceBtn.disabled = true;
  voiceStatus.textContent = "Listening... Speak now.";
  recognition.onresult = (event) => {
    observationText.value = (observationText.value.trim() + " " + event.results[0][0].transcript).trim();
    voiceStatus.textContent = "Voice captured. You can edit the text before generating the journal.";
  };
  recognition.onerror = (event) => {
    voiceStatus.textContent = "Voice error: " + event.error + ". Check microphone permission.";
  };
  recognition.onend = () => { voiceBtn.disabled = false; };
  try { recognition.start(); }
  catch (error) {
    voiceStatus.textContent = "Could not start microphone. Please try again.";
    voiceBtn.disabled = false;
  }
});

</script>
</body>
</html>
"""

@app.get("/")
def home():
    return render_template_string(PAGE)

def generate_journal(bird_results):
    prompt = ("Write a short nature journal entry using ONLY these BirdNET predictions. Do not invent location, weather, bird behaviour, sounds, or other observations. BirdNET scores are model scores, not certainty. If details are missing, do not guess.\n\n" + bird_results[:3000])
    payload = {"messages": [{"role": "system", "content": "You write concise, factual nature journal entries. Never invent observations."}, {"role": "user", "content": prompt}], "temperature": 0.2, "max_tokens": 120}
    try:
        req = urllib.request.Request("http://172.23.0.1:8081/v1/chat/completions", data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=60) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"].strip()
    except Exception as exc:
        return "Nature journal unavailable: " + str(exc)[:250]


@app.post("/identify")
def identify():
    audio = request.files.get("audio")
    if not audio:
        return jsonify(error="Audio file nahi mili."), 400

    suffix = os.path.splitext(audio.filename or "")[1].lower()
    if suffix not in {".mp3", ".wav", ".ogg", ".flac", ".aiff", ".aif"}:
        return jsonify(error="Unsupported audio format. Please use MP3, WAV, OGG, FLAC or AIFF."), 400

    path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=suffix, dir="/tmp", delete=False) as f:
            path = f.name
            audio.save(path)

        worker = "/app/python/bird_worker.py"
        completed = subprocess.run(
            [sys.executable, worker, path],
            capture_output=True, text=True, timeout=300
        )
        if completed.returncode != 0:
            return jsonify(error=completed.stderr[-2000:] or "Bird analysis failed."), 500
        bird_results = completed.stdout[-5000:]
        journal = generate_journal(bird_results)
        return jsonify(result=bird_results, journal=journal)
    except subprocess.TimeoutExpired:
        return jsonify(error="Analysis mein zyada time laga. Dobara try karo."), 504
    except Exception as e:
        return jsonify(error=str(e)), 500
    finally:
        if path and os.path.exists(path):
            os.unlink(path)


@app.post("/journal")
def create_observation_journal():
    body = request.get_json(silent=True) or {}
    observation = str(body.get("observation", "")).strip()[:2000]

    if not observation:
        return jsonify(error="Please enter an observation."), 400

    prompt = (
        "Translate the users observation into accurate, natural English. "
        "The input may be Hindi, Hinglish, Kannada, Telugu, or another language. "
        "Preserve every explicitly stated fact, especially animal identity, size, "
        "colour, number, and action. Never replace one animal with another. "
        "Never invent details or remove important details. "
        "For example, तोता means parrot, not tree; "
        "कौवा means crow, and cow means cow. "
        "Return only the English translation in 1-2 sentences.\n\n"
        "User observation:\n" + observation
    )
    payload = {
        "messages": [
            {"role": "system", "content": "Translate the observation into simple English. Translate only what the user actually said. Do not guess the animal species, add colours, or invent facts. Keep unusual or impossible details exactly as stated. Return only the translation."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1,
        "max_tokens": 120
    }
    try:
        req = urllib.request.Request(
            "http://172.23.0.1:8081/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=60) as response:
            data = json.loads(response.read().decode("utf-8"))
        journal = data["choices"][0]["message"]["content"].strip()
        return jsonify(journal=journal)
    except Exception as exc:
        return jsonify(error="Qwen journal error: " + str(exc)[:200]), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
