
import { GalleryContext } from "@/contexts/gallery-context";
import { useContext } from "react";

export function useGallery() {
    const ctx = useContext(GalleryContext);
    if (!ctx) throw new Error("useGallery must be used within a GalleryProvider");
    return ctx;
  }
  
  