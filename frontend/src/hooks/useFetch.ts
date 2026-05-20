import { useEffect, useState } from 'react';

interface FetchState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}

const useFetch = <T,>(fetcher: () => Promise<T>, deps: any[] = []) => {
  const [state, setState] = useState<FetchState<T>>({ data: null, loading: true, error: null });

  useEffect(() => {
    let active = true;

    const load = async () => {
      setState({ data: null, loading: true, error: null });
      try {
        const data = await fetcher();
        if (!active) return;
        setState({ data, loading: false, error: null });
      } catch (error: unknown) {
        if (!active) return;
        const message =
          typeof error === 'object' && error !== null && 'data' in error
            ? (error as any).data?.message ?? String(error)
            : String(error);
        setState({ data: null, loading: false, error: message });
      }
    };

    load();

    return () => {
      active = false;
    };
  }, deps);

  return state;
};

export default useFetch;
