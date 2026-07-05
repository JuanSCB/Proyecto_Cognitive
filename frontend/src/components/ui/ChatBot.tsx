import { useState, type FormEvent } from 'react';

const initialMessages: Message[] = [
  {
    from: 'bot',
    text: 'Hola, soy LumiBot.\n\nPuedo responder preguntas sobre:\n\n• ESP32\n\n• BH1750\n\n• Dashboard\n\n• Consumo energético\n\n• Salones\n\n• Roles Administrador y Alumno\n\n• Funcionamiento del sistema.'
  }
];

type Message = {
  from: 'user' | 'bot';
  text: string;
};

const sanitizeMarkdown = (text: string) => {
  if (!text) return '';
  return text
    .replace(/\*\*(.*?)\*\*/g, '$1')
    .replace(/(^|\n)[ \t]*[#*]+[ \t]*/g, '$1')
    .replace(/[\*#]/g, '')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
};

const ChatBot = () => {
  const [open, setOpen] = useState(false);
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const API_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';

  const sendMessage = async () => {
    const trimmed = message.trim();
    if (!trimmed) return;

    const userMessage: Message = { from: 'user', text: trimmed };
    setMessages(prev => [...prev, userMessage]);
    setMessage('');
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ mensaje: trimmed })
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = await response.json();
      const respuesta = sanitizeMarkdown(String(data.respuesta || 'Lo siento, no pude generar una respuesta.'));

      setMessages(prev => [...prev, { from: 'bot', text: respuesta }]);
    } catch (err) {
      setError('Error al conectar con LumiBot. Intenta de nuevo.');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    sendMessage();
  };

  return (
    <div className="fixed bottom-6 right-6 z-50"> 
      <button
        type="button"
        onClick={() => setOpen(prev => !prev)}
        className="inline-flex h-14 w-14 items-center justify-center rounded-full bg-slate-900 text-xl text-white shadow-xl transition hover:bg-slate-700"
      >
        💬
      </button>

      {open && (
        <div className="mt-4 w-[340px] rounded-3xl border border-slate-200 bg-white p-4 shadow-2xl">
          <div className="mb-4 border-b border-slate-200 pb-3">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-semibold text-slate-900">LumiBot</p>
                <p className="text-xs text-slate-500">Asistente del Sistema Inteligente de Iluminación Académica</p>
              </div>
              <button type="button" onClick={() => setOpen(false)} className="text-slate-400 hover:text-slate-700">✕</button>
            </div>
          </div>

          <div className="max-h-[320px] space-y-3 overflow-y-auto pb-2">
            {messages.map((msg, index) => (
              <div key={`${msg.from}-${index}`} className={msg.from === 'user' ? 'text-right' : 'text-left'}>
                <div className={`inline-block rounded-3xl px-4 py-3 text-sm ${msg.from === 'user' ? 'bg-slate-900 text-white' : 'bg-slate-100 text-slate-900'}`}>
                  {msg.text.split('\n').map((line, lineIndex) => (
                    <p key={lineIndex} className="leading-6">{line}</p>
                  ))}
                </div>
              </div>
            ))}
          </div>

          {error && <p className="mb-2 rounded-2xl bg-rose-50 px-3 py-2 text-xs text-rose-700">{error}</p>}

          <form onSubmit={handleSubmit} className="mt-3 flex gap-2">
            <input
              value={message}
              onChange={event => setMessage(event.target.value)}
              placeholder="Escribe tu pregunta..."
              className="w-full rounded-3xl border border-slate-300 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none focus:border-slate-500"
            />
            <button
              type="submit"
              disabled={loading}
              className="rounded-3xl bg-slate-900 px-4 py-3 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {loading ? 'Enviando...' : 'Enviar'}
            </button>
          </form>
        </div>
      )}
    </div>
  );
};

export default ChatBot;
