/**
 *
 * Breaks the text line every 25 chars if no white-space
 * found
 */
export function preventTextOverflow(text: string) {
  const words = text.split(" ");
  const result: string[] = [];
  let currentLine = "";

  for (const word of words) {
    if (currentLine.length + word.length <= 25) {
      currentLine += (currentLine ? " " : "") + word;
    } else {
      if (currentLine) {
        result.push(currentLine);
      }
      if (word.length > 25) {
        for (let i = 0; i < word.length; i += 25) {
          result.push(word.slice(i, i + 25));
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
