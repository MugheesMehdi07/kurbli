import { useEffect, useRef } from "react";
import { Social_links } from "../components/social";

interface Props {
  handleClose: Function;
  score: number;
}

export function Scorebadge({ handleClose, score }: Props) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const socialCanvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    if (canvasRef.current) {
      const canvas = canvasRef.current;
      const ctx = canvas.getContext("2d");
      if (ctx) {
        const img = new Image();
        img.src = "/scorebadgeimg.jpg";
        img.onload = () => {
          ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
          ctx.font = "bold 48px Arial";
          ctx.fillStyle = "black";
          ctx.textAlign = "center";
          ctx.fillText(score.toString(), canvas.width / 2, canvas.height - 60);
        };
      }
    }
  }, [score]);

  const handleDownloadBadge = () => {
    if (canvasRef.current) {
      const canvas = canvasRef.current;
      canvas.toBlob((blob) => {
        if (blob) {
          const url = URL.createObjectURL(blob);
          const link = document.createElement("a");
          link.href = url;
          link.download = "score-badge.png";
          link.click();
          URL.revokeObjectURL(url);
        }
      }, "image/png");
    }
  };

  const handleBadgeCloseClick = () => {
    handleClose();
  };

  return (
    <div className="rounded-xl bg-white">
      <div className="text-center text-3xl bg-[#F9F1DE] py-3 rounded-t-xl grid grid-cols-12">
        <div className="col-span-11 text-center pl-10">Kurbli Score Badge</div>
        <button className="text-2xl" onClick={handleBadgeCloseClick}>
          &times;
        </button>
      </div>
      <div className="flex flex-col justify-center items-center">
        <canvas
          ref={(node) => {
            canvasRef.current = node;
            socialCanvasRef.current = node;
          }}
          width="300"
          height="257.38"
          className="pt-4"
        ></canvas>
        <p className="px-4 text-lg">
          Download or share your property score badge with your circle
        </p>
        <Social_links text="" canvasRef={socialCanvasRef} />
        <button
          className="px-6 py-3 my-3 mx-4 rounded-full bg-[#D9A831] font-bold cursor-pointer relative z-10"
          onClick={handleDownloadBadge}
        >
          DOWNLOAD BADGE
        </button>
      </div>
    </div>
  );
}
