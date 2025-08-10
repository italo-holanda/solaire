import { createContext, useMemo, useState } from "react";
import type { ReactNode } from "react";
import type { NavigationView } from "@/types/common/navigation";
import type { Category } from "@/types";

type Params = {
  searchTerms?: string;
  categories?: Category[];
};

type NavigationContextValue = {
  currentView: NavigationView;
  setCurrentView: (view: NavigationView) => void;
  getCurrentView: () => NavigationView;

  params: Params;
  setParams: (params: Params) => void;
  getParams: () => Params;
};

export const NavigationContext = createContext<
  NavigationContextValue | undefined
>(undefined);

type NavigationProviderProps = {
  children: ReactNode;
  initialView?: NavigationView;
};

export function NavigationProvider({
  children,
  initialView = "history",
}: NavigationProviderProps) {
  const [currentView, setCurrentView] = useState<NavigationView>(initialView);
  const [params, setParams] = useState<Params>({});

  const value = useMemo<NavigationContextValue>(
    () => ({
      currentView,
      setCurrentView,
      getCurrentView: () => currentView,

      params,
      setParams,
      getParams: () => params,
    }),
    [currentView, params]
  );

  return (
    <NavigationContext.Provider value={value}>
      {children}
    </NavigationContext.Provider>
  );
}
