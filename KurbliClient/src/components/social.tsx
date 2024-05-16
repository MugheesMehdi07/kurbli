import { MutableRefObject, useEffect, useState } from "react";

interface SocialLinksProps {
  canvasRef: MutableRefObject<HTMLCanvasElement | null>;
}

function getCanvasImageUrl(canvas: HTMLCanvasElement): Promise<string | null> {
  return new Promise((resolve) => {
    canvas.toBlob((blob) => {
      if (blob) {
        resolve(uploadImage(blob)); // Upload directly after creating blob
      } else {
        resolve(null);
      }
    }, "image/png");
  });
}

// Function to upload image to ImgBB and return public URL
async function uploadImage(blob: Blob): Promise<string> {
  const formData = new FormData();
  formData.append("image", blob);

  const apiKey = "a926e58ce71548f84cce88831a71c8df"; // Replace with your actual ImgBB API key
  const response = await fetch(`https://api.imgbb.com/1/upload?key=${apiKey}`, {
    method: "POST",
    body: formData,
  });

  if (response.ok) {
    const data = await response.json();
    return data.data.url; // ImgBB returns the URL of the uploaded image here
  } else {
    throw new Error("Failed to upload image");
  }
}

export function SocialLinks({ canvasRef }: SocialLinksProps) {
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
    <div className="flex mt-1 md:my-1">
      <a href={`https://www.tiktok.com`} target="_blank" rel="noopener noreferrer">
        <img
          className="cursor-pointer p-1 m-1"
          alt="Share on Tiktok"
          src="/tiktok.svg"
        />
      </a>
      <a
        href={`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(
          canvasImageUrl || ""
        )}`}
        target="_blank"
        rel="noopener noreferrer"
      >
        <img
          className="cursor-pointer p-1 m-1"
          alt="Share on Facebook"
          src="/facebook.svg"
        />
      </a>
      <a href={`https://www.instagram.com`} target="_blank" rel="noopener noreferrer">
        <img
          className="cursor-pointer p-1 m-1"
          alt="Share on Instagram"
          src="/instagram.svg"
        />
      </a>
      {/* Instagram does not support direct sharing of URLs. Link needs to be posted manually or through specific API integrations */}
      <a
        href={`https://www.linkedin.com/shareArticle?mini=true&url=${encodeURIComponent(
          canvasImageUrl || ""
        )}`}
        target="_blank"
        rel="noopener noreferrer"
      >
        <img
          className="cursor-pointer p-1 m-1"
          alt="Share on LinkedIn"
          src="/linkedin.svg"
        />
      </a>
      {/* TikTok sharing link needs to be updated according to their sharing API or guidelines */}
    </div>
  );
}
