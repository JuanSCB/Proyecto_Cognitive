import { Link } from 'react-router-dom';

const Header = () => (
  <header className="sticky top-0 z-20 border-b border-slate-200 bg-white/95 backdrop-blur-xl">
    <div className="mx-auto flex max-w-[1600px] items-center justify-between gap-4 px-4 py-4 lg:px-8">
      <Link to="/" className="text-xl font-semibold tracking-tight text-slate-900">
        Sistema de Iluminación Inteligente
      </Link>
      <div className="flex items-center gap-3 text-slate-600">
        <span className="hidden rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-sm sm:inline-flex">
          Dashboard en tiempo real
        </span>
      </div>
    </div>
  </header>
);

export default Header;
