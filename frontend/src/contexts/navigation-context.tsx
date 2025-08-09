import { createContext, useContext, useMemo, useState } from "react";
import type { ReactNode } from "react";
import type { NavigationView } from "@/types/common/navigation";

type NavigationContextValue = {
  currentView: NavigationView;
  setCurrentView: (view: NavigationView) => void;
  getCurrentView: () => NavigationView;
};

export const NavigationContext = createContext<NavigationContextValue | undefined>(
  undefined
);

type NavigationProviderProps = {
  children: ReactNode;
  initialView?: NavigationView;
};

export function NavigationProvider({
  children,
  initialView = "history",
}: NavigationProviderProps) {
  const [currentView, setCurrentView] = useState<NavigationView>(initialView);

  const value = useMemo<NavigationContextValue>(
    () => ({
      currentView,
      setCurrentView,
      getCurrentView: () => currentView,
    }),
    [currentView]
  );

  return (
    <NavigationContext.Provider value={value}>
      {children}
    </NavigationContext.Provider>
  );
}


