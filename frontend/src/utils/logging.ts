const LOG_LEVEL = import.meta.env.VITE_LOG_LEVEL || "INFO";

function getTime() {
  return new Date().toLocaleTimeString();
}

export const logger = {
  debug: (...args: any[]) => {
    if (["DEBUG"].includes(LOG_LEVEL))
      console.log(`[🪲 <DEBUG> ${getTime()}]`, ...args);
  },
  info: (...args: any[]) => {
    if (["INFO", "DEBUG"].includes(LOG_LEVEL))
      console.log(`[ℹ️ ${getTime()}]`, ...args);
  },
  warn: (...args: any[]) => {
    if (["WARN", "INFO", "DEBUG"].includes(LOG_LEVEL))
      console.log(`[⚠️ ${getTime()}]`, ...args);
  },
  error: (...args: any[]) => {
    if (["ERROR", "WARN", "INFO", "DEBUG"].includes(LOG_LEVEL))
      console.log(`[⛔ ${getTime()}]`, ...args);
  },
};
