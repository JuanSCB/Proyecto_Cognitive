import { BrowserRouter } from 'react-router-dom';
import AppRoutes from './routes';
import ChatBot from './components/ui/ChatBot';

function App() {
  return (
    <BrowserRouter
      future={{
        v7_startTransition: true,
        v7_relativeSplatPath: true
      }}
    >
      <div className="min-h-screen bg-slate-50">
        <AppRoutes />
        <ChatBot />
      </div>
    </BrowserRouter>
  );
}

export default App;
