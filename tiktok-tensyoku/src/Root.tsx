import React from "react";
import { Composition } from "remotion";
import { KyujinhyoCard, DURATION, NgWord } from "./compositions/KyujinhyoCard";
import { TensyokuStory, STORY_DURATION } from "./compositions/TensyokuStory";
import { Story01, STORY01_DURATION } from "./compositions/Story01";
import ngWords from "./content/ng-words.json";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* 台本①: 妻に「無理」と言われた45歳の転職 */}
      <Composition
        id="story-01"
        component={Story01}
        durationInFrames={STORY01_DURATION}
        fps={30}
        width={1080}
        height={1920}
      />

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
