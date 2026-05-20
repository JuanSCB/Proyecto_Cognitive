import { ReactNode } from 'react';

interface CardProps {
  title?: string;
  children: ReactNode;
  className?: string;
}

const Card = ({ title, children, className = '' }: CardProps) => (
  <section className={`rounded-3xl border border-slate-200 bg-white p-5 shadow-soft ${className}`}>
    {title ? <h2 className="mb-4 text-lg font-semibold text-slate-900">{title}</h2> : null}
    {children}
  </section>
);

export default Card;
