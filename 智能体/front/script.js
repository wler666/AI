// ============================================================
// 智能体聊天前端交互逻辑
// 当前为演示模式：发送消息后会返回一句模拟回复。
// 后续接入真实后端时，只需修改 getAgentReply() 函数即可。
// ============================================================

const chat = document.getElementById("chat");
const input = document.getElementById("msgInput");
const sendBtn = document.getElementById("sendBtn");
const resetBtn = document.getElementById("resetBtn");

// -------------------------------------------------------------
// 工具函数
// -------------------------------------------------------------
function nowTime() {
  const d = new Date();
  const h = String(d.getHours()).padStart(2, "0");
  const m = String(d.getMinutes()).padStart(2, "0");
  return `${h}:${m}`;
}

function scrollToBottom() {
  chat.scrollTop = chat.scrollHeight;
}

// 追加一条消息气泡。role: 'ai' | 'user'
function appendMessage(role, text) {
  const row = document.createElement("div");
  row.className = `msg-row ${role}`;

  const avatar = document.createElement("div");
  if (role === "ai") {
    avatar.className = "avatar ai-avatar";
    avatar.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M12 2L2 7l10 5 10-5-10-5z" fill="currentColor"/><path d="M2 17l10 5 10-5M2 12l10 5 10-5" stroke="currentColor" stroke-width="1.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
  } else {
    avatar.className = "avatar user-avatar";
    avatar.textContent = "我";
  }

  const col = document.createElement("div");
  col.className = "bubble-col";

  const bubble = document.createElement("div");
  bubble.className = `bubble ${role === "ai" ? "ai-bubble" : "user-bubble"}`;
  bubble.textContent = text;

  const time = document.createElement("span");
  time.className = "time";
  time.textContent = nowTime();

  col.appendChild(bubble);
  col.appendChild(time);

  if (role === "ai") {
    row.appendChild(avatar);
    row.appendChild(col);
  } else {
    row.appendChild(col);
    row.appendChild(avatar);
  }

  chat.appendChild(row);
  scrollToBottom();
  return { row, bubble };
}

// 显示"正在输入"占位气泡，返回一个用于移除/替换它的函数
function showTyping() {
  const row = document.createElement("div");
  row.className = "msg-row ai";

  const avatar = document.createElement("div");
  avatar.className = "avatar ai-avatar";
  avatar.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M12 2L2 7l10 5 10-5-10-5z" fill="currentColor"/><path d="M2 17l10 5 10-5M2 12l10 5 10-5" stroke="currentColor" stroke-width="1.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>`;

  const col = document.createElement("div");
  col.className = "bubble-col";

  const bubble = document.createElement("div");
  bubble.className = "bubble ai-bubble typing-bubble";
  bubble.innerHTML = "<span></span><span></span><span></span>";

  col.appendChild(bubble);
  row.appendChild(avatar);
  row.appendChild(col);
  chat.appendChild(row);
  scrollToBottom();

  return row;
}

// -------------------------------------------------------------
// 与后端智能体通信
// -------------------------------------------------------------
// TODO: 接入真实后端时，把下面的模拟逻辑换成真实请求，例如：
//
// async function getAgentReply(userText) {
//   const resp = await fetch("http://127.0.0.1:8000/api/chat", {
//     method: "POST",
//     headers: { "Content-Type": "application/json" },
//     body: JSON.stringify({ message: userText }),
//   });
//   const data = await resp.json();
//   return data.reply;
// }
//
async function getAgentReply(userText) {
  // 演示用：模拟网络延迟 + 简单回声回复
  await new Promise((r) => setTimeout(r, 700 + Math.random() * 600));
  return `（演示回复）我收到了你的消息："${userText}"。接入真实智能体后，这里会返回基于知识库检索得到的答案。`;
}

// -------------------------------------------------------------
// 发送逻辑
// -------------------------------------------------------------
async function handleSend() {
  const text = input.value.trim();
  if (!text) return;

  appendMessage("user", text);
  input.value = "";
  autoResize();
  sendBtn.disabled = true;

  const typingRow = showTyping();

  try {
    const reply = await getAgentReply(text);
    typingRow.remove();
    appendMessage("ai", reply);
  } catch (err) {
    typingRow.remove();
    appendMessage("ai", "抱歉，连接智能体服务失败，请稍后重试。");
    console.error(err);
  } finally {
    sendBtn.disabled = false;
    input.focus();
  }
}

// 输入框自适应高度
function autoResize() {
  input.style.height = "auto";
  input.style.height = Math.min(input.scrollHeight, 140) + "px";
}

// -------------------------------------------------------------
// 事件绑定
// -------------------------------------------------------------
input.addEventListener("input", autoResize);

input.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    handleSend();
  }
});

sendBtn.addEventListener("click", handleSend);

resetBtn.addEventListener("click", () => {
  if (!confirm("确定要清空当前对话吗？")) return;
  chat.innerHTML = "";
  appendMessage("ai", "对话已清空。有什么可以帮你的吗？");
});

// 初始滚动到底部
scrollToBottom();

