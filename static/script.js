const chatArea = document.getElementById('chatArea');
const welcomeScreen = document.getElementById('welcomeScreen');
const userInput = document.getElementById('userInput');

let activeTool = 'llm';

function autoResize(el) {
  el.style.height = 'auto';
  el.style.height = Math.min(el.scrollHeight, 200) + 'px';
}

function handleKey(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
}

function selectTool(toolName) {
  activeTool = toolName;

  document.querySelectorAll('.tool-chip').forEach((chip) => {
    chip.classList.remove('active');
  });
  const chip = document.querySelector(`[data-tool="${toolName}"]`);
  if (chip) chip.classList.add('active');

  const placeholders = {
    llm: 'Ask anything for general research...',
    calc: 'Enter expression, e.g. 25*8+40',
    read: 'Enter file path, e.g. data/sample.txt or data/sample_pdf.pdf',
    find: 'Enter keyword to find in the loaded document...',
    summarize: 'Enter PDF path, e.g. data/sample_pdf.pdf',
  };

  userInput.placeholder = placeholders[toolName] || placeholders.llm;
  userInput.focus();
}

function buildCommand(input) {
  const text = input.trim();
  if (!text) return '';

  if (activeTool === 'calc') return `calculate ${text}`;
  if (activeTool === 'read') return `read ${text}`;
  if (activeTool === 'find') return `find ${text}`;
  if (activeTool === 'summarize') return `summarize pdf ${text}`;
  return text;
}

function runQuickAction(type) {
  const examples = {
    read: 'data/sample.txt',
    find: 'agent',
    calc: '2+3*10',
    summarize: 'data/sample_pdf.pdf',
  };

  const tools = {
    read: 'read',
    find: 'find',
    calc: 'calc',
    summarize: 'summarize',
  };

  selectTool(tools[type]);
  userInput.value = examples[type] || '';
  autoResize(userInput);
  sendMessage();
}

function appendMessage(sender, text) {
  const msgDiv = document.createElement('div');
  msgDiv.className = `message ${sender}`;

  if (sender === 'bot') {
    const icon = document.createElement('div');
    icon.className = 'bot-icon';
    icon.innerHTML = '✦';
    msgDiv.appendChild(icon);
  }

  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.textContent = text;
  msgDiv.appendChild(bubble);

  chatArea.appendChild(msgDiv);
  chatArea.scrollTop = chatArea.scrollHeight;
}

function setSendingState(isSending) {
  const sendBtn = document.getElementById('sendBtn');
  sendBtn.disabled = isSending;
  sendBtn.style.opacity = isSending ? '0.5' : '';
}

async function sendMessage() {
  const raw = userInput.value.trim();
  if (!raw) return;

  if (welcomeScreen && welcomeScreen.style.display !== 'none') {
    welcomeScreen.style.display = 'none';
  }

  const command = buildCommand(raw);
  appendMessage('user', command);

  userInput.value = '';
  userInput.style.height = 'auto';
  setSendingState(true);

  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: command }),
    });

    const data = await res.json();
    appendMessage('bot', data.response || data.error || 'No response.');
  } catch (err) {
    appendMessage('bot', 'Could not reach the backend.');
  } finally {
    setSendingState(false);
    userInput.focus();
  }
}

selectTool('llm');
