import React from "react";
import { Composition } from "remotion";
import { KyujinhyoCard, DURATION, NgWord } from "./compositions/KyujinhyoCard";
import ngWords from "./content/ng-words.json";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {(ngWords as NgWord[]).map((word) => (
        <Composition
          key={word.id}
          id={`kyujinhyo-${word.id.toString().padStart(2, "0")}`}
          component={KyujinhyoCard}
          durationInFrames={DURATION}
          fps={30}
          width={1080}
          height={1920}
          defaultProps={{ word }}
        />
      ))}
    </>
  );
};
