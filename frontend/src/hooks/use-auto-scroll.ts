import { useEffect } from "react";

export function useAutoScroll(elementId?: string) {
  useEffect(() => {
    if (elementId)
      document.getElementById(elementId)?.scrollIntoView({
        behavior: "instant",
      });
  }, [elementId]);
}
