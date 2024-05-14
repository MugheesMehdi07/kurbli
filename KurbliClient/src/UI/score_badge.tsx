import { useEffect, useRef, useState } from 'react';
import { Helmet } from 'react-helmet';
import { SocialLinks } from '../components/social'; // Ensure this path matches your actual component path

interface Props {
  handleClose: () => void;
  score: number;
}

export function ScoreBadge({ handleClose, score }: Props) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [imageReady, setImageReady] = useState(false);
  const [imageURL, setImageURL] = useState("");

  useEffect(() => {
    if (canvasRef.current) {
      const canvas = canvasRef.current;
      const ctx = canvas.getContext("2d");
      if (ctx) {
        const img = new Image();
        img.src = "/scorebadgeimg.jpg"; // Make sure the image path is correct
        img.onload = () => {
          ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
          ctx.font = "bold 48px Arial";
          ctx.fillStyle = "black";
          ctx.textAlign = "center";
          ctx.fillText(score.toString(), canvas.width / 2, canvas.height - 60);
          canvas.toBlob((blob) => {
            if (blob) {
              const url = URL.createObjectURL(blob);
              setImageURL(url);
              setImageReady(true); // Image is ready to be shared
              URL.revokeObjectURL(url); // Clean up the object URL
            }
          }, 'image/png');
        };
      }
    }
  }, [score]);

  const handleBadgeCloseClick = () => {
    handleClose();
  };

  const handleDownloadBadge = () => {
    if (canvasRef.current) {
      const canvas = canvasRef.current;
      canvas.toBlob((blob) => {
        if (blob) {
          const url = URL.createObjectURL(blob);
          const link = document.createElement('a');
          link.href = url;
          link.download = 'score-badge.png'; // Set the default filename for download
          link.click();
          URL.revokeObjectURL(url);
        }
      }, "image/png");
    }
  };

    handleClose();
  return (
    <div className="rounded-xl bg-white shadow-lg overflow-hidden">
      <Helmet>
        <title>Score Badge</title>
        <meta property="og:url" content={window.location.href} />
        <meta property="og:type" content="website" />
        <meta property="og:title" content="My Kurbli Score" />
        <meta property="og:description" content="Hey Guys, Checkout my latest Kurbli Score for my property" />
        <meta property="og:image" content={imageURL} />
        <meta property="og:image:width" content="300" />
        <meta property="og:image:height" content="257" />
      </Helmet>
      <div className="text-center text-3xl bg-[#F9F1DE] py-3 px-4">
        <span className="block">Kurbli Score Badge</span>
        <button className="absolute top-2 right-2 text-2xl" onClick={handleBadgeCloseClick}>&times;</button>
      </div>
      <div className="flex flex-col items-center p-4">
        <canvas ref={canvasRef} width="300" height="257.38" className="mb-4"></canvas>
        <p className="px-4 text-lg">
          Download or share your property score badge with your circle
        </p>
        {imageReady && <SocialLinks canvasRef={canvasRef} />}
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
