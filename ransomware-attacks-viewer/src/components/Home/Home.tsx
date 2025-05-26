import { useEffect, useRef, useState } from 'react';

import './Home.css';

const phrases: string[] = [
  'Hello,',
  'Waves of ransomware attacks are sweeping across the globe...',
  'You have a mission.',
  'Use this tool to stay informed, stay alert — and stay ahead.',
  'The cyber battlefield is real. Will you rise to the challenge?'
];

const typingSpeed = 25;
const phraseDelay = 500;
const preGlitchPause = 2000;
const glitchChars = '█▓▒░<>|\\/[]{}-=+*#@!$%&?';

export const Home =() => {
  const [displayText, setDisplayText] = useState<string>('');
  const [isGlitching, setIsGlitching] = useState<boolean>(false);

  const phraseIndexRef = useRef<number>(0);
  const charIndexRef = useRef<number>(0);
  const currentTextRef = useRef<string>('');
  const glitchFrameRef = useRef<number>(0);

  // Timers ID refs
  const typingTimeoutRef = useRef<number | null>(null);
  const glitchTimeoutRef = useRef<number | null>(null);
  const glitchIntervalRef = useRef<number | null>(null);

  useEffect(() => {
    // Clean pends timers
    const clearTimers = () => {
      if (typingTimeoutRef.current !== null) {
        clearTimeout(typingTimeoutRef.current);
      }
      if (glitchTimeoutRef.current !== null) {
        clearTimeout(glitchTimeoutRef.current);
      }
      if (glitchIntervalRef.current !== null) {
        clearInterval(glitchIntervalRef.current);
      }
    };

    const typeText = (text: string, callback: () => void) => {
      if (charIndexRef.current < text.length) {
        currentTextRef.current += text.charAt(charIndexRef.current);
        setDisplayText(currentTextRef.current);
        charIndexRef.current += 1;
        typingTimeoutRef.current = window.setTimeout(
          () => typeText(text, callback),
          typingSpeed
        );
      } else {
        typingTimeoutRef.current = window.setTimeout(callback, phraseDelay);
      }
    };

    const startGlitch = (callback: () => void) => {
      setIsGlitching(true);
      glitchFrameRef.current = 0;
      const original = currentTextRef.current;

      glitchTimeoutRef.current = window.setTimeout(() => {
        glitchIntervalRef.current = window.setInterval(() => {
          let glitched = '';
          for (let i = 0; i < original.length; i++) {
            if (Math.random() > glitchFrameRef.current / 12) {
              glitched +=
                glitchChars.charAt(
                  Math.floor(Math.random() * glitchChars.length)
                );
            } else {
              glitched += ' ';
            }
          }
          setDisplayText(glitched);
          glitchFrameRef.current += 1;

          if (glitchFrameRef.current >= 12) {
            if (glitchIntervalRef.current !== null) {
              clearInterval(glitchIntervalRef.current);
            }
            setIsGlitching(false);
            currentTextRef.current = '';
            charIndexRef.current = 0;
            setDisplayText('');
            callback();
          }
        }, 50);
      }, preGlitchPause);
    };

    const cycle = () => {
      const phrase = phrases[phraseIndexRef.current];
      typeText(phrase, () => {
        startGlitch(() => {
          phraseIndexRef.current =
            (phraseIndexRef.current + 1) % phrases.length;
          cycle();
        });
      });
    };

    cycle();

    return () => {
      clearTimers();
    };
  }, []);

  return (
    <div className="flex flex-col items-center justify-center h-full w-full overflow-hidden bg-black text-[#00FF00] font-[VT323] text-4xl text-center px-6 select-none">
      {/* Google Font */}
      <style>{`@import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');`}</style>

      <div className="max-w-[90vw] whitespace-pre-wrap">{displayText}</div>

      {!isGlitching && (
        <div className="inline-block w-[10px] border-r-2 border-[#00FF00] animate-blink align-bottom" />
      )}
    </div>
  );
}
