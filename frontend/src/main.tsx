import "./index.css";

import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "./components/atoms/sonner";

import App from "./App.tsx";
import { NavigationProvider } from "./contexts/navigation-context.tsx";
import { GalleryProvider } from "./contexts/gallery-context.tsx";

const queryClient = new QueryClient();

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <NavigationProvider>
      <GalleryProvider>
        <QueryClientProvider client={queryClient}>
          <App />
        </QueryClientProvider>
      </GalleryProvider>
    </NavigationProvider>
    <Toaster />
  </StrictMode>
);
