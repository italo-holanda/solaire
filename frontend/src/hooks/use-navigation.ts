import { NavigationContext } from "@/contexts/navigation-context";
import { useContext } from "react";

export function useNavigation() {
    const ctx = useContext(NavigationContext);
    if (!ctx) throw new Error("useNavigation must be used within a NavigationProvider");
    return ctx;
  }
  
  