import { useState } from "react";

export const useKurbilScore = () => {
  const [kurbilScore, setKurbilScore] = useState(5);

  return { kurbilScore, setKurbilScore };
};
