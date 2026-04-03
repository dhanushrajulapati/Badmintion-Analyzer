"use client";

import Image from "next/image";
import { useState, useEffect, useRef } from "react";
import axios from "axios";
import Link from "next/link";
import { CardBody, CardContainer, CardItem } from "../../components/ui/3d-card";
import { BackgroundGradient } from "@/components/ui/background-gradient";
import { LampDemo } from "@/components/MyLamp";
import { CardSpotlightDemo } from "@/components/MySpecialCard";
import { CardSpotlightDemoScore } from "@/components/MyScore";
import { TextToSpeech } from "@/components/Audio";

import { GoogleGenerativeAI } from "@google/generative-ai";
import { WobbleCardDemo } from "@/components/Commentary";
import socket from "@/utils/socket";

export default function Harshit() {
  const [matchData, setMatchData] = useState<any>(null);
  const [score, setScore] = useState<number | null>(null);
  const [apidata, setApidata] = useState<string | null>(null);
  const [distance, setDistance] = useState<any>(null);
  const [key, setKey] = useState<any>("hello");
  const hasFetchedData = useRef(false);
  const [hitby, setHitby] = useState<any>(null);
  
  // 1. ADDED: State to track if we are currently fetching to prevent spam
  const [isFetching, setIsFetching] = useState(false);

  useEffect(() => {
    socket.on("update_match_data", (data) => {
      setMatchData(data);
      setHitby(data.HitPlayer);
    });

    return () => {
      socket.off("update_match_data");
    };
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      // 2. ADDED: If we are already fetching, or matchData isn't ready, stop here.
      if (isFetching || !matchData) return;
      
      setIsFetching(true); // Lock the function so it can't be spammed

      const apiKey = process.env.NEXT_PUBLIC_GEMINI_KEY || "AIzaSyAvguxIaYJqqWNrbtPEEOs7qdTih-5wGio";
      setKey(apiKey);

      const genAI = new GoogleGenerativeAI(apiKey);
      const model = genAI.getGenerativeModel({
        model: "gemini-1.5-flash",
        systemInstruction:
          "Generate 10 word commentary not more than 10 words. Ensure the commentary is engaging, uses sports jargon, and adds a touch of excitement. Output the generated commentary in JSON format {commentary : data} based on my given inputs . . . and generate different type of commentary every time and use my given numerical datas too. ",
        generationConfig: { responseMimeType: "application/json" },
      });

      const lastElementPlayer1 = matchData?.scoreArray["Player 1"]?.[matchData?.scoreArray["Player 1"].length - 1];
      const lastElementPlayer2 = matchData?.scoreArray["Player 2"]?.[matchData?.scoreArray["Player 2"].length - 1];
      
      let prompt: string = `Player 1 score is ${lastElementPlayer1?.score} and player 2 score is ${lastElementPlayer2?.score}`;
      
      if (matchData?.HitPlayer == "Player 1") {
        prompt = `Player 1 hit with the speed of  ${lastElementPlayer1?.speed} at a distance of ${lastElementPlayer1?.distance} and player 1 score is ${lastElementPlayer1?.score} and player 2 score is ${lastElementPlayer2?.score} `;
      }

      if (matchData?.HitPlayer == "Player 2") {
        prompt = `Player 2 hit with the speed of  ${lastElementPlayer2?.speed} at a distance of ${lastElementPlayer2?.distance} and player 2 score is ${lastElementPlayer2?.score} and player 1 score is ${lastElementPlayer1?.score} `;
      }

      // 3. ADDED: Try/Catch block to gracefully handle 429 Rate Limit Errors
      try {
        const result = await model.generateContent(prompt);
        const responseText = result.response.text();
        
        if (responseText) {
          const jsonObject = JSON.parse(responseText);
          setApidata(jsonObject.commentary);
        }
      } catch (error) {
        // This stops your app from crashing! It just logs the error instead.
        console.error("Gemini API Error (Rate Limit likely hit):", error);
      } finally {
        // 4. ADDED: Wait 5 seconds before allowing another API call
        setTimeout(() => {
          setIsFetching(false);
        }, 5000); 
      }
    };

    fetchData();
  }, [hitby]);

  return (
    <>
      <div className="min-h-screen bg-slate-950 py-12 pt-36">
        <LampDemo first={"Video with Analysis"}>
          <div className="flex flex-wrap justify-center">
            <div className="min-h-screen bg-slate-950 py-12 pt-36">
              <BackgroundGradient key={1} className="rounded-[22px]">
                <h1 className="text-lg md:text-4xl text-center font-sans font-bold mb-8 text-red-300">
                  {"Status"}
                </h1>

                <h1 className="text-lg md:text-5xl text-center  font-sans font-bold mb-8 text-white">
                  {matchData?.HitPlayer}
                </h1>
              </BackgroundGradient>
              <CardContainer key={1} className="inter-var m-4">
                <CardBody className="bg-gray-50 relative group/card dark:hover:shadow-2xl dark:hover:shadow-emerald-500/[0.1] dark:bg-black dark:border-white/[0.2] border-black/[0.1] w-auto sm:w-[30rem] h-auto rounded-xl p-6 border">
                  <CardItem
                    translateZ="50"
                    className="text-xl font-bold text-neutral-600 dark:text-white"
                  >
                    {"Live Distance"}
                  </CardItem>
                  <CardItem
                    as="p"
                    translateZ="60"
                    className="text-neutral-500 text-sm max-w-sm mt-2 dark:text-neutral-300"
                  >
                    {"Find Distance Covered by each Player Here"}
                  </CardItem>
                  <CardItem translateZ="100" className="w-full mt-4">
                    <CardSpotlightDemoScore
                      player1={matchData?.playerdistance["Player 1"]}
                      player2={matchData?.playerdistance["Player 2"]}
                    />
                  </CardItem>
                </CardBody>
              </CardContainer>
            </div>
            <div className="flex flex-wrap justify-center mt-11 m-9 ml-7 gap-5">
              <div>
                <img
                  src="http://localhost:5000/yolo_video_feed"
                  width="640"
                  height="480"
                  className="border border-gray-200 rounded-lg"
                  style={{ marginTop: "95px" }}
                />
              </div>

              <div>
                <img
                  src="http://localhost:5000/match_map_feed"
                  width="640"
                  height="900"
                  className="border border-gray-200 rounded-lg"
                  style={{ height: "682px", width: "543px" }}
                />
              </div>
              <div className="relative z-1 flex flex-wrap justify-center m-10">
                <CardContainer key={1} className="inter-var m-4">
                  <CardBody className="bg-gray-50 relative group/card dark:hover:shadow-2xl dark:hover:shadow-emerald-500/[0.1] dark:bg-black dark:border-white/[0.2] border-black/[0.1] w-auto sm:w-[30rem] h-auto rounded-xl p-6 border">
                    <CardItem
                      translateZ="50"
                      className="text-xl font-bold text-neutral-600 dark:text-white"
                    >
                      {"Live Score"}
                    </CardItem>
                    <CardItem
                      as="p"
                      translateZ="60"
                      className="text-neutral-500 text-sm max-w-sm mt-2 dark:text-neutral-300"
                    >
                      {"Find Live Score Here"}
                    </CardItem>

                    <CardItem translateZ="100" className="w-full mt-4">
                      <CardSpotlightDemoScore
                        player1={matchData?.liveScore["Player 1"]}
                        player2={matchData?.liveScore["Player 2"]}
                      />
                    </CardItem>
                  </CardBody>
                </CardContainer>
              </div>
            </div>
            {matchData && (
              <>
                <div className="flex flex-wrap justify-center gap-7 mt-8">
                  <br />
                  {matchData && (
                    <>
                      {" "}
                      <h1 className="text-lg md:text-5xl text-center  font-sans font-bold mb-8 text-white">
                        {"Player 1"}
                      </h1>
                      <div className="flex flex-wrap justify-center gap-7 mt-8">
                        <br />
                        {matchData?.scoreArray["Player 1"]
                          ?.slice(-4)
                          .map((shot: any, index: any) => (
                            <BackgroundGradient
                              key={index}
                              className="rounded-[22px]"
                            >
                              <CardSpotlightDemo
                                shot_number={index}
                                prop={shot.distance}
                                speed={shot.speed}
                                player={shot.score}
                              />
                            </BackgroundGradient>
                          ))}
                        <br />
                      </div>
                      <br />
                      <br />
                      <br />
                      <h1 className="text-lg md:text-5xl text-center  font-sans font-bold mb-8 text-white">
                        {"Player 2"}
                      </h1>
                      <div className="flex flex-wrap justify-center gap-7 mt-8">
                        <br />
                        {matchData?.scoreArray["Player 2"]
                          ?.slice(-4)
                          .map((shot: any, index: any) => (
                            <BackgroundGradient
                              key={index}
                              className="rounded-[22px]"
                            >
                              <CardSpotlightDemo
                                shot_number={index}
                                prop={shot.distance}
                                speed={shot.speed}
                                player={shot.score}
                              />
                            </BackgroundGradient>
                          ))}
                        <br />
                      </div>
                    </>
                  )}
                </div>
              </>
            )}
          </div>
        </LampDemo>
        <WobbleCardDemo apidata={apidata} />
        <TextToSpeech text={apidata} />
        <Link href={"/actual"} className="m-6 p-4 w-auto max-w-xs">
          <BackgroundGradient key={1} className="rounded-[12px] p-4">
            <h1 className="text-base md:text-lg text-center font-sans font-bold mb-4 text-red-300">
              {"Show actual video"}
            </h1>
          </BackgroundGradient>
        </Link>
      </div>
    </>
  );
}