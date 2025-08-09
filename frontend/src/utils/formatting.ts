/**
 *
 * Breaks the text line every maxLen chars if no white-space
 * found
 */
export function preventTextOverflow(text: string, maxLen = 25) {
  const words = text.split(" ");
  const result: string[] = [];
  let currentLine = "";

  for (const word of words) {
    if (currentLine.length + word.length <= maxLen) {
      currentLine += (currentLine ? " " : "") + word;
    } else {
      if (currentLine) {
        result.push(currentLine);
      }
      if (word.length > maxLen) {
        for (let i = 0; i < word.length; i += maxLen) {
          result.push(word.slice(i, i + maxLen));
        }
        currentLine = "";
      } else {
        currentLine = word;
      }
    }
  }

  if (currentLine) {
    result.push(currentLine);
  }

  return result.join("\n");
}
