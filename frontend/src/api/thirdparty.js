// API de terceros gratuita, sin API key: Advice Slip (frase/consejo motivador).
// https://api.adviceslip.com/
const ADVICE_URL = "https://api.adviceslip.com/advice";

export async function getMotivationalAdvice() {
  const response = await fetch(ADVICE_URL);
  if (!response.ok) {
    throw new Error("No se pudo obtener la frase del día");
  }
  const data = await response.json();
  return data.slip.advice;
}
