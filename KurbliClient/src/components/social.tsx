import { MutableRefObject, useEffect, useState } from "react";

interface SocialLinksProps {
  text: string;
  canvasRef: MutableRefObject<HTMLCanvasElement | null>;
}

function getCanvasImageUrl(canvas: HTMLCanvasElement): Promise<string | null> {
  return new Promise((resolve) => {
    canvas.toBlob((blob) => {
      if (blob) {
        const url = URL.createObjectURL(blob);
        console.log(url);
        resolve(url);
      } else {
        resolve(null);
      }
    }, "image/png");
  });
}

export function Social_links({ text, canvasRef }: SocialLinksProps) {
  const [canvasImageUrl, setCanvasImageUrl] = useState<string | null>(null);

  useEffect(() => {
    async function getUrl() {
      if (canvasRef.current) {
        const url = await getCanvasImageUrl(canvasRef.current);
        setCanvasImageUrl(url);
      }
    }
    getUrl();
  }, [canvasRef]);

  return (
    <div className="flex my-1">
      <div className="font-bold py-1 my-1 pr-3">{text}</div>
      <a
        href={`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(
          canvasImageUrl || ""
        )}`}
        target="_blank"
        rel="noopener noreferrer"
      >
        <img className="cursor-pointer p-1 m-1" alt="" src="/facebook.svg" />
      </a>
      <a
        href={`https://www.instagram.com/?url=${encodeURIComponent(
          canvasImageUrl || ""
        )}`}
        target="_blank"
        rel="noopener noreferrer"
      >
        <img className="cursor-pointer p-1 m-1" alt="" src="/instagram.svg" />
      </a>
      <a
        href={`https://www.linkedin.com/shareArticle?mini=true&url=${encodeURIComponent(
          canvasImageUrl || ""
        )}`}
        target="_blank"
        rel="noopener noreferrer"
      >
        <img className="cursor-pointer p-1 m-1" alt="" src="/linkedin.svg" />
      </a>
      <a
        href={`https://www.tiktok.com/@your_username_here?url=${encodeURIComponent(
          canvasImageUrl || ""
        )}`}
        target="_blank"
        rel="noopener noreferrer"
      >
        <img className="cursor-pointer p-1 m-1" src="tiktok.svg" />
      </a>
    </div>
  );
}
