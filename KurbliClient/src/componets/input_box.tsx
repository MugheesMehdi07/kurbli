import { useEffect, useState } from "react";
import { Score } from "./score";

export function Input() {
  const [email, setEmail] = useState("");
  const [isEmail, setIsEmail] = useState(true);
  const [valid_address, setValid_address] = useState(false);
  const [placeholder, setPlaceholder] = useState("Enter valid email");
  const [inputType, setInputType] = useState("email");
  const [button_text, setButton_text] = useState("NEXT");
  const [score, setScore] = useState(false);

  useEffect(() => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    setIsEmail(emailRegex.test(email));
  }, [email]);

  const address = () => {
    if (isEmail) {
      setPlaceholder("Start typing to select the address");
      setInputType("text");
      setButton_text("CALUCULATE SCORE");
      setEmail("");
      setValid_address(true);
    }
    if (valid_address && email.length > 0) {
      setScore(true);
    }
  };

  return (
    <div className="py-10">
      <div className="flex">
        <div>
          <div className="flex relative">
            <input
              type={inputType}
              className={`bg-[#FCFAF5] block w-full border ${
                isEmail ? "border-green-500" : "border-red-500"
              } text-lg rounded-full shadow px-6 font-medium py-3 w-96 pr-12`}
              value={email}
              placeholder={placeholder}
              required
              onChange={(e) => setEmail(e.target.value)}
            />

            {isEmail ? (
              <span className="absolute inset-y-0 right-0 pr-3 flex items-center">
                <svg
                  width="250px"
                  height="15px"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                  <g
                    id="SVGRepo_tracerCarrier"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  ></g>
                  <g id="SVGRepo_iconCarrier">
                    <g id="Warning / Circle_Check">
                      <path
                        id="Vector"
                        d="M15 10L11 14L9 12M12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12C21 16.9706 16.9706 21 12 21Z"
                        stroke="green"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      ></path>
                    </g>
                  </g>
                </svg>
              </span>
            ) : email.length > 0 && !isEmail && !valid_address ? (
              <span className="absolute inset-y-0 right-0 pr-3 flex items-center">
                <svg
                  width="250px"
                  height="15px"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                  // style={{ marginTop: "-25px" }}
                >
                  <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                  <g
                    id="SVGRepo_tracerCarrier"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  ></g>
                  <g id="SVGRepo_iconCarrier">
                    <g id="Warning / Circle_Check">
                      <path
                        d="M12 8H12.01M12 11V16M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z"
                        stroke="red"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      ></path>
                    </g>
                  </g>
                </svg>
              </span>
            ) : null}
            <button
              className="px-6 mx-4 rounded-full bg-[#D9A831] font-bold cursor-pointer relative z-10"
              onClick={address}
            >
              {button_text}
            </button>
          </div>
          {valid_address ||
            (!isEmail && email.trim() != "" && (
              <p className="text-[#FF7575] font-medium px-4">
                Please enter a valid email address
              </p>
            ))}
        </div>
      </div>
      {score && (
        <>
          <div className="flex flex-wrap justify-start mt-4">
            <div
              className="px-1 mb-2 mr-2 bg-[#CFFFEB] flex rounded-full"
              style={{ whiteSpace: "nowrap" }}
            >
              <img src="/premium.svg" width="20px" height="20px" />
              <div className="px-2 py-2 font-semibold ">Kurbil Score: 5</div>
            </div>

            <Score text="Crime Score: 10" color="#F5FFCF" />
            <Score text="School Score: 5" color="#CFF1FF" />
            <Score text="NSFR Score: 20" color="#CFD4FF" />
            <Score text="RFSR Score: 20" color="#F8CFFF" />
            <Score text="CAP Score: 1" color="#FFE6CF" />
          </div>
          <div className="font-semibold py-40">
            <p>pdf of the batch to share on the social media</p>
            <br />
            <p>pop open and then download</p>
          </div>
        </>
      )}
    </div>
  );
}
