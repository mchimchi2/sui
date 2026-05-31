import React from "react";
import { Composition } from "remotion";
import { KyujinhyoCard, DURATION, NgWord } from "./compositions/KyujinhyoCard";
import { TensyokuStory, STORY_DURATION } from "./compositions/TensyokuStory";
import ngWords from "./content/ng-words.json";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* 40-50代向けストーリー動画 */}
      <Composition
        id="tensyoku-story-01"
        component={TensyokuStory}
        durationInFrames={STORY_DURATION}
        fps={30}
        width={1080}
        height={1920}
      />

      {/* 求人票裏読みシリーズ */}
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
